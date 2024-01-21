from . import views
from django.urls import path,include
from .views import GetTeamsForMatch,CustomPasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("fixture", views.fixtures, name="fixtures"),
    # path("register_user", views.register_user, name="register_user"),
    path("register_user2", views.register_user2, name="register_user2"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("match_registration", views.match_registration, name="match_registration"),
    path("update_match/<match_id>", views.update_match, name="update_match"),
    path("login_user", views.login_user, name="login"),
    path("predict", views.predict, name="predict"),
    path("logout_user", views.logout_user, name="logout"),
    path('get_teams_for_match/<int:match_id>/', GetTeamsForMatch.as_view(), name='get_teams_for_match'),
    path('user_input_form/', views.user_input_form, name='user_input_form'),
    path('user_submissions/<str:username>/', views.user_submissions, name='user_submissions'),


    # path("register_user4", views.register_user4, name="register_user4"),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='predictsa20/password_reset_form.html'), name='password_reset'),
    path('password_reset/', CustomPasswordResetView.as_view(template_name='predictsa20/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='predictsa20/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='predictsa20/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='predictsa20/password_reset_complete.html'), name='password_reset_complete'),

]
