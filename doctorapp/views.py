from django.shortcuts import render
from home.models import Resources,editProfile, FollowersCount,FriendRequest,Bank,Doctor
# Create your views here.
from blogapp.models import Post

def doctorHome(request):
    return render(request,'docHome.html')

def doctoranonym(request):
    allProfiles = editProfile.objects.filter(count_mentalH__gte=3)
    allPosts = Post.objects.filter(mentalH ='suicide')
    #allPosts = len(Post.objects.filter(author=))
    #print(allPosts)
    return render(request,'docAnonym.html',{'allProfiles':allProfiles,'allPosts':allPosts})

