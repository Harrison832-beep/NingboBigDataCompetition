import os
import subprocess
from datetime import datetime
import json
from aip import AipSpeech

from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


from . import log_in_out
from .models import Chat, User, Course, StudentCourse, Teacher, Club

from chatterbot.trainers import UbuntuCorpusTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot
from django.core.cache import cache
import hashlib, time

from backend import settings

chatbot = ChatBot(**settings.CHATTERBOT, logic_adapters=[
    {
        "import_path": "chatterbot.logic.BestMatch",
        "default_response": "I am sorry, I don't understand.",
        "maximum_similarity_threshold": 0.90
    }
])


# Uncomment the two lines to train the chat bot
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train("chatterbot.corpus.english")
# trainer.train("chatterbot.corpus.chinese")

@csrf_exempt
def login(request):
    """
    author: Chunlong ZHENG
    Login function that accepts a code sent by WeChat mini-program, decode and obtain associated openid to get user
    If there is no user associate with the openid, a new user will be created
    """
    if request.method != "POST":
        return JsonResponse({"code": 1, "msg": "POST method required."}, status=400)

    param = json.loads(request.body)
    if not param.get("code"):
        return JsonResponse({"code": 1, "msg": "Missing parameter"})
    else:
        code = param.get("code")
        user_data = log_in_out.get_login_info(code)
        if user_data:
            val = user_data["session_key"] + "&" + user_data["openid"]
            md5 = hashlib.md5()
            md5.update(str(time.clock()).encode("utf-8"))
            md5.update(user_data["session_key"].encode("utf-8"))
            key = md5.hexdigest()
            cache.set(key, val)
            user = User.objects.filter(openid=user_data["openid"]).first()
            if user is None:
                user = User.objects.create(openid=user_data["openid"], username=user_data["openid"], password="123456")
            User.objects.update()

            return JsonResponse({
                "code": 0,
                "msg": "ok",
                "data": {"token": key,
                         "openid": user_data["openid"],
                         "nickname": user.nickname,
                         "bot_nickname": user.bot_nickname,
                         "font_size": user.font_size,
                         "font_color": user.font_color,
                         "font_style": user.font_style,
                         "image_path": user.image_path
                         }
            }, status=200)
        else:
            return JsonResponse({"code": 1, "msg": "Invalid code"}, status=400)


@csrf_exempt
def modify_user_configuration(request):
    """
    author: Chunlong ZHENG
    Clicking on the "save" button in the configuration page should save the changes to the database and reflect
    changes to the user.
    If the openid is not specified or empty, the request will be rejected.
    """
    if request.method != "POST":
        return JsonResponse({"code": 1, "msg": "POST method required."}, status=400)

    data = json.loads(request.body)
    openid = data.get("openid")
    if openid is None or len(openid) == 0:
        return JsonResponse({"code": 1,
                             "msg": "Expect openid"}, status=400)

    try:
        user = User.objects.get(openid=openid)
    except User.DoesNotExist:
        return JsonResponse({
            "code": 1,
            "msg": f"User {request.user.username} does not exist"
        }, status=400)

    if "nickname" in data:
        user.nickname = data.get("nickname")
    if "bot_nickname" in data:
        user.bot_nickname = data.get("bot_nickname")
    if "font_size" in data:
        user.font_size = data.get("font_size")
    if "font_color" in data:
        user.font_color = data.get("font_color")
    if "font_style" in data:
        user.font_style = data.get("font_style")
    if "image_path" in data:
        user.image_path = data.get("image_path")

    # Save changes to database
    user.save()
    print(f"{data.get('nickname')}, nickname: {user.nickname}")
    return JsonResponse({"code": 0, "msg": "Configurations saved", "data": {
        "nickname": user.nickname,
        "bot_nickname": user.bot_nickname,
        "font_size": user.font_size,
        "font_color": user.font_color,
        "font_style": user.font_style,
        "image_path": user.image_path
    }}, status=200)


@csrf_exempt
def save_chat_to_history(request):
    """
    author: Qicheng CHEN
    Accepts a POST request with specified openid, content, is_bot, is_audio, which specifies if the message
    is sent by a bot or not, whether it is an audio message or not.
    """
    if request.method != "POST":
        return JsonResponse({"code": 1,
                             "msg": "POST request required."}, status=400)

    data = json.loads(request.body)
    openid = data.get("openid")

    if openid is None or len(openid) == 0:
        return JsonResponse({"code": 1,
                             "msg": "Expect openid"}, status=400)

    user = User.objects.get(openid=openid)

    if len(data.get("content")) == 0 or "content" not in data:
        return JsonResponse({"code": 1,
                             "msg": "Expect chat content"}, status=400)

    try:
        Chat.objects.create(user=user, is_bot=data.get("is_bot"),
                            is_audio=data.get("is_audio"), content=data.get("content"))
        Chat.objects.update()
    except IntegrityError:
        return JsonResponse({"code": 1,
                             "msg": "Cannot create chat history."}, status=500)

    return JsonResponse({"code": 0,
                         "msg": "Chat content saved."}, status=200)


@csrf_exempt
def get_chat_history(request):
    """
    author: Qicheng CHEN
    When a POST request with an openid is sent to the server, the server should return all chats associated with
    the user with the openid, if no openid is specified, the request will be rejected.
    """
    data = json.loads(request.body)
    openid = data.get("openid")
    if openid is None or len(openid) == 0:
        return JsonResponse({"code": 1,
                             "msg": "Expect openid"}, status=400)

    user = User.objects.get(openid=openid)

    return JsonResponse({"code": 0,
                         "chats": [chat.serialize() for chat in user.chats.all()]}, status=200)


def search_chat_history_date(request, openid, year, month, day):
    """
    author: Qicheng CHEN
    When a POST request is sent to the server to request for chats associated with a user with a particular date,
    related chats will be returned.
    """
    user = User.objects.get(openid=openid)
    chats = Chat.objects.filter(user=user,
                                timestamp__year=year,
                                timestamp__month=month,
                                timestamp__day=day)

    return JsonResponse({
        "code": 0,
        "msg": "Chat fetch successful.",
        "chats": [chat.serialize() for chat in chats]
    }, status=200)


@csrf_exempt
def clear_chat_history(request):
    """
    author: Qicheng CHEN
    When a POST request is sent to the server to delete all the chats associated with the user, an openid should be
    specified in order to find the user, otherwise the request will be rejected.
    """
    if request.method != "POST":
        return JsonResponse({"code": 1, "msg": "POST request required."}, status=400)

    data = json.loads(request.body)
    openid = data.get("openid")
    if openid is None or len(openid) == 0:
        return JsonResponse({"code": 1,
                             "msg": "Expect openid"}, status=400)

    user = User.objects.get(openid=openid)

    for chat in user.chats.all():
        try:
            chat.delete()
        except IntegrityError:
            return JsonResponse({"code": 1,
                                 "msg": "IntegrityError: Delete failure"}, status=500)

    return JsonResponse({
        "code": 0,
        "msg": "Chat history deleted successfully."
    }, status=200)


@csrf_exempt
def generate_response(request):
    """
    author: Qicheng CHEN
    reference: https://chatterbot.readthedocs.io/en/stable/
    Response will be generated according to the user input.
    The response will be saved to database before it is returned.
    """
    if request.method != "POST":
        return JsonResponse({
            "code": 1,
            "msg": "Post method is required"
        }, status=400)

    data = json.loads(request.body)
    openid = data.get("openid")
    if openid is None or len(openid) == 0:
        return JsonResponse({"code": 1,
                             "msg": "Expect openid"}, status=400)

    if "text" not in data:
        return JsonResponse({
            "msg": [
                "The attribute 'text' is required"
            ]
        }, status=400)

    response = chatbot.get_response(data)
    response_data = response.serialize()

    user = User.objects.get(openid=data.get("openid"))

    # Save response from the bot to database
    Chat.objects.create(
        user=user,
        is_bot=True,
        content=response_data.get("text")
    )

    Chat.objects.update()
    # print(response_data)
    return JsonResponse(response_data, status=200)


def get_course_data(request):
    '''
    author: Longwen Hu
    Get the course data in database based on input student id
    '''
    student_id = request.GET.get('id')
    week_day = datetime.now().isoweekday()
    courseID = StudentCourse.objects.filter(student_id=student_id, week_day=week_day).values()
    if courseID:
        retlist = []
        for course_info in courseID:
            course_id = course_info['course_id']
            qs = Course.objects.filter(course_id=course_id, week_day=week_day).values()
            retlist = retlist + list(qs)
        result = {'code': 0, 'retlist': retlist}
        return HttpResponse(json.dumps(result, ensure_ascii=False), status=200,
                            content_type="application/json,charset=utf-8")
    else:
        is_id_valid = StudentCourse.objects.filter(student_id=student_id)
        if is_id_valid:
            retlist = {}
            result = {'code': 0, 'retlist': retlist}
            return HttpResponse(json.dumps(result, ensure_ascii=False), status=200,
                                content_type="application/json,charset=utf-8")
        else:
            return JsonResponse({"code": 1, 'prob': 'student id cannot be found'}, status=400)


def get_teacher_data(request):
    '''
    author: Longwen Hu
    Get the teacher data in database based on input teacher name
    '''
    name = request.GET.get('id')
    if name:
        qs = Teacher.objects.filter(name__contains=name).values()
        retlist = list(qs)
        if retlist:
            result = {'code': 0, 'retlist': retlist}
            return HttpResponse(json.dumps(result, ensure_ascii=False), status=200,
                                content_type="application/json,charset=utf-8")
        else:
            return JsonResponse({"code": 1}, status=400)
    else:
        return JsonResponse({"code": 1}, status=400)


def get_club_data(request):
    '''
    author: Longwen Hu
    Get the club data in database based on input clue name
    '''
    name = request.GET.get('id')
    if name:
        qs = Club.objects.filter(name__contains=name).values()
        if qs:
            retlist = list(qs)
            result = {'code': 0, 'retlist': retlist}
            return HttpResponse(json.dumps(result, ensure_ascii=False), status=200,
                                content_type="application/json,charset=utf-8")
        else:
            return JsonResponse({"code": 1}, status=400)
    else:
        return JsonResponse({"code": 1}, status=400)


def generate_database_response(request):

    """
    author: Longwen Hu
    Generate the response accroding to user's request with the data from data base
    """
    type = request.GET.get('type')
    if type == 'course':
        return get_course_data(request)
    elif type == 'teacher':
        return get_teacher_data(request)
    elif type == 'club':
        return get_club_data(request)
    else:
        return JsonResponse({"code": 1}, status=400)


@csrf_exempt
def generate_text_from_audio(request):
    '''
    author: Longwen Hu
    Reference: https://cloud.baidu.com/doc/SPEECH/s/Bk4o0bmt3
    Transfer input audio into text by calling baidu's api and return the text back to front-end
    '''
    audio = request.FILES.get('audio')

    if not audio:
        return JsonResponse({"ret": "no file founded"}, status=400)

    if str(audio.name)[-3:] == 'wav':
        APP_ID = '23868076'
        API_KEY = 'wrwTmcWdRFG3rG8KYW0LqBOd'
        SECRET_KEY = '85l0hhinnbO0cGURUDL1923pL3QAo4yM'

        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        untransed_file_path = "chatbot/audio/untransed_audio.wav"
        transed_file_path = "chatbot/audio/transed_audio.wav"

        file = open(untransed_file_path,'wb')
        for chrunk in audio.chunks():
            file.write(chrunk)
        file.close()

        #untransed file should be less than 1 MB
        fsize = os.path.getsize(untransed_file_path)
        fsize = fsize/(float)(1024*1024)
        if fsize >= 1:
            return JsonResponse({"ret": "input file should no more than 1MB"}, status=400)

        __trans_audio_ar(untransed_file_path, transed_file_path)
        result = client.asr(__get_file_content(transed_file_path), 'wav', 16000, {
            'dev_pid': 1737,
        })

        response = result['result']
        return JsonResponse({"ret": 1, 'response':response}, status=200)
    else:
        return JsonResponse({"ret": "incorrect file type"}, status=400)


def __get_file_content(file_path):
    '''
    author: Longwen Hu
    Open local file
    '''
    with open(file_path, 'rb') as fp:
        return fp.read()


def __trans_audio_ar(input_file,output_file):
    '''
    author: Longwen Hu
    Calling ffmpeg to change input audio's acquisition rate
    '''
    command = f"ffmpeg -y -i {input_file} -ar 16000 {output_file}"
    subprocess.call(command,shell=True)
