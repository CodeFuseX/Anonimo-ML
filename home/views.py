from anonimo.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from django.views.decorators.csrf import  csrf_exempt
from home.models import Resources,editProfile, FollowersCount,FriendRequest,Bank
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from blogapp.models import Post, Like
import os
import razorpay
import random

# Create your views here.
def home(request):
    friend_count = len(FriendRequest.objects.filter(to_user = request.user))
    if request.user.is_authenticated:
        acc_bal_len = len(Bank.objects.filter(profile_user=request.user))
        if acc_bal_len>0:
            acc_bal = Bank.objects.get(profile_user=request.user)
            account_bal = acc_bal.account_bal
            return render (request, 'home.html',{'friend_count':friend_count,'account_bal':account_bal})
        else:
            acc_create = Bank(profile_user = request.user,account_bal=0)
            acc_create.save()
            account_bal = 0
            return render (request, 'home.html',{'friend_count':friend_count,'account_bal':account_bal})
    return render(request, 'home.html')

def resources(request):
    blogs = Resources.objects.all()
    friend_count = len(FriendRequest.objects.filter(to_user = request.user))
   
    
    if request.user.is_authenticated:
        acc_bal = Bank.objects.get(profile_user=request.user)
        account_bal = acc_bal.account_bal
        return render(request,'resources.html',{"blogs":blogs,'friend_count':friend_count,'account_bal':account_bal})
    else:
        return render(request,'resources.html',{"blogs":blogs,'friend_count':friend_count})


def post(request):
    if request.method=='POST':
        acc_bal = Bank.objects.get(profile_user=request.user)
        account_bal = acc_bal.account_bal
        author = request.user
        title = request.POST['content-title']
        body = request.POST['content-area']
        specialkey = editProfile.objects.get(profile_user= request.user)
        key = specialkey.key

        
        ins = Post(author=author, title=title,body=body,slug=key)
        ins.save()
        print("Data has been successfully saved!")
        return render(request,'post.html',{'account_bal':account_bal})
    return render(request,'post.html')

def handlelogin(request):
    flag = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username= username , password=password)
        if user is not None:
            auth.login(request,user)
            flag = True
            return redirect("/")

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
   
    allPosts = Post.objects.all()
    allProfiles = editProfile.objects.all()
    allPostU = Post.objects.all().filter(author = request.user)
    posts_counts = allPostU.count()
    allProfiles = editProfile.objects.all().filter(profile_user = request.user)
    user_followers = len(FollowersCount.objects.filter(user=request.user))
    user_following = len(FollowersCount.objects.filter(follower= request.user))
    count = allProfiles.count()
    target_id =""
    acc_bal = Bank.objects.get(profile_user=request.user)
    account_bal = acc_bal.account_bal
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
        'account_bal':account_bal,
        
       
        
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
    context = {'user_profile':user_profile,'friend_count':friend_count, }
    return render(request, 'edit.html',context) 

def userProfile(request,id):
    flag = False
    if request.user.is_authenticated:
        flag = True
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
    fr = FriendRequest.objects.filter(to_user= request.user)
    friend_count = len(FriendRequest.objects.filter(to_user = request.user))
    print(friend_count)

    return render(request, 'requestpage.html', {'fr':fr,'friend_count':friend_count})



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
    
    user_names_followers = []
    for name in allfollowers:
        current_user = User.objects.get(username = name.follower)
        user_names_followers.append(current_user)


    return render(request, 'chatlist.html',{'allfollowers': allfollowers,'allProfiles':allProfiles,'user_names_followers':user_names_followers})
