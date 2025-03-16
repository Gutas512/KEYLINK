from django.urls import path
from website import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
]
