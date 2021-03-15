from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm,Registrationform
from django.contrib.auth import authenticate, login, logout
import os
from .models import UserProfile,User
from django.urls import path, include
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required

from django.contrib import messages
import face_recognition
import cv2 

def facedect(loc):
        cam = cv2.VideoCapture(0)   
        s, img = cam.read()
        if s:   
                
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MEDIA_ROOT =os.path.join(BASE_DIR,)

                loc=(str(MEDIA_ROOT)+loc)
                face_1_image = face_recognition.load_image_file(loc)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

                #

                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
                

                print(check)
                if check[0]:
                        print(User.username)
                        return True

                else :
                        return False    

def about(request):
    return render(request,"about.html",{})

def base(request):
        if request.method =="POST":
                form =LoginForm(request.POST)
                if form.is_valid():
                        username=request.POST['username']
                        password=request.POST['password']
                        user = authenticate(request,username=username,password=password)
                        if user is not None:

                                if facedect(user.userprofile.head_shot.url):
                                        login(request,user)
                                        if user.username == 'khirod':
                                                return redirect('profile')
                                        else:
                                                pass

                                return redirect('index')
                        else:
                                messages.info(request, 'Username OR password is incorrect')       
        else:
                MyLoginForm = LoginForm()
                return render(request,"base.html",{"MyLoginForm": MyLoginForm})  

def home(request):
   return render(request, 'home.html', {})

#from django.contrib.auth.forms import UserCreationForm



def index(request):
    return render(request,"index.html",{})


def register(request):
        if request.method =="POST":
                form =Registrationform(request.POST)
                if form.is_valid():
                        form.save()
                        username=form.cleaned_data['username']
                        password=form.cleaned_data['password1']
                        user = authenticate(username=username,password=password)
                        login(request,user)
                        return redirect('snap')
                else:
                        error=form.errors
                        # return redirect('error', {'error':error})
                        return render(request,'error.html',{'error':error})           

        form =Registrationform()
        return render(request,'registration/register.html',{'form':form})        

@login_required(login_url='base')
def profile(request):
        return render(request,'profile.html',{})


def common(request):
        return render(request,'common.html',{})


def error(request):
        return render(request,'error.html',{})


@login_required(login_url='base')
def snap(request):
        if request.method == 'POST' :
                head_shot = request.FILES['filename']

                # fs = FileSystemStorage()
                # file=fs.save(myfile.name, myfile)
                # head_shot="media/"+myfile.name
                user=request.user
                print(head_shot)
                prop=UserProfile(user=user, head_shot=head_shot)
                prop.save()
                return redirect('index')
        return render(request,'snap.html',{})

     



def logout(request):
	logout(request)
	return redirect('base')



# def reg(request):
#         if request.method == 'POST' :
#                 username=request.POST['name']
#                 email=request.POST['email']
#                 password=request.POST['psw']
#                 password1=request.POST['psw-rep']
#                 #myfile=request.FILES['filename']
#                 # fs = FileSystemStorage()
#                 # file=fs.save(myfile.name, myfile)
#                 # image="media/"+myfile.name
#                 user= User.objects.create_user(username=username, password=password, email=email )
#                 user.save()
#                 print("user created")

#         return render(request,'reg.html',{})
