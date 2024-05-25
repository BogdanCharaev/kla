from django.shortcuts import get_object_or_404, redirect, render
import datetime
from users.models import User, Attendance, Lesson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from users.models import Attendance, AttendTimer

def index(request):
    hello = 'hello'
    return render(request, 'index.html', {'hello': hello})

def profile(request):
    user = request.user
    dt_now = datetime.datetime.now()
    lessons = user.lessons.all()
    actual_lesson = ''
    end_t = ''
    st_lesson = ''
    end_t_st = ''
    hd_lesson = ''
    end_t_hd = ''
    att = False
    can_attend = False
    if request.user.is_headman:
        
        group = user.group
        hd_lessons = group.group_lessons.all()
        for lesson in hd_lessons:
            if (lesson.start_time.timestamp() < dt_now.timestamp()) and (lesson.end_time.timestamp() > dt_now.timestamp()):
                hd_lesson = lesson
        if hd_lesson:
            end_t_hd = hd_lesson.end_time.strftime('%H:%M')
        

    if request.user.is_student:
        
        group = user.group
        st_lessons = group.group_lessons.all()
        for lesson in st_lessons:
            if (lesson.start_time.timestamp() < dt_now.timestamp()) and (lesson.end_time.timestamp() > dt_now.timestamp()):
                st_lesson = lesson
        if st_lesson:
            end_t_st = st_lesson.end_time.strftime('%H:%M')
        
        att = Attendance.objects.filter(lesson=st_lesson, student=request.user)
        timer = False
        timers = st_lesson.timer.all()
        can_attend = False
        for time in timers:
            if (time.start_time.timestamp() < dt_now.timestamp()) and ((time.start_time + datetime.timedelta(minutes=15)).timestamp() > dt_now.timestamp()):
                can_attend = True
            else:
                can_attend = False


    for lesson in lessons:
        if (lesson.start_time.timestamp() < dt_now.timestamp()) and (lesson.end_time.timestamp() > dt_now.timestamp()):
            actual_lesson = lesson
    if actual_lesson:
        end_t = actual_lesson.end_time.strftime('%H:%M')
    
        
    return render(request, 'users/profile.html', {'user': user,
                                                  'dt_now': dt_now,
                                                  'actual_lesson': actual_lesson,
                                                  'end_t': end_t,
                                                  'st_lesson': st_lesson,
                                                  'end_t_st': end_t_st,
                                                  'att':att,
                                                  'end_t_hd': end_t_hd,
                                                  'hd_lesson': hd_lesson,
                                                  'can_attend': can_attend})
@login_required
def attendance_by_teacher(request):
    user = request.user
    dt_now = datetime.datetime.now()
    lessons = user.lessons.all()
    actual_lesson = False
    for lesson in lessons:
        if (lesson.start_time.timestamp() < dt_now.timestamp()) and (lesson.end_time.timestamp() > dt_now.timestamp()):
            actual_lesson = lesson
    if actual_lesson:
        end_t = actual_lesson.end_time.strftime('%H:%M')
        students = actual_lesson.group.group_students.all()
    attendance = False;
    attendances = {}
    for student in students:
        attendances[student] = Attendance.objects.filter(lesson=actual_lesson, student=student)

    
    return render(request, 'users/attendance_by_teacher.html', {'actual_lesson':actual_lesson,
                                                                'end_t': end_t,
                                                                'students': students,
                                                                'attendances': attendances})

@login_required
def attendance_by_headman(request):
    user = request.user
    dt_now = datetime.datetime.now()
    group = user.group
    hd_lessons = group.group_lessons.all()
    actual_lesson = False
    for lesson in hd_lessons:
        if (lesson.start_time.timestamp() < dt_now.timestamp()) and (lesson.end_time.timestamp() > dt_now.timestamp()):
            actual_lesson = lesson
    if actual_lesson:
        end_t = actual_lesson.end_time.strftime('%H:%M')
        students = actual_lesson.group.group_students.all()
    attendances = {}
    for student in students:
        attendances[student] = Attendance.objects.filter(lesson=actual_lesson, student=student)
    return render(request, 'users/attendance_by_headman.html', {'actual_lesson':actual_lesson,
                                                                'end_t': end_t,
                                                                'students': students,
                                                                'attendances': attendances})

def create_attendance_teacher(request, ls_id, st_id):
    lesson = Lesson.objects.get(id = ls_id)
    user = User.objects.get(id = st_id)
    Attendance.objects.create(lesson = lesson, student = user)

    return redirect('users:teacher')

def remove_attendance_teacher(request, ls_id, st_id):
    lesson = Lesson.objects.get(id = ls_id)
    user = User.objects.get(id = st_id)
    
    object = Attendance.objects.filter(lesson = lesson, student = user)
    if object.exists():
        object.delete()

    return redirect('users:teacher')

def create_attendace_stud(request, ls_id, st_id):
    lesson = Lesson.objects.get(id = ls_id)
    user = User.objects.get(id = st_id)

    Attendance.objects.create(lesson = lesson, student = user)
    
    return redirect('users:profile')

def remove_attendace_stud(request, ls_id, st_id):
    lesson = Lesson.objects.get(id = ls_id)
    user = User.objects.get(id = st_id)

    object = Attendance.objects.filter(lesson = lesson, student = user)
    if object.exists():
        object.delete()
    
    return redirect('users:profile')

def rdir_to_login(request):
    return redirect('users:login')



def create_attendance_headman(request, ls_id, st_id):
    lesson = Lesson.objects.get(id = ls_id)
    user = User.objects.get(id = st_id)
    Attendance.objects.create(lesson = lesson, student = user)

    return redirect('users:headman')

def remove_attendance_headman(request, ls_id, st_id):
    lesson = Lesson.objects.get(id = ls_id)
    user = User.objects.get(id = st_id)
    
    object = Attendance.objects.filter(lesson = lesson, student = user)
    if object.exists():
        object.delete()

    return redirect('users:headman')


def lessons(request):
    lessons = request.user.lessons.all()
    return render(request, 'users/lessons.html', {'lessons': lessons})


def lesson_detail(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    group = lesson.group
    students = group.group_students.all()
    attendances = {}
    for student in students:
        attendances[student] = Attendance.objects.filter(lesson=lesson, student=student)
    

    
    return render(request, 'users/lesson_detail.html', {'lesson':lesson, 'students':students, 'attendances': attendances})


def export_to_excel(request, id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    lesson = Lesson.objects.get(id=id)

    wb = Workbook()
    ws = wb.active
    ws.title = 'title'

    # Add headers
    headers = ["Студент", "Был не был"]
    ws.append(headers)

    lesson = get_object_or_404(Lesson, id=id)
    group = lesson.group
    students = group.group_students.all()
    attendances = {}
    for student in students:
        attendances[student] = Attendance.objects.filter(lesson=lesson, student=student)
    for st, att in attendances:
        ws.append([st, att])

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response

def att_timer(request,id):
    lesson = get_object_or_404(Lesson, id=id)
    AttendTimer.objects.create(lesson=lesson)
    return redirect('users:profile')

