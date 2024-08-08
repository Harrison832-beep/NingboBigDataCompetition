from django.contrib import admin

# Register your models here.
from .models import User, Chat, StudentCourse, Teacher, Course, Club


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "nickname")

class Student_CourseAdmin(admin.ModelAdmin):
    list_display = ("student_id", "course_id","week_day")

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "email","office","office_hour","research_area")
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content")

class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_id", "course_name")

class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "club_info")

admin.site.register(User, UserAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(StudentCourse, Student_CourseAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Club, ClubAdmin)

