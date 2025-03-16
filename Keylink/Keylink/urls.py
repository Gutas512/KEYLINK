from django.urls import path
from website import views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),

    path('login/', views.login_funcionario, name='login'),
    path('logout/', views.logout_funcionario, name='logout'),

    path('', views.index, name='index'),

    path('funcionarios/', views.listar_funcionarios, name='listar_funcionarios'),

    path('salas/', views.listar_salas, name='listar_salas'),

    path('registros/', views.listar_registros, name='listar_registros'),

]
