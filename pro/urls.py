
from django.contrib import admin
from django.urls import path

from app import views


urlpatterns = [

    path('admin/', admin.site.urls),

    # HOME

    path('', views.home, name='home'),

    # AUTH

    path('register/', views.register, name='register'),

    path('login/', views.login_user, name='login'),

     path('dashboard/', views.dashboard, name='dashboard'),

     path('settings/', views.settings_view, name='settings'),

    path('logout/', views.logout_user, name='logout'),

    # STUDENTS

    path('students/', views.students, name='students'),

    path('add-student/',
         views.add_student,
         name='add_student'),

    path('edit-student/<int:id>/',
         views.edit_student,
         name='edit_student'),

    path('delete-student/<int:id>/',
         views.delete_student,
         name='delete_student'),

    path('student-profile/<int:id>/',
         views.student_profile,
         name='student_profile'),

    # ATTENDANCE

    path('attendance/',
         views.attendance,
         name='attendance'),

    path('mark-attendance/<int:id>/',
         views.mark_attendance,
         name='mark_attendance'),

    path('mark-absent/<int:id>/',
         views.mark_absent,
         name='mark_absent'),

    path('attendance-history/',
         views.attendance_history,
         name='attendance_history'),

    # RESULTS

    path('results/',
         views.results,
         name='results'),

    path('add-result/',
         views.add_result,
         name='add_result'),

    path('download-result/<int:id>/',
         views.download_result,
         name='download_result'),

    # FEES

    path('fees/',
         views.fees,
         name='fees'),

    path('add-fees/',
         views.add_fees,
         name='add_fees'),

    # FACULTY

    path('faculty/',
         views.faculty,
         name='faculty'),

    path('add-faculty/',
         views.add_faculty,
         name='add_faculty'),

    # TIMETABLE

    path('timetable/',
         views.timetable,
         name='timetable'),

    path('add-timetable/',
         views.add_timetable,
         name='add_timetable'),

]
