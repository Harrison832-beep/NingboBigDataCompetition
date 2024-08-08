# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class StudentCourse(models.Model):
    student_id = models.CharField(max_length=200)
    course_id = models.CharField(max_length=200)
    week_day = models.IntegerField(default=0)


class Teacher(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    email = models.CharField(max_length=200)
    office = models.CharField(max_length=200)
    office_hour = models.CharField(max_length=200, null=True)
    research_area = models.CharField(max_length=200)


class Course(models.Model):
    course_id = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    course_type = models.CharField(max_length=200)
    course_class = models.CharField(max_length=200, null=True)
    week_day = models.IntegerField(default=0)
    course_time = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)


class Club(models.Model):
    name = models.CharField(max_length=200)
    club_info = models.CharField(max_length=200)
    club_official_account = models.CharField(max_length=200, null=True)


class User(AbstractUser):
    nickname = models.CharField(max_length=30, default="WeChat User")
    bot_nickname = models.CharField(max_length=30, default="Siri")
    font_size = models.IntegerField(default=30)
    font_color = models.CharField(default="Black", max_length=30)
    font_style = models.CharField(default="Medium", max_length=30)
    openid = models.CharField(max_length=255, blank=False, unique=True)
    language = models.CharField(max_length=50, default="en")
    image_path = models.CharField(max_length=255, default="/static/background.jpg") # Background image


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "bot_nickname": self.bot_nickname,
            "font_size": self.font_size,
            "font_style": self.font_style,
            "openid": self.openid,
            "language": self.language,
            "image": self.image_path,
            "chats": [chat.serialize() for chat in self.chats.all()]
        }

    def __str__(self):
        return f"{self.nickname}"


class Chat(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="chats")
    is_bot = models.BooleanField(default=False)
    content = models.CharField(max_length=200, blank=False)
    is_audio = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "is_bot": self.is_bot,
            "is_audio": self.is_audio,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

    def __str__(self):
        return f"{self.content}"
