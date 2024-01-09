from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, MatchForm
from .models import Submissions, UserInfo, Match
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from datetime import datetime, timedelta
from pytz import timezone


def home(request):
    return render(request,"predictsa20/home.html",{})

def fixtures(request):
    match_list = Match.objects.all().filter(match_status=0).order_by('match_date')
    
    p = Paginator(match_list,5)
    page = request.GET.get('page')
    matches = p.get_page(page)
    nums = "a" * matches.paginator.num_pages
    return render(request,"predictsa20/fixtures.html",{'match_list':match_list,'matches':matches,'nums':nums})

def leaderboard(request):
    user_list = UserInfo.objects.all().order_by('-score')
    
    p = Paginator(user_list,5)
    page = request.GET.get('page')
    users = p.get_page(page)
    nums = "a" * users.paginator.num_pages
    return render(request,'predictsa20/leaderboard.html',{'user_list':user_list,'users':users,'nums':nums})

def match_registration(request):
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()

            messages.success(request, "Match submitted successfully!")
            return redirect('home')  # Redirect to the home page

        else:
            messages.error(request, "Invalid form details. Please check and try again.")
            return redirect('home')  # Redirect to the home page with an error message

    else:
        form = MatchForm()

    return render(request, 'predictsa20/match_registration.html', {'form': form})

def update_match(request,match_id):
    venue = Match.objects.get(pk=match_id)
    # venue = get_object_or_404(Match, pk=match_id)
    form = MatchForm(request.POST or None, instance = venue)

    if form.is_valid():
        form.save()

        score_update3(request,match_id)

        messages.success(request, ("Match Details and Score Updated!!"))
        return redirect('home')

    return render(request, 'predictsa20/update_match.html', {'venue':venue, 'form':form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(request, username=username, password=pass1)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Only Admin can Login!!"))
            return redirect('home')
    else:
        return render(request, 'predictsa20/login.html', {})

IST = timezone('Asia/Kolkata')

def predict(request):
    match_list = Match.objects.all().filter(match_status=0).order_by('match_date')

    current_time = datetime.now(IST)

    if request.method == "POST":
        smatch_id = request.POST.get('match_id')
        match = Match.objects.get(pk=smatch_id)

        # Extract the time from the datetime field
        match_start_time = match.match_start_time

        MATCH_START_TIME = IST.localize(datetime.combine(match.match_date, match_start_time))

        # Check if submissions are allowed based on the match date and time
        if current_time < MATCH_START_TIME:
            username = request.POST['username']
            pass1 = request.POST['pass1']
            
            predicted_team = request.POST.get('predicted_team')
            
            user = authenticate(request, username=username, password=pass1)

            if user is not None:            
                existing_submission = Submissions.objects.filter(susername=username, smatch_id=smatch_id).first()

                if existing_submission:
                    existing_submission.predicted_team = predicted_team
                    existing_submission.save()
                else:
                    submission = Submissions(susername=username, smatch_id=smatch_id, predicted_team=predicted_team)
                    submission.save()

                messages.success(request, "Submission successful.")
                return redirect('leaderboard')
            else:
                messages.error(request, "There is an error while logging in.")
                return redirect('home')
        else:
            messages.error(request, "Submissions are closed as the match has started.")
            return redirect('home')
    else:
        return render(request, 'predictsa20/predict.html', {'match_list': match_list})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logged Out Successfully!! "))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            pass1 = form.cleaned_data['password1']
            user = authenticate(username=username, password=pass1)
            login(request, user)
            messages.success(request, ("Registration Successful"))
            return redirect('home')
        
    else:
        form = RegisterUserForm()

    return render(request, 'predictsa20/register_user.html', {'form':form})

class GetTeamsForMatch(View):
    def get(self, request, match_id):
        try:
            match = Match.objects.get(match_id=match_id)
            teams = [match.match_team_A, match.match_team_B]
            return JsonResponse({'teams': teams})
        except Match.DoesNotExist:
            return JsonResponse({'error': 'Match not found'}, status=404)

def score_update3(request,match_id):
    matches1 = Match.objects.all().filter(match_id = match_id).first()

    winner_team = matches1.match_winner if matches1 else None

    users_list = Submissions.objects.filter(smatch_id=match_id, predicted_team=winner_team)
    
    for each_user in users_list:
        un = each_user.susername
        ur= UserInfo.objects.all().filter(user__username = un).first()
        ur.score += 1
        ur.save()
        
    return render(request, 'predictsa20/score_update.html', {'matches1':matches1,'teama':winner_team,'users_list':users_list})
