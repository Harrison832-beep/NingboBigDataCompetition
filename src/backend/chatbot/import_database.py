import sys

from chatbot.models import StudentCourse, Teacher, Course, Club
from termcolor import cprint


def import_student_course():
    '''
    student_id = models.CharField(max_length=200)
    course_id = models.CharField(max_length=200)
    week_day = models.IntegerField(default=0)
    '''
    in_file = open("student_course.txt", "r")
    StudentCourse.objects.all().delete()
    for line in in_file:
        vals =line.strip().split(", ")
        StudentCourse.objects.create(student_id=vals[0], course_id=vals[1], week_day=int(vals[2]))
    in_file.close()
    cprint("Import course success", "green")


def import_teacher():
    '''
    name = models.CharField(max_length=200,primary_key=True)
    email = models.CharField(max_length=200)
    office = models.CharField(max_length=200)
    office_hour = models.CharField(max_length=200,default="null")
    research_area = models.CharField(max_length=200)
    '''
    in_file = open("teacher.txt", "r")
    Teacher.objects.all().delete()
    for line in in_file:
        vals = line.strip().split(", ")
        Teacher.objects.create(name=vals[0], email=vals[1], office=vals[2], office_hour=vals[3], research_area=vals[4])
    in_file.close()
    cprint("Import success", "green")


def import_course():
    '''
    course_id = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    course_type = models.CharField(max_length=200)
    course_class = models.CharField(max_length=200,default='null')
    week_day = models.IntegerField(max_length=200)
    course_time = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,default='')
    '''
    in_file = open("course.txt", "r")
    Course.objects.all().delete()
    for line in in_file:
        vals =line.strip().split(", ")
        print(vals)
        Course.objects.create(course_id=vals[0], course_name=vals[1], course_type=vals[2],
                            course_class=vals[3], week_day=int(vals[4]), course_time=vals[5], teacher=Teacher.objects.get(name=vals[6]))
    in_file.close()
    cprint("Import success", "green")


def import_club():
    '''
    name = models.CharField(max_length=200)
    club_info = models.CharField(max_length=200)
    club_official_account = models.CharField(max_length=200,default='null')
    '''
    in_file = open("club.txt", "r")
    Club.objects.all().delete()
    for line in in_file:
        vals =line.strip().split(", ")
        Club.objects.create(name=vals[0], club_info=vals[1], club_official_account=vals[2])
    in_file.close()
    cprint("Import success", "green")


def import_from_file():
    """
    Every import function will actually clear records in the database first, then add records to the database.
    Records are read from files.
    """
    import_student_course()
    import_teacher()
    import_course()
    import_club()
    cprint("Import success", "green")



