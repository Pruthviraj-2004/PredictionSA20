from django.contrib import admin
from .models import UserInfo,Match,Submissions
class SubmissionsAdmin(admin.ModelAdmin):
    list_display = ('susername', 'smatch_id', 'predicted_team')
    ordering = ('-smatch_id',)

admin.site.register(UserInfo)
admin.site.register(Match)
admin.site.register(Submissions, SubmissionsAdmin)
