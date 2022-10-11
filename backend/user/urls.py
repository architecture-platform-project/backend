from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView
from django.urls import path, include

from user.views import EmailUniqueCheck

urlpatterns = [
    # path("", include("dj_rest_auth.urls")),
    path("login", LoginView.as_view()),
    path("signup", include("dj_rest_auth.registration.urls")),
    path("uniquecheck/email", EmailUniqueCheck.as_view()),
    path("token/refresh", get_refresh_view().as_view()),
]
