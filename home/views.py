from anonimo.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from django.views.decorators.csrf import  csrf_exempt
from home.models import Resources,editProfile, FollowersCount,FriendRequest,Bank,Doctor
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from blogapp.models import Post, Like
from doctorapp.models import Session
import os
import razorpay
import random, pickle

#ML preprocessing
from nltk.stem import PorterStemmer,WordNetLemmatizer
import nltk,re
def preprocess(data):
    nltk.download('wordnet')
    wo = WordNetLemmatizer()
    #preprocess
    a = re.sub('[^a-zA-Z]',' ',data)
    a = a.lower()
    a = a.split()
    a = [wo.lemmatize(word) for word in a ]
    a = ' '.join(a)  
    return a

# Create your views here.
def home(request):
    friend_count = len(FriendRequest.objects.filter(to_user = request.user))
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if request.user.is_authenticated:
        user_data = len(editProfile.objects.filter(profile_user=request.user))
        if doc>0:
            doc_present=True
            
            return render(request,'home.html',{'doc_present':doc_present})
        if user_data!=0:
            user_data1 = editProfile.objects.get(profile_user=request.user)
            mental_count = user_data1.count_mentalH
            approved = user_data1.approval
            return render (request, 'home.html',{'friend_count':friend_count,'mental_count':mental_count,'approved':approved,'doc_present':doc_present})
        else:
            acc_create = Bank(profile_user = request.user,account_bal=0)
            acc_create.save()
            account_bal = 0
            return render (request, 'home.html',{'friend_count':friend_count,})
    return render(request, 'home.html')

def resources(request):
    blogs = Resources.objects.all()
    friend_count = len(FriendRequest.objects.filter(to_user = request.user))
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if request.user.is_authenticated:
        user_data = len(editProfile.objects.filter(profile_user=request.user))
        if doc>0:
            doc_present=True
            
    
    if request.user.is_authenticated:
        user_data = editProfile.objects.get(profile_user=request.user)
        mental_count = user_data.count_mentalH
        approved = user_data.approval
        return render(request,'resources.html',{"blogs":blogs,'friend_count':friend_count,'mental_count':mental_count,'approved':approved,'doc_present':doc_present})
    else:
        return render(request,'resources.html',{"blogs":blogs,'friend_count':friend_count})


def post(request):
    if request.method=='POST':
        author = request.user
        title = request.POST['content-title']
        body = request.POST['content-area']
        specialkey = editProfile.objects.get(profile_user= request.user)
        key = specialkey.key
        vectorizer = pickle.load(open('E:/Anonimo-ML-collo/vectorizer.pickle','rb'))
        print("-------------------------------")
        examples = body
        a = preprocess(examples)
        example_counts = vectorizer.transform([a])
        model = pickle.load(open('E:/Anonimo-ML-collo/model1.pkl','rb'))
        prediction=model.predict(example_counts) 
        print(prediction)


        if prediction[0]=="suicide":
            mentalH = "suicide"
            print("Inside IF")
            userState = editProfile.objects.get(profile_user= request.user)
            user_mentalH_count = userState.count_mentalH
            user_mentalH_count+=1
            userState.count_mentalH= user_mentalH_count
            userState.save()

            

        elif prediction[0]=="non-suicide":
            mentalH = "non-suicide"

        
        ins = Post(author=author, title=title,body=body,slug=key,mentalH=mentalH)
        ins.save()
        print("Data has been successfully saved!")
        #return render(request,'anonym.html',{'account_bal':account_bal})
    return render(request,'post.html')

def handlelogin(request):
    flag = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username , password=password)
        if user is not None:
            auth.login(request,user)
            user_data = len(Doctor.objects.filter(doctor_username=request.user))
            if user_data>0:
                doc_details = Doctor.objects.get(doctor_username=request.user)
                if doc_details.doc_bio:
                    return redirect('/')
                else:
                    return redirect('/doctorprofile')
            flag = True
            alreadyexisting = len(editProfile.objects.filter(profile_user = request.user))
            if alreadyexisting>0:

                return redirect("/")
            else:
                return redirect("/complete")
        else:
            flag = False
            return render(request, 'login.html', {'flag':flag})
    else:
        return render(request, 'login.html')

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            
        
            user = User.objects.create_user(username= username, password=password, email=email)
            user.save()
            print("User entered into the database successfully!")
            args = {'user': request.user}
            return render(request, 'signup.html',args)
        except IntegrityError:

            flag = True
            print("already exisitng")
         
        #Account creation message
        
            args = {'user': request.user,'flag':flag}
            return render(request, 'signup.html',args)
    else:
        return render(request, 'signup.html')


def settings(request):
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if request.user.is_authenticated:
        user_data = len(editProfile.objects.filter(profile_user=request.user))
        if doc>0:
            doc_present=True
    user_data = editProfile.objects.get(profile_user=request.user) 
    mental_count = user_data.count_mentalH 
    approved = user_data.approval
    allPosts = Post.objects.all()
    allProfiles = editProfile.objects.all()
    allPostU = Post.objects.all().filter(author = request.user)
    posts_counts = allPostU.count()
    allProfiles = editProfile.objects.all().filter(profile_user = request.user)
    user_followers = len(FollowersCount.objects.filter(user=request.user))
    user_following = len(FollowersCount.objects.filter(follower= request.user))
    count = allProfiles.count()
    target_id =""
    if count!=0:
        target_id = allProfiles[0].id

    friend_count = len(FriendRequest.objects.filter(to_user = request.user))

    context = {
        'allPostsU': allPostU,
        'posts_counts': posts_counts,
        'allProfiles':allProfiles,
        'count':count, 
        'target_id':target_id,
        'user_followers': user_followers,
        'user_following': user_following,
        'allPosts': allPosts,
        'allProfiles':allProfiles,
        'friend_count':friend_count,
        'mental_count':mental_count, 
        'approved':approved,
        'doc_present':doc_present
    }
    return render(request, 'settings.html', context)


def complete(request):
    if request.method =="POST":
        user_profile = editProfile()
        user_profile.profile_user = request.user
        user_profile.bio = request.POST.get('bio')
        user_profile.instagram = request.POST.get('instagram')
        user_profile.hobbies = request.POST.get('Hobbies')
        if len(request.FILES)!=0:
            user_profile.image = request.FILES['image']
        user_profile.key = random.randint(111,999)
        user_profile.save()
        return redirect('settings')
    return render(request,'complete.html')


def edit(request,id):
    user_data = editProfile.objects.get(profile_user=request.user)
    mental_count = user_data.count_mentalH
   
    user_profile = editProfile.objects.get(id= id)
    if request.method == "POST":
        if len(request.FILES)!=0:
            if len(user_profile.image) > 0:
                os.remove(user_profile.image.path)
            user_profile.image = request.FILES['image']
        user_profile.bio = request.POST.get('bio')
        user_profile.instagram = request.POST.get('instagram')
        user_profile.hobbies = request.POST.get('Hobbies')
        user_profile.save()
        return redirect('settings')
    friend_count = len(FriendRequest.objects.filter(to_user = request.user))
    context = {'user_profile':user_profile,'friend_count':friend_count,'mental_count':mental_count }
    return render(request, 'edit.html',context) 

def userProfile(request,id):
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
       
    flag = False
    mental_count = 0
    approved = 1
    
    if request.user.is_authenticated:
        user_data = len(editProfile.objects.filter(profile_user=request.user))
        if doc>0:
            doc_present=True
        flag = True
        if user_data>0:
            user_data = editProfile.objects.get(profile_user=request.user)
            mental_count = user_data.count_mentalH
            approved = user_data.approval
        current_user = editProfile.objects.get(id= id)
        current_user_pro = current_user.profile_user
        current_user_posts = Post.objects.all().filter(author=current_user_pro)
        current_user = editProfile.objects.get(id= id)
        current_user_pro = current_user.profile_user
        CAllposts = Post.objects.all().filter(author=current_user_pro)
        buttonclick = "true"
        
        user_key = current_user.key
        posts_counts = current_user_posts.count()
        
        current_user_pro_id = current_user_pro.id
        logged_in_user = request.user.username
        user_followers = len(FollowersCount.objects.filter(user=current_user_pro))
        user_following = len(FollowersCount.objects.filter(follower= current_user_pro))
        user_followers0 = FollowersCount.objects.filter(user = current_user_pro)
        friend_count = len(FriendRequest.objects.filter(to_user = request.user))
        print(user_followers0)
        user_followers1= []
        for i in user_followers0:
            user_followers0 = i.follower
            user_followers1.append(user_followers0)
        if logged_in_user in user_followers1:
            follow_button_value = 'unfollow'
        else:
            follow_button_value = 'follow'

        allfollowers = FollowersCount.objects.all().filter(user = request.user)
        friendlist = []
        for follower in allfollowers:
            Friend = User.objects.get(username = follower.follower)
            friendlist.append(Friend)
        
        flagrequest=True

        allRequests = len(FriendRequest.objects.filter(from_user=request.user,to_user=current_user_pro))
        print(allRequests)
        if allRequests>=1:
            flagrequest = False
        
    context = {
        'current_user': current_user,
        'current_user_posts':current_user_posts,
        'posts_counts':posts_counts, 
        'current_user':current_user,
        'current_user_pro':current_user_pro,
        'user_followers': user_followers,
        'user_following': user_following,
        'follow_button_value' : follow_button_value,
        'current_user_pro_id':current_user_pro_id,
        'buttonclick':buttonclick,
        'friend_count':friend_count,
        'CAllposts':CAllposts,
        'flag':flag,
        'friendlist':friendlist,
        'user_key':user_key,
        'flagrequest':flagrequest,
        'mental_count':mental_count,
        'approved':approved,
        'doc_present':doc_present
        
        }


    return render(request, 'userprofile.html', context )
  
def followers_count(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.POST['user']
        follower = request.POST['follower']
        if value == 'follow':
            followers_cnt = FriendRequest.objects.create(from_user=follower, to_user= user)
            followers_cnt.save()
        elif value == 'unfriend':
            followercnt = FollowersCount.objects.get(follower = follower, user = user)
            followercnt2 = FollowersCount.objects.get(follower=user,user = follower)
            followercnt.delete()
            followercnt2.delete()
        else:
            followers_cnt = FriendRequest.objects.get(from_user=follower,to_user= user)
            followers_cnt.delete()
        return redirect('anonym')

def buycoins(request):
        acc_bal = Bank.objects.get(profile_user=request.user)
        account_bal = acc_bal.account_bal
        amount1= 100000
        amount2 = 200000
        amount = 50000
        order_currency = 'INR'
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        payment = client.order.create({'amount':amount, 'currency':'INR'}) 
        payment1 = client.order.create({'amount':amount1, 'currency':'INR'}) 
        payment2 = client.order.create({'amount':amount2, 'currency':'INR'}) 
        return render(request, 'buycoins.html', {'payment':payment,'amount1':amount1, 'amount2':amount2, 'payment1':payment1, 'payment2':payment2,'account_bal':account_bal})

@csrf_exempt
def success(request):
    return HttpResponse("successfully paid !!")

def requestpage(request):
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if request.user.is_authenticated:
        user_data = len(editProfile.objects.filter(profile_user=request.user))
        if doc>0:
            doc_present=True
        user_data = editProfile.objects.get(profile_user=request.user)
        mental_count = user_data.count_mentalH
        approved = user_data.approval
    fr = FriendRequest.objects.filter(to_user= request.user)
    friend_count = len(FriendRequest.objects.filter(to_user = request.user))
    print(friend_count)
    
    return render(request, 'requestpage.html', {'fr':fr,'friend_count':friend_count,'doc_present':doc_present,'mental_count':mental_count,'approved':approved})

def accept_request(request):
    if request.method == 'POST':
        value = request.POST['value']
        print(value)
        user = request.POST['user']
        print(user)
        follower = request.POST['follower']
        if value == 'accept':
            print("inside if")
            followers_cnt = FollowersCount.objects.create(follower=user, user= follower)
            follower_cnt2 = FollowersCount.objects.create(follower=follower, user = user)
            followers_cnt.save()
            follower_cnt2.save()
            requestcnt = FriendRequest.objects.get(from_user=user,to_user= follower)
            requestcnt.delete()
            print("Suceesfully saved!")
        elif value=='decline':
            requestcnt = FriendRequest.objects.get(from_user=user,to_user= follower)
            requestcnt.delete()
        return redirect('request')
        

def unfriend(request):
    if request.method =="POST":
        value = request.POST['value']
        user = request.POST['user']
        follower = request.POST['follower']
        followercnt = FollowersCount.objects.get(follower = user, user = follower)
        followercnt2 = FollowersCount.objects.get(follower=follower ,user=user)
        followercnt2.delete()
        followercnt.delete()
   
    return redirect('anonym')

def chatlist(request):
    allfollowers = FollowersCount.objects.all().filter(user = request.user)
    allProfiles = editProfile.objects.all()
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if request.user.is_authenticated:
        user_data = len(editProfile.objects.filter(profile_user=request.user))
        if doc>0:
            doc_present=True
        user_data = editProfile.objects.get(profile_user=request.user)
        mental_count = user_data.count_mentalH
        approved = user_data.approval
    user_names_followers = []
    for name in allfollowers:
        current_user = User.objects.get(username = name.follower)
        user_names_followers.append(current_user)


    return render(request, 'chatlist.html',{'allfollowers': allfollowers,'allProfiles':allProfiles,'user_names_followers':user_names_followers,'doc_present':doc_present,'mental_count':mental_count})

def agreement(request):
    user_data = editProfile.objects.get(profile_user=request.user)
    mental_count = user_data.count_mentalH
    return render(request,'agreement.html',{'mental_count':mental_count})

def approveDoc(request):
    if request.method == "POST":
        user_data = editProfile.objects.get(profile_user=request.user)
        user_data.approval = 1
        user_data.save()

        return redirect("/")
  
def doctorsignup(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            doctor = request.POST['doctor']
            doctorobj = Doctor()
            doctorobj.doctor_username = username
            doctorobj.doctype = doctor
            doctorobj.save()
            user = User.objects.create_user(username= username, password=password, email=email)
            user.save()
            print("User entered into the database successfully!")
            args = {'user': request.user}
            return render(request, 'signup.html',args)
        except IntegrityError:

            flag = True
            print("already exisitng")
         
        #Account creation message
        
            args = {'user': request.user,'flag':flag}
            return render(request, 'doctorsignup.html',args)
    else:
        return render(request, 'doctorsignup.html')

def doctorprofile(request):
    if request.method =="POST":
        doc = Doctor.objects.get(doctor_username=request.user) 
        doc.doc_bio = request.POST.get('bio')
        doc.doc_type = request.POST.get('doctype')
        doc.doc_exp = request.POST.get('exp')
        doc.doc_qualification = request.POST.get('qualification')
        if len(request.FILES)!=0:
            doc.doc_image = request.FILES['image']
        doc.save()
        return redirect('/')
    return render(request, 'doctorprofile.html') 



def doctorsetting(request):
    docData = Doctor.objects.filter(doctor_username=request.user) 
    doc = len(Doctor.objects.filter(doctor_username=request.user))
    doc_present = False
    if doc>0:
        doc_present=True
    context = {
        'docData': docData, 
        'doc_present':doc_present
    }
    return render(request, 'doctorsetting.html', context)


def help(request,id):
    current_user = editProfile.objects.get(id= id)
    current_user_pro = current_user.profile_user
    current_user_posts = Post.objects.all().filter(author=current_user_pro)
    current_user = editProfile.objects.get(id= id)
    current_user_pro = current_user.profile_user
    CAllposts = Post.objects.all().filter(author=current_user_pro)
    buttonclick = "true"
    target_id = current_user.id
    user_key = current_user.key
    posts_counts = current_user_posts.count()
    session_started=False
    session_details = len(Session.objects.filter(patient_username = current_user_pro))
    print(session_details)
    if session_details>0:
        session_started = True
    current_user_pro_id = current_user_pro.id

    context = {
        'current_user': current_user,
        'current_user_posts':current_user_posts,
        'posts_counts':posts_counts, 
        'current_user':current_user,
        'current_user_pro':current_user_pro,
        'current_user_pro_id':current_user_pro_id,
        'buttonclick':buttonclick,
        'CAllposts':CAllposts,
        'user_key':user_key,
        'target_id':target_id,
        'session_started':session_started
        }


    return render(request,'docHelp.html',context)
