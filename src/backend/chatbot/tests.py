import json
import wave

from datetime import datetime
from unittest import skip
from django.test import TestCase, Client
from django.test.client import RequestFactory
from urllib3 import encode_multipart_formdata

f
from .models import User, Chat, Course, StudentCourse, Teacher, Club

# Create your tests here.
from .views import clear_chat_history, search_chat_history_date, modify_user_configuration


class TestChatHistory(TestCase):
    """
    This is a simple test class that tests if the user and chat models can work properly
    """
    def setUp(self):
        u1 = User.objects.create(openid="111", username="Harrison", nickname="Harry", bot_nickname="Harry's bot")
        u2 = User.objects.create(openid="222", username="Ron Weasley", nickname="Ron", bot_nickname="Ron's bot")

        Chat.objects.create(user=u1, content="Good morning to you.")
        Chat.objects.create(user=u1, is_bot=True, content="Good morning, how are you doing?")

        Chat.objects.create(user=u2, content="Howdy?")
        Chat.objects.create(user=u2, is_bot=True, content="Hello, how are you?")

    def test_get_user(self):
        u_list = User.objects.all()
        self.assertEquals(len(u_list), 2)

    def test_get_chat_history(self):
        u = User.objects.get(openid="111")
        self.assertEquals(u.chats.count(), 2)

    def test_get_chat_history_by_user_and_date(self):
        user = User.objects.get(openid="111")

        for chat in Chat.objects.filter(user=user, timestamp__year=datetime.now().year,
                                        timestamp__month=datetime.now().month, timestamp__day=datetime.now().day):
            self.assertEqual(chat.user, user)
            self.assertEqual(chat.timestamp.day, datetime.now().day)
            self.assertEqual(chat.timestamp.month, datetime.now().month)
            self.assertEqual(chat.timestamp.year, datetime.now().year)


class TestChatClient(TestCase):
    """
    This class tests all chat relevant functions such as get_chat_history, get_response, save_chat_to_history...
    """
    def setUp(self):
        u1 = User.objects.create(openid="111", username="Harrison", nickname="Harry", bot_nickname="Harry's bot")
        u2 = User.objects.create(openid="222", username="Ron Weasley", nickname="Ron", bot_nickname="Ron's bot")

        Chat.objects.create(user=u1, content="Good morning to you.")
        Chat.objects.create(user=u1, is_bot=True, content="Good morning, how are you doing?")

        Chat.objects.create(user=u2, content="Howdy?")
        Chat.objects.create(user=u2, is_bot=True, content="Hello, how are you?")

        self.c = Client()

    # 01 - Qicheng CHEN
    # Normal case where user posts the content along with the user openid, is_bot, is_audio
    def test_send_chat_api_POST(self):
        user = User.objects.get(openid="111")
        self.assertEquals(user.username, "Harrison")

        '''
        Example of testing using RequestFacotry()
        request = self.factory.get('/chatbot/')
        request.user = user
        self.assertTrue(request.user is not None)
        self.assertEqual(request.user, user)

        response = index(request)
        self.assertEqual(response.status_code, 200)
        '''

        # Test sending chat
        p_dict = {
            "openid": "111",
            "is_bot": False,
            "is_audio": False,
            "content": "I'm doing well."
        }

        response = self.c.post("/chatbot/save_chat", json.dumps(p_dict), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"code": 0, "msg": "Chat content saved."}
        )

        # Now there should be 3 chats associated with Harrison
        self.assertEquals(user.chats.count(), 3)

    # 02 - Qicheng CHEN
    # Case where the user access the URL with GET method instead of POST method, the request should be rejected
    def test_send_chat_api_GET(self):
        c = Client()
        response = c.get('/chatbot/save_chat')
        # print(response.content)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"code": 1, "msg": "POST request required."}
        )

    # 03 - Qicheng CHEN
    # When the user send an empty message, the message should not be saved
    def test_send_chat_api_empty_content(self):
        c = Client()

        p_dict = {
            "openid": "111",
            "is_bot": False,
            "is_audio": False,
            "content": ""
        }

        response = c.post("/chatbot/save_chat", json.dumps(p_dict), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"code": 1, "msg": "Expect chat content"}
        )

    # 04 - Qicheng CHEN
    # When the user send a message but without the user's openid, the request should be rejected
    def test_send_chat_api_without_openid(self):
        c = Client()

        p_dict = {
            "is_bot": False,
            "is_audio": False,
            "content": "No openid"
        }

        response = c.post("/chatbot/save_chat", json.dumps(p_dict), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"code": 1, "msg": "Expect openid"}
        )

    # 05 - Qicheng CHEN
    # When the client posts openid and content, but the openid is empty, the request should be rejected
    def test_send_chat_api_empty_openid(self):
        c = Client()

        p_dict = {
            "openid": "",
            "is_bot": False,
            "is_audio": False,
            "content": "Empty openid"
        }

        response = c.post("/chatbot/save_chat", json.dumps(p_dict), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"code": 1, "msg": "Expect openid"}
        )

    # 06 - Qicheng CHEN
    # When the client sends a request to delete all chats associated with a user, all the chats
    # related to that user should be deleted
    def test_clear_chat_history_api(self):
        user = User.objects.get(openid=111)
        self.assertEqual(user.chats.count(), 2)

        p_dict = {
            "openid": "111"
        }

        response = self.c.post('/chatbot/clear_chat', json.dumps(p_dict), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.chats.count(), 0)

    # 07 - Qicheng CHEN
    # When the client sends a request to delete all chats associated with a user but doesn't specify openid
    # the request should be rejected
    def test_clear_chat_history_api_empty_openid(self):
        user = User.objects.get(openid=111)
        self.assertEqual(user.chats.count(), 2)
        p_dict = {
            "openid": ""
        }
        request = self.factory.post('/chatbot/clear_chat', json.dumps(p_dict), content_type="application/json")
        request.user = user
        response = clear_chat_history(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(user.chats.count(), 2)

    # 08 - Qicheng CHEN
    # When the client asks to search all chats at a particular date for a particular user
    # All chats on that date associated with that user should be returned
    # This function is not yet implemented, so not heavily tested.
    def test_search_chat_history_api_by_date(self):
        user = User.objects.get(openid=111)

        request = self.factory.get("/chatbot/search_chat_date/111/2021/03/14")
        request.user = user
        response = search_chat_history_date(request, 111, datetime.now().year, datetime.now().month, datetime.now().day)

        self.assertEqual(response.status_code, 200)
        chats = json.loads(response.content)["chats"]
        self.assertEqual(len(chats), 2)

    # 09 - Qicheng CHEN
    # When the client sends a get chat history request with a specified user openid
    # All chats associated with that user should be returned
    def test_get_chats(self):
        c = Client()

        p_dict = {
            "openid": "111"
        }

        response = c.post("/chatbot/chat_history", json.dumps(p_dict), content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data.get("chats")), 2)

    # 10 - Qicheng CHEN
    # If the client sends a "get chat history" request without a specified user openid
    # the request should be rejected
    def test_get_chats_without_openid(self):
        c= Client()

        p_dict = {} # Empty dict

        response = c.post("/chatbot/chat_history", json.dumps(p_dict), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    # 11 - Qicheng CHEN
    # When the client sends a text with an openid to the URL, a response generated by the chat bot
    # model should be returned The response of the chat bot should be saved to database at the mean time
    def test_get_response(self):
        c = Client()

        p_dict = {
            "openid": "111",
            "text": "What is your name?"
        }

        response = c.post("/chatbot/get_response", json.dumps(p_dict), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(openid="111")
        self.assertEqual(user.chats.count(), 3)

    # 12 - Qicheng CHEN
    # If the client sends a text without an openid to the URL, the request should be rejected
    def test_get_response_empty_openid(self):
        c = Client()

        p_dict = {
            "openid": "",
            "text": "What is your name?"
        }

        response = c.post("/chatbot/get_response", json.dumps(p_dict), content_type="application/json")
        self.assertEqual(response.status_code, 400)


class TestModifyConfig(TestCase):
    def setUp(self):
        u1 = User.objects.create(openid="111", username="Harrison", nickname="Harry", bot_nickname="Harry's bot")
        u2 = User.objects.create(openid="222", username="Ron Weasley", nickname="Ron", bot_nickname="Ron's bot")

        Chat.objects.create(user=u1, content="Good morning to you.")
        Chat.objects.create(user=u1, is_bot=True, content="Good morning, how are you doing?")

        Chat.objects.create(user=u2, content="Howdy?")
        Chat.objects.create(user=u2, is_bot=True, content="Hello, how are you?")

        self.factory = RequestFactory()

    # 13 - Qicheng CHEN
    # Under usual circumstances, the client will post fields that need to be modified, along with
    # an openid about which user it should modify
    # The modification should be reflected in the database
    def test_modify_config(self):
        user = User.objects.get(openid=111)
        self.assertEqual(user.nickname, "Harry")

        p_dict = {
            "openid": "111",
            "nickname": "Wells"
        }

        request = self.factory.post("/chatbot/modify", json.dumps(p_dict), content_type="application/json")
        request.user = user
        response = modify_user_configuration(request)
        user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.nickname, "Wells")

    # 14 - Qicheng CHEN
    # If the client sends a modification request but without any specified field, the request will not be rejected
    # But nothing will change in the database
    def test_modify_config_with_no_modification(self):
        user = User.objects.get(openid="111")
        self.assertEqual(user.nickname, "Harry")

        p_dict = {
            "openid": "111"
        }
        c = Client()
        response = c.post("/chatbot/modify", json.dumps(p_dict), content_type="application/json")
        user.refresh_from_db()
        self.assertEqual(response.status_code, 200)

    # 15 - Qicheng CHEN
    # If the client sends a modification request but without openid, the request will be rejected
    def test_modify_config_without_openid(self):
        user = User.objects.get(openid="111")
        self.assertEqual(user.nickname, "Harry")

        p_dict = {
            "nickname": "Wells"
        }
        c = Client()
        response = c.post("/chatbot/modify", json.dumps(p_dict), content_type="application/json")
        user.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(user.nickname, "Harry")
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"code": 1, "msg": "Expect openid"}
        )


class GenerateResponseFromDatabaseTest(TestCase):
    def setUp(self):
        StudentCourse.objects.create(student_id='20126522', week_day=1, course_id='comp2048')
        StudentCourse.objects.create(student_id='20126522', week_day=2, course_id='comp2049')

        Teacher.objects.create(name='Heshan Du', email='comp2048@nottingham.edu.cn', office="PMB-432",
                               office_hour="Tuesday 14:00-16:00"
                               , research_area="algorithms, big data and artificial intelligence")

        Teacher.objects.create(name='Amin', email='comp2049@nottingham.edu.cn', office="PMB-432",
                               office_hour="Monday 14:00-16:00"
                               , research_area="algorithms, big data and artificial intelligence")

        Course.objects.create(course_id='comp2048', course_name='Algorithms Correctness and Effciency',
                              course_type='lecture', week_day='1',
                              course_time='9:00-11:00', teacher=Teacher.objects.get(name='Heshan Du'))


        Club.objects.create(name='SESA', club_info='only sociation in UNNC', club_official_account='HAHAHAH')
        '''
        Course.objects.create(course_id='comp2048', course_name='Algorithms Correctness and Effciency',
                              course_type='Lab', week_day='2',
                              course_time='16:00-18:00', teacher='Heshan Du')
        Course.objects.create(course_id='comp2049', course_name='Language and Computations',
                              course_type='Lab', week_day='1',
                              course_time='14:00-15:00', teacher='Amin')
        Course.objects.create(course_id='comp2049', course_name='Language and Computations',
                              course_type='Lab', week_day='7',
                              course_time='14:00-15:00', teacher='Amin')
        '''

    # 01 - Longwen Hu
    # when input type is teacher and input teacher name can be found in database, it should respsonse 0 in 'code'
    def test_generate_database_response_01(self):
        c = Client()
        response = c.get("/chatbot/generate_database_response?type=teacher&id=heshan du")
        self.assertEqual(response.json()['code'], 0)

    # 02 - Longwen Hu
    # when input type is teacher and input teacher name cannot be found in database, it should respsonse 1 in 'code'
    def test_generate_database_response_02(self):
        c = Client()
        response = c.get("/chatbot/generate_database_response?type=teacher&id=heshandu")
        self.assertEqual(response.json()['code'], 1)

    # 03 - Longwen Hu
    # when input type is club and input club name can be found in database, it should respsonse 0 in 'code'
    def test_generate_database_response_03(self):
        c = Client()
        response = c.get("/chatbot/generate_database_response?type=club&id=SESA")
        self.assertEqual(response.json()['code'], 0)

    # 04 - Longwen Hu
    # when input type is club and input club name cannot be found in database, it should response 1 in 'code'
    def test_generate_database_response_04(self):
        c = Client()
        response = c.get("/chatbot/generate_database_response?type=club&id=ACCA")
        self.assertEqual(response.json()['code'], 1)

    # 05 - Longwen Hu
    # when input type is course and input student id can be found in database, its response status_code should be 200
    def test_generate_database_response_05(self):
        c = Client()
        response = c.get("/chatbot/generate_database_response?type=course&id=20126522")
        self.assertEqual(response.status_code, 200)

    # delete corresponding week_day objetcs in Student_Course table
    # 06 - Longwen Hu
    # when input type is course and input student id can be found in database, if there is no course for the subject, 'ans' states "no such course today"
    @skip("Pass when current day do not have crouse")
    def test_generate_database_response_06(self):
        c = Client()
        response = c.get("/chatbot/generate_database_response?type=course&id=20126522")
        retlist = response.json()['retlist']
        self.assertIsNone(retlist)



    # 07 - Longwen Hu
    # when input type is course and input student id cannot be found in database, it should return with status_code = 400 and 'prob' states 'student id cannot be found'
    def test_generate_database_response_07(self):
        c = Client()
        response = c.get("/chatbot/generate_database_response?type=course&id=20000000")
        prob = response.json()['prob']
        self.assertEqual(response.status_code, 400)
        self.assertEqual(prob, 'student id cannot be found')


    # 08 - Longwen Hu
    # when input type is course and input student id can be found in database, and course can be found in that day,it should return with 'ret' equals 0
    def test_generate_database_response_08(self):
        c = Client()
        response = c.get("/chatbot/generate_database_response?type=course&id=20126522")
        ret = response.json()['code']
        self.assertEqual(ret, 0)

    # 09 - Longwen Hu
    # when input type cannot be recoginized, its response status_code should be 400
    def test_generate_database_response_09(self):
        c = Client()
        response = c.get("/chatbot/generate_database_response?type=null")

        self.assertEqual(response.status_code, 400)


class GenerateTextFromAudioTest(TestCase):
    @skip("Pass when current computer is involed in the Internet")
    # 10 - Longwen Hu
    # when user pass a correct audio file, which is a wav file, its response status code should be 200
    def test_generate_text_from_audio_01(self):
        c = Client()
        wave_file = open("chatbot/audio/proper_untransed_audio.wav", "rb")
        url_str = "/chatbot/audio2text"
        response = c.post(url_str, {"audio": wave_file})
        wave_file.close()
        self.assertEqual(response.status_code, 200)

    # 11 - Longwen Hu
    # when user pass an incorrect audio file, which is not a wav file, its response status code should be 400
    # and in response's 'ret', it will states 'incorrect file type'
    def test_generate_text_from_audio_02(self):
        c = Client()
        wave_file = open("chatbot/audio/test.txt", "rb")
        url_str = "/chatbot/audio2text"
        response = c.post(url_str, {"audio": wave_file})
        wave_file.close()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['ret'], "incorrect file type")

    # 12 - Longwen Hu
    # when user pass nothing in audio, it should response "no file founded" in 'ret', and status code should be 400
    def test_generate_text_from_audio_03(self):
        c = Client()
        url_str = "/chatbot/audio2text?audio="
        response = c.get(url_str)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['ret'], "no file founded")

    # 13 - Longwen Hu
    # when user input a file that is greater than 1MB, it should response "input file should no more than 1MB" in "ret" and status code should be 400
    def test_generate_text_from_audio_04(self):
        c = Client()
        wave_file = open("chatbot/audio/test_file_exceed_max_size.wav", "rb")
        url_str = "/chatbot/audio2text"
        response = c.post(url_str, {"audio": wave_file})
        wave_file.close()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['ret'], "input file should no more than 1MB")