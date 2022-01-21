from blogapp.models import Badges
from home.models import editProfile,FriendRequest, FollowersCount
from django.shortcuts import render
from blogapp.models import Post,Like
from django.shortcuts import redirect
from blogapp.models import BlogComment, Report
from blogapp.templatetags import extras
from django.contrib.auth.decorators import login_required
from home.models import Bank
from django.contrib.auth.models import User,auth
import random
# Create your views here.



def anonymhome(request):
 
    friend_count = len(FriendRequest.objects.filter(to_user = request.user))
    allfollowers = FollowersCount.objects.all().filter(user = request.user)
    allPosts = Post.objects.all()
    friendlist = []
    for follower in allfollowers:
        Friend = User.objects.get(username = follower.follower)
        friendlist.append(Friend)

    
    

    allProfiles = editProfile.objects.all()
    allBadges = Badges.objects.all()
    if request.user.is_authenticated:
        acc_bal = Bank.objects.get(profile_user=request.user)
        account_bal = acc_bal.account_bal

        context = {'allPosts': allPosts, 'allProfiles':allProfiles, 'allBadges':allBadges,'friend_count':friend_count, 'account_bal':account_bal,'allfollowers':allfollowers,'friendlist':friendlist}
        return render(request, 'anonym.html', context)
    else:
        context = {'allPosts': allPosts, 'allProfiles':allProfiles, 'allBadges':allBadges,'friend_count':friend_count,}
        return render(request, 'anonym.html', context)




@login_required
def like_post(request):
    user = request.user
    if request.method=='POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(pk = post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like,created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value=='like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
        return redirect('anonym')



def blogPost(request,my_id):
    allfollowers = FollowersCount.objects.all().filter(user = request.user)
    friendlist = []
    for follower in allfollowers:
        Friend = User.objects.get(username = follower.follower)
        friendlist.append(Friend)

    post = Post.objects.filter(sno=my_id).first()
    allPosts = Post.objects.all()
    comments= BlogComment.objects.filter(post=post, parent=None)
    allProfiles = editProfile.objects.all()
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context={'post':post, 'comments': comments, 'allProfiles':allProfiles, 'user': request.user, 'replyDict': replyDict,'friendlist':friendlist,'allPosts':allPosts}
    return render(request, 'blogPost.html', context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
    
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
         
        
    return redirect("anonym")


def badges(request):
    if request.method == "POST":
        title = request.POST.get('title')
        print("Actual Title", title)
        cost = int(request.POST.get('value'))
        print("Cost of Button", cost)
        badges = len(Badges.objects.filter(post = title))
        print("Total number of instance:",badges)
        if badges!=0:
            print("---INSIDE IF----")
            true_badges = Badges.objects.get(post= title)
            gold_count = true_badges.gold
            platinum_count = true_badges.platinum
            if cost == 100:
                gold_count = gold_count+1
                print(gold_count)
                true_badges.gold = gold_count

            elif cost == 200:
                platinum_count = platinum_count+1
                true_badges.platinum = platinum_count

            userprofile = Bank.objects.get(profile_user=request.user)
            acc_bal = userprofile.account_bal
            if acc_bal<int(cost):
                print("Insufficient Funds")
            else:
                acc_bal = acc_bal - int(cost)
                print("Remaining Balance: " ,acc_bal)
                userprofile.account_bal = acc_bal
                userprofile.save()
                print("Transaction Successful!")
                true_badges.save()
                print("Badges Saved Successfully!")

        else:
            print("-------INSIDE ELSE-----------")
            gold_count =0
            platinum_count = 0
            if cost == 100:
                gold_count = gold_count+1
                print(gold_count)
            elif cost == 200:
                platinum_count = platinum_count+1
            new_badges = Badges.objects.create(post = title , gold = gold_count, platinum=platinum_count)
            userprofile = Bank.objects.get(profile_user=request.user)
            acc_bal = userprofile.account_bal
            if acc_bal<int(cost):
                print("Insufficient Funds")
            else:
                acc_bal = acc_bal - int(cost)
                print("Remaining Balance: " ,acc_bal)
                userprofile.account_bal = acc_bal
                userprofile.save()
                print("Transaction Successful!")
                new_badges.save()
                print("Badges Saved Successfully!")
                
        
    return redirect('anonym')
            

def report(request):
    if request.method=="POST":
        title = request.POST.get('title')
        content = request.POST.get('body')
        value = request.POST.get('value')
        ins = Report(post_title=title, post_content=content,reason=value)
        ins.save()
        return redirect('anonym')


