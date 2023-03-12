from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('searchattendance/', views.searchAttendance, name='searchattendance'),
    path('addstudent/', views.addStudent, name='addstudent'),
    # path('takeattendance/', views.takeAttendance, name='takeattendance'),
    path('account/', views.facultyProfile, name='account'),

    path('updateStudentRedirect/', views.updateStudentRedirect, name='updateStudentRedirect'),
    path('updateStudent/', views.updateStudent, name='updateStudent'),
    path('studentUpdate/', views.studentUpdate, name='studentUpdate'),   #new
    path('attendance/', views.takeAttendance, name='attendance'),
    path('camera/', views.camera, name='camera'),
    path('saveAttendance/', views.saveAttendance, name='saveAttendance'),

    # path('video_feed/', views.videoFeed, name='video_feed'),
    # path('videoFeed/', views.getVideo, name='videoFeed'),
]