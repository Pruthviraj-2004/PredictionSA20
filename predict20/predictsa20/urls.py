from . import views
from django.urls import path,include
from .views import GetTeamsForMatch

urlpatterns = [
    path("", views.home, name="home"),
    path("fixture", views.fixtures, name="fixtures"),
    path("register_user", views.register_user, name="register_user"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("match_registration", views.match_registration, name="match_registration"),
    path("update_match/<match_id>", views.update_match, name="update_match"),
    path("login_user", views.login_user, name="login"),
    path("predict", views.predict, name="predict"),
    path("logout_user", views.logout_user, name="logout"),
    path('get_teams_for_match/<int:match_id>/', GetTeamsForMatch.as_view(), name='get_teams_for_match'),

]
