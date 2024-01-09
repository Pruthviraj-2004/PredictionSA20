from django.contrib import admin
from .models import UserInfo,Match,Submissions
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Match)
admin.site.register(Submissions)