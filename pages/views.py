from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .form import *
from .utils import send_email_to_client
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.signing import Signer
import random

# Create your views here.
def index(request):
    userId = request.user.username
    print(userId)
    context = {
        'username':userId,
        'title':"Password Saver | Home",
    }
    return render(request,'index.html',context)

def loginPage(request):
    if request.method == "POST":
        data = request.POST
        usernameR = data.get("username")
        passwordR = data.get("password")

        users = authenticate(username = usernameR, password = passwordR)
        if users is None:
            messages.error(request,"Incorrect Username or Password")
            return redirect('/login')
            
        else:
            login(request,users)
            return redirect("/")

    return render(request,'login.html')

def signupPage(request):
    if request.method == 'POST':
        data = request.POST

        usernameR = data.get('username')
        emailR = data.get('email')
        passwordR = data.get('password')
        pinR = data.get('pin')

        if User.objects.filter(email = emailR).exists():
            print("Email Already Exists")
            messages.error(request,"Email Already Exists. Try Login")
            return redirect('/signUp')
        
        if User.objects.filter(username = usernameR).exists():
            print("Username Already Exists")
            messages.error(request,"Username Already Exists. Try New")
            return redirect('/signUp')

        if checkUsernameRequirenment(usernameR) == True:
            if checkPasswordRequirenment(passwordR) == True:
                if len(pinR) == 4:
                    code = random.randint(1000,9999)
                    entry = TemporaryData.objects.create(
                        username = usernameR,
                        email = emailR,
                        password = passwordR,
                        pin = pinR,
                        conformation = False,
                        code = code
                    )
                    send_email_to_client(usernameR,emailR,code)
                    entry.save()
                    sendId = entry.id
                    
                    return redirect(f'/checkCode/{sendId}')
                else:
                    messages.error(request,"4 digit Pin Required")
                    return redirect('/signUp')
            else:
                messages.error(request,"Password must Uppercase,Lowercase,SpecialChar,Number")
                return redirect('/signUp')
        else:
            messages.error(request,"Username Must Cointain 6 Characters")
            return redirect('/signUp')

        
    return render(request,"signup.html")


def sendConformation(request,id):
    user = TemporaryData.objects.get(id = id)
    usrEmail = user.email
    context = {'email': usrEmail}
    code = user.code
    print(type(code))
    if request.method == "POST":
        data = request.POST
        codeR = int(data.get("code"))
        print(type(codeR))

        if codeR == code:
            print("conform")
            username = user.username
            password = user.password
            usr = User.objects.create(
                username = username,
                email = usrEmail,
                password = password,
            )
            usr.set_password(password)
            usr.save()
            login(request, usr)
            return redirect("/")
        else:
            print("Error")
            return redirect(f"/checkCode/{id}")

    return render(request,'email.html',context)


def passwordPage(request):
        
    if request.method == "POST":
        data = request.POST

        userInfo = TemporaryData.objects.get(email = request.user.email)
        nameR = data.get('name')
        usernameR = data.get('username')
        passwordR = data.get('password')
        email = request.user.email
        if len(nameR) < 4 and len(usernameR) < 4 and len(email):
            messages.error(request,"Can't Leave Blank")
            return redirect('/details')
        
        UserNamePassword.objects.create(
            email = email,
            name = nameR,
            username = usernameR,
            password = passwordR,
            pin = userInfo.pin,
        )
        return redirect('/details')
    if request.user.is_authenticated:
        usernamepass = UserNamePassword.objects.filter(email = request.user.email)
        context = {'userpassword':usernamepass,
               'title':"Password Saver | Details"}
        return render(request,'password.html',context)
    else:
        context = {'title':"Password Saver | Details"}
        return render(request,'password.html',context)

    

def deleteDetails(request,id):
    details = UserNamePassword.objects.get(id = id)
    if request.method =="POST":
        data = request.POST
        pinR = data.get("pin")
        if pinR != 4:
            messages.error(request,"Wrong Pin")
            return redirect(f"/delete/{id}")
        if int(pinR) == details.pin:
            details.delete()
            return redirect(f"/details")
        else :
            messages.error(request,"Wrong Pin")
            return redirect(f"/delete/{id}")
    context = {'name' : details.name}
    return render(request,'delete.html',context)

def sendEmail(request):
    send_email_to_client()
    return redirect('/')

def logoutPage(request):
    logout(request)
    return redirect('/')

