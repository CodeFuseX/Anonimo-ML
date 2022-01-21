from django.contrib import admin
from blogapp.models import Post,Like,BlogComment,Badges,Report
# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(BlogComment)
admin.site.register(Badges)
admin.site.register(Report)
