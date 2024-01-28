from users import views as users_views
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home ,name="blog-home"),
    path('about', views.about ,name="blog-about"),
    path('register/', users_views.register ,name="register"),


]
