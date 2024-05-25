from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path
from . import views
from .views import export_to_excel
app_name = 'users'

urlpatterns = [
    path('index/', views.index, name='index'),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path('prof/', views.profile, name='profile'),
    path('attendance_by_teacher/', views.attendance_by_teacher, name='teacher'),
    path('create_att/<int:ls_id>/<int:st_id>/', views.create_attendance_teacher, name='create_att'),
    path('remove_att/<int:ls_id>/<int:st_id>/', views.remove_attendance_teacher, name='remove_att'),
    path('create_stud/<int:ls_id>/<int:st_id>/', views.create_attendace_stud, name='create_att_stud'),
    path('remove_stud/<int:ls_id>/<int:st_id>/', views.remove_attendace_stud, name='remove_att_stud'),
    path('attendance_by_headman/', views.attendance_by_headman, name='headman'),
    path('rdir_to_login', views.rdir_to_login, name = 'rdir'),
    path('remove_att_hd/<int:ls_id>/<int:st_id>/', views.remove_attendance_headman, name='remove_att_hd'),
    path('create_att_hd/<int:ls_id>/<int:st_id>/', views.create_attendance_headman, name='create_att_hd'),
    path('lessons/', views.lessons, name='lessons'),
    path('lesson_detail/<int:id>', views.lesson_detail, name='lesson_detail'),
    path('export/<int:id>/', export_to_excel, name='export_to_excel'),
    path('start_timer/<int:id>/', views.att_timer, name='timer')

    
]  