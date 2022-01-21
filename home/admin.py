from django.contrib import admin

from home.models import SignUp,Resources,editProfile,FollowersCount,FriendRequest,Bank
# Register your models here.

admin.site.register(SignUp)
admin.site.register(Resources)
admin.site.register(editProfile)
admin.site.register(FriendRequest)
admin.site.register(FollowersCount)
admin.site.register(Bank)