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

from django.contrib.auth import views as auth_views
from django import forms
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import CustomPasswordResetForm 

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse


def home(request):
    num_users = UserInfo.objects.count()
    return render(request,"predictsa20/home.html",{"num_users":num_users})

def fixtures(request):
    match_list = Match.objects.all().filter(match_status=0).order_by('match_date')
    
    p = Paginator(match_list,5)
    page = request.GET.get('page')
    matches = p.get_page(page)
    nums = "a" * matches.paginator.num_pages
    return render(request,"predictsa20/fixtures.html",{'match_list':match_list,'matches':matches,'nums':nums})

def leaderboard(request):
    user_list = UserInfo.objects.all().order_by('-score','user__username')
    
    for rank, user_info in enumerate(user_list, start=1):
        user_info.rank = rank

    
    p = Paginator(user_list,10)
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
                return redirect('predict')#redirect to predict
        else:
            messages.error(request, "Submissions are closed as the match has started.")
            return redirect('home')
    else:
        return render(request, 'predictsa20/predict.html', {'match_list': match_list})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logged Out Successfully!! "))
    return redirect('home')

# def register_user(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             pass1 = form.cleaned_data['password1']
#             user = authenticate(username=username, password=pass1)
#             login(request, user)
#             messages.success(request, ("Registration Successful"))
#             return redirect('home')
        
#     else:
#         form = RegisterUserForm()

#     return render(request, 'predictsa20/register_user.html', {'form':form})

def register_user2(request):
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

    return render(request, 'predictsa20/register_user2.html', {'form':form})

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


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm  
    template_name = 'predictsa20/password_reset_form.html'  # Specify your template name
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        # Check if the entered username and email match a user in the database
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']

        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            messages.error(self.request, 'Invalid username or email.')
            return HttpResponseRedirect(self.get_success_url())

        # If the user is found, proceed with sending the password reset email
        form.save(request=self.request)

        # Add your custom logic here if needed

        return super().form_valid(form)
    
#unwanted
# def register_user4(request):
#     # form=RegisterUserForm()
#     if request.method=='POST':
#         form=RegisterUserForm(request.POST)
    
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
            
#             current_site = get_current_site(request)  
#             mail_subject = 'Activation link has been sent to your email id'   
#             message = render_to_string('acc_active_email.html', {  
#                     'user': user,  
#                     'domain': current_site.domain,  
#                     'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
#                     'token':account_activation_token.make_token(user),  
#                 })  
#             to_email = form.cleaned_data.get('email')  
#             email = EmailMessage(  
#                             mail_subject, message, to=[to_email]  
#                 )  
#             email.send()  
#             messages.success(request,"Please confirm your email address to complete the registration") 
#             return redirect('home')
    
#         else:  
        
#             form = RegisterUserForm()  
#             return render(request, 'predictsa20/register_user2.html', {'form': form})
#     return render(request, 'predictsa20/register_user2.html')

def user_input_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if not username:
            messages.warning(request, 'Please enter a valid username.')
            return redirect('user_input_form')

        # Redirect to user_submissions with the entered username
        return redirect('user_submissions', username=username)

    return render(request, 'predictsa20/user_input_form.html')

def user_submissions(request, username):
    # Fetch all submissions for the specified user
    user_submissions = Submissions.objects.filter(susername=username).order_by('smatch_id')

    # Fetch related match details for each submission
    submission_details = []
    for submission in user_submissions:
        match = Match.objects.get(match_id=submission.smatch_id)
        submission_details.append({
            'smatch_id': submission.smatch_id,
            'match_team_A': match.match_team_A,
            'match_team_B': match.match_team_B,
            'predicted_team': submission.predicted_team,
            'match_winner': match.match_winner,
        })

    context = {
        'username': username,
        'submissions': submission_details,
    }

    return render(request, 'predictsa20/user_submissions.html', context)

