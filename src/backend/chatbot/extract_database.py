from chatbot.models import StudentCourse, Teacher, Course, Club


def write_student_course():
    '''
    student_id = models.CharField(max_length=200)
    course_id = models.CharField(max_length=200)
    week_day = models.IntegerField(default=0)
    '''
    out_file = open("student_course.txt", "w")
    for sc in StudentCourse.objects.all():
        for v in sc.serialize().values():
            print("")

        print(f"{sc.student_id}, {sc.course_id}, {sc.week_day}", file=out_file)
    out_file.close()


def write_teacher():
    '''
    name = models.CharField(max_length=200,primary_key=True)
    email = models.CharField(max_length=200)
    office = models.CharField(max_length=200)
    office_hour = models.CharField(max_length=200,default="null")
    research_area = models.CharField(max_length=200)
    '''
    out_file = open("teacher.txt", "w")
    for t in Teacher.objects.all():
        print(f"{t.name}, {t.email}, {t.office}, {t.office_hour}, {t.research_area}", file=out_file)
    out_file.close()


def write_course():
    '''
    course_id = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    course_type = models.CharField(max_length=200)
    course_class = models.CharField(max_length=200,default='null')
    week_day = models.CharField(max_length=200)
    course_time = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,default='')
    '''
    out_file = open("course.txt", "w")
    for c in Course.objects.all():
        print(f"{c.course_id}, {c.course_name}, {c.course_type}, {c.course_class}, {c.week_day}, {c.course_time}, {c.teacher.name}", file=out_file)
    out_file.close()


def write_club():
    '''
    name = models.CharField(max_length=200)
    club_info = models.CharField(max_length=200)
    club_official_account = models.CharField(max_length=200,default='null')
    '''
    out_file = open("club.txt", "w")
    for c in Club.objects.all():
        print(f"{c.name}, {c.club_info}, {c.club_official_account}", file=out_file)
    out_file.close()


def write_to_file():
    write_student_course()
    write_teacher()
    write_course()
    write_club()


