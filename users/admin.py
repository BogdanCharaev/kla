from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.hashers import make_password

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_teacher', 'is_student', 'is_headman')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    
    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password) # шифруем пароль перед сохранением
        super().save_model(request, obj, form, change)

#admin.site.register(User, UserAdmin)

from users.models import Discipline, Lesson, Attendance, StudyGroup 
 
class DisciplineAdmin(admin.ModelAdmin): 
    list_display = ('id', 'title', ) 
 
 
class LessonAdmin(admin.ModelAdmin): 
    list_display = ('id', 'start_time', 'end_time', 'discipline', 'group') 
 

 
class AttendanceAdmin(admin.ModelAdmin): 
    list_display = ('id', 'lesson', 'student', ) 
 
class StudyGroupAdmin(admin.ModelAdmin): 
    list_display = ('id', 'group_name', 'course_number' ) 
 

admin.site.register(StudyGroup,StudyGroupAdmin) 
admin.site.register(Discipline, DisciplineAdmin) 
admin.site.register(Lesson, LessonAdmin) 
admin.site.register(Attendance, AttendanceAdmin)