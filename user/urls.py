from django.urls import path

from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from user.views import CreateUserView,UserViewPrivate,CustomTokenObtainParirView, LogoutView, AdimView

urlpatterns =[
    path('', csrf_exempt(CreateUserView.as_view())),
    path("token/",CustomTokenObtainParirView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
    path("edite/",UserViewPrivate.as_view()),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin/", AdimView.as_view(), name="user-detail"),
    path("admin/<id>/", AdimView.as_view(), name="user-detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)



