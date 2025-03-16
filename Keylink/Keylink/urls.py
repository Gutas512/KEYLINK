from django.urls import path
from website import views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),

    path('login/', views.login_funcionario, name='login'),
    path('logout/', views.logout_funcionario, name='logout'),

    path('', views.index, name='index'),

    path('funcionarios/', views.listar_funcionarios, name='listar_funcionarios'),
    path('funcionarios/adicionar/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('funcionarios/editar/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/excluir/<int:id>/', views.excluir_funcionario, name='excluir_funcionario'),

    path('salas/', views.listar_salas, name='listar_salas'),

    path('registros/', views.listar_registros, name='listar_registros'),

]
