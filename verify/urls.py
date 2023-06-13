from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("login/", views.UserLogin.as_view(), name='login'),
    path("verify/", views.UserVerification.as_view(), name="verify"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("retrieve/", views.PostRetrieveView.as_view(), name="retrieve"),
    path("update/<slug:slug>/", views.PostUpdateView.as_view(), name="update"),
    path("delete/<slug:slug>/", views.PostDeleteView.as_view(), name="delete"),
]