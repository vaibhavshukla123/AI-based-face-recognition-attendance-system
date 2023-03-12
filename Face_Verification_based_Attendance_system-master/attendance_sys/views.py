from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Student, Attendance
from .filters import AttendanceFilter

# from django.views.decorators import gzip

from .recognizer import Recognizer
from datetime import date


import face_recognition
import numpy as np
import cv2
import os

from django.http import JsonResponse


names = []

@login_required(login_url = 'login')
def home(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data = request.POST, files=request.FILES)
        # print(request.POST)
        stat = False 
        try:
            student = Student.objects.get(registration_id = request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get('firstname') +" " +studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name + ' was successfully added.')
            return redirect('home')
        else:
            messages.error(request, 'Student with Registration Id '+request.POST['registration_id']+' already exists.')
            return redirect('home')

    context = {'studentForm':studentForm}
    return render(request, 'attendance_sys/home.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'attendance_sys/login.html', context)

@login_required(login_url = 'login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
def updateStudentRedirect(request):

    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            branch = request.POST['branch']
            student = Student.objects.get(registration_id = reg_id, branch = branch)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form':updateStudentForm, 'prev_reg_id':reg_id, 'student':student}
        except:
            messages.error(request, 'Student Not Found')
            return redirect('home')
    return render(request, 'attendance_sys/student_update.html', context)

@login_required(login_url = 'login')
def updateStudent(request):
    if request.method == 'POST':
        context = {}
        try:
            student = Student.objects.get(registration_id = request.POST['prev_reg_id'])
            updateStudentForm = CreateStudentForm(data = request.POST, files=request.FILES, instance = student)
            if updateStudentForm.is_valid():
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                return redirect('home')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('home')
    return render(request, 'attendance_sys/student_update.html', context)


@login_required(login_url = 'login')
def takeAttendance(request):
    if request.method == 'POST':
        details = {
            'branch':request.POST['branch'],
            'year': request.POST['year'],
            'section':request.POST['section'],
            'period':request.POST['period'],
            'faculty':request.user.faculty
            }
        if Attendance.objects.filter(date = str(date.today()),branch = details['branch'], year = details['year'], section = details['section'],period = details['period']).count() != 0 :
            messages.error(request, "Attendance already recorded.")

            return JsonResponse({'status':True,'message':'Already recorded', 'url': 'http://127.0.0.1:8000'})
            # return redirect('home')
        else:
            return JsonResponse({'status':True,'message':'Plese record', 'url': ''})
            # students = Student.objects.filter(branch = details['branch'], year = details['year'], section = details['section'])
            # # camera()
            # names = Recognizer(details)
            # for student in students:
            #     if str(student.registration_id) in names:
            #         attendance = Attendance(Faculty_Name = request.user.faculty, 
            #         Student_ID = str(student.registration_id), 
            #         period = details['period'], 
            #         branch = details['branch'], 
            #         year = details['year'], 
            #         section = details['section'],
            #         status = 'Present')
            #         attendance.save()
            #     else:
            #         attendance = Attendance(Faculty_Name = request.user.faculty, 
            #         Student_ID = str(student.registration_id), 
            #         period = details['period'],
            #         branch = details['branch'], 
            #         year = details['year'], 
            #         section = details['section'])
            #         attendance.save()
            # attendances = Attendance.objects.filter(date = str(date.today()),branch = details['branch'], year = details['year'], section = details['section'],period = details['period'])
            # context = {"attendances":attendances, "ta":True}
            # messages.success(request, "Attendance taking Success")
            # return render(request, 'attendance_sys/attendance.html', context)        
    context = {}
    return render(request, 'attendance_sys/take_attendance.html', context)

def searchAttendance(request):
    attendances = Attendance.objects.all()
    myFilter = AttendanceFilter(request.GET, queryset=attendances)
    attendances = myFilter.qs
    context = {'myFilter':myFilter, 'attendances': attendances, 'ta':False}
    return render(request, 'attendance_sys/attendance.html', context)


def facultyProfile(request):
    faculty = request.user.faculty
    form = FacultyForm(instance = faculty)
    context = {'form':form}
    return render(request, 'attendance_sys/facultyForm.html', context)






def addStudent(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data = request.POST, files=request.FILES)
        # print(request.POST)
        stat = False 
        try:
            student = Student.objects.get(registration_id = request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get('firstname') +" " +studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name + ' was successfully added.')
            return redirect('home')
        else:
            messages.error(request, 'Student with Registration Id '+request.POST['registration_id']+' already exists.')
            return redirect('home')

    context = {'studentForm':studentForm}
    return render(request, 'attendance_sys/add_student.html', context)

# def takeAttendance(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data = request.POST, files=request.FILES)
        # print(request.POST)
        stat = False 
        try:
            student = Student.objects.get(registration_id = request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get('firstname') +" " +studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name + ' was successfully added.')
            return redirect('home')
        else:
            messages.error(request, 'Student with Registration Id '+request.POST['registration_id']+' already exists.')
            return redirect('home')

    context = {'studentForm':studentForm}
    return render(request, 'attendance_sys/home.html', context)



def studentUpdate(request):
    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            branch = request.POST['branch']
            student = Student.objects.get(registration_id = reg_id, branch = branch)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form':updateStudentForm, 'prev_reg_id':reg_id, 'student':student}
        except:
            messages.error(request, 'Student Not Found')
            return redirect('home')
    return render(request, 'attendance_sys/update_student.html', context)



#new code
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

@gzip.gzip_page
def camera(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    # return render(request, 'app1.html')

#to capture video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    details = {
        'branch':"CSE",
        'year': 1,
        'section':"A",
        'period':1,
        'faculty':"VENU GOPALKADAMBA"
        }
    known_face_encodings = []
    known_face_names = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.getcwd()
    image_dir = os.path.join(base_dir,"{}\{}\{}\{}\{}\{}".format('static','images','Student_Images',details['branch'],details['year'],details['section']))
    
    for root,dirs,files in os.walk(image_dir):
        for file in files:
            if file.endswith('jpg') or file.endswith('png'):
                path = os.path.join(root, file)
                img = face_recognition.load_image_file(path)
                label = file[:len(file)-4]
                img_encoding = face_recognition.face_encodings(img)[0]
                known_face_names.append(label)
                known_face_encodings.append(img_encoding)

    face_locations = []
    face_encodings = []

    while True:
        frame = camera.frame
        check = camera.grabbed
        small_frame = cv2.resize(frame, (0,0), fx=0.5, fy= 0.5)
        rgb_small_frame = small_frame[:,:,::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []


        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)

            face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)	
            
            try:
                matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)

                face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    face_names.append(name)
                    if name not in names:
                        names.append(name)
            except:
                pass

        if len(face_names) == 0:
            for (top,right,bottom,left) in face_locations:
                top*=2
                right*=2
                bottom*=2
                left*=2

                cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255,255,255),1)
        else:
            for (top,right,bottom,left), name in zip(face_locations, face_names):
                top*=2
                right*=2
                bottom*=2
                left*=2

                cv2.rectangle(frame, (left,top),(right,bottom), (0,255,0), 2)

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left, top), font, 0.8, (255,255,255),1)
                print (name)
        

        _, jpeg = cv2.imencode('.jpg', frame)

        # print ("names")
        # print (names)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        # return names
    





# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         ret,image = self.video.read()
#         ret,jpeg = cv2.imencode('.jpg',image)
#         return jpeg.tobytes()


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield(b'--frame\r\n'
#         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# @gzip.gzip_page
# def videoFeed(request):
#     try:
#         return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
#     except:
#         print("aborted")

# def getVideo(request):
#     return render(request, 'attendance_sys/videoFeed.html')


def saveAttendance(request):
    print("names")
    print(names)
    details = {
        'branch':"CSE",
        'year': 1,
        'section':"A",
        'period':1,
        'faculty':"VENU GOPALKADAMBA"
        }
    students = Student.objects.filter(branch = details['branch'], year = details['year'], section = details['section'])
    for student in students:
        if str(student.registration_id) in names:
            attendance = Attendance(Faculty_Name = request.user.faculty, 
            Student_ID = str(student.registration_id), 
            period = details['period'], 
            branch = details['branch'], 
            year = details['year'], 
            section = details['section'],
            status = 'Present')
            attendance.save()
        else:
            attendance = Attendance(Faculty_Name = request.user.faculty, 
            Student_ID = str(student.registration_id), 
            period = details['period'],
            branch = details['branch'], 
            year = details['year'], 
            section = details['section'])
            attendance.save()
    attendances = Attendance.objects.filter(date = str(date.today()),branch = details['branch'], year = details['year'], section = details['section'],period = details['period'])
    context = {"attendances":attendances, "ta":True}
    messages.success(request, "Attendance is taken successfully")
    return render(request, 'attendance_sys/attendance.html', context) 
   
