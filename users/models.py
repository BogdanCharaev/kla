from django.contrib.auth.models import AbstractUser
from django.db import models


class StudyGroup(models.Model): 
    group_name = models.CharField(max_length=150) 
    course_number = models.IntegerField()
    
    def __str__(self):
        return self.group_name
    
    class Meta:
        
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    second_name = models.CharField(
        max_length=150,
        verbose_name='Отчество'
    )
    group = models.ForeignKey(StudyGroup, 
                              on_delete=models.CASCADE, 
                              related_name='group_students', null=True, blank=True) 
    
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_headman = models.BooleanField(default=False)

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'is_student', 'is_teacher', 'is_headman')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


 
class AttendanceCheck(models.Model): 
    pass 
 
class Discipline(models.Model): 
    title = models.CharField(max_length=150, verbose_name='Дисциплина') 
 
    def __str__(self): 
        return self.title
    
    class Meta:
        
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
 
class Lesson(models.Model): 
    start_time = models.DateTimeField() 
    end_time = models.DateTimeField()
    place = models.CharField(max_length=50, verbose_name='Аудитория', default='3 корпус 325 ауд.')
    lecturer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='lessons',
                                 verbose_name='Лектор')
    discipline = models.ForeignKey( 
        Discipline, 
        on_delete=models.CASCADE, 
    ) 
    group = models.ForeignKey(StudyGroup, 
                              on_delete=models.SET_NULL, 
                              related_name='group_lessons', null=True, blank=True) 
     
    def __str__(self): 
        return self.discipline.title 
    
    class Meta:
        
        verbose_name = 'Пара'
        verbose_name_plural = 'Пары'

 
class Attendance(models.Model): 
    lesson = models.ForeignKey( 
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='lesson', 
    ) 
    student = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name='student', 
    ) 
    isPresent = models.BooleanField(default=False)

    class Meta:
        
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'