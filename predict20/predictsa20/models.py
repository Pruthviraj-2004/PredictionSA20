from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserInfo(models.Model):
    # user_ids = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField('Score', default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_info(sender, instance, **kwargs):
    instance.userinfo.save()
    
class Match(models.Model):
    match_id = models.PositiveSmallIntegerField(primary_key=True)
    match_date = models.DateField('Match Date')
    match_start_time = models.TimeField('Match Start Time',default='21:00:00')
    match_team_A = models.CharField("Team A",max_length=30)
    match_team_B = models.CharField("Team B",max_length=30)
    match_status = models.SmallIntegerField("Match Status",default=0)
    match_winner = models.CharField("Winner",default=None,max_length=30)

    def __str__(self):
        return f"{self.match_team_A} V/S {self.match_team_B}"
    
class Submissions(models.Model):
    susername = models.CharField("Username",max_length=100)
    smatch_id = models.PositiveSmallIntegerField("Match ID")
    predicted_team = models.CharField("Predicted Team",max_length=20)

    def __str__(self):
        return f"{self.susername} team {self.smatch_id}  {self.predicted_team}"
 
