from django.urls import path
from website import views
from website.views import primeiro_acesso
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.index, name='index'),

    path('funcionarios/', views.listar_funcionarios, name='listar_funcionarios'),
    path('funcionarios/adicionar/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('funcionarios/editar/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/excluir/<int:id>/', views.excluir_funcionario, name='excluir_funcionario'),

    path('chaves/', views.listar_chaves, name='listar_chaves'),
    path('chaves/adicionar/', views.adicionar_chave, name='adicionar_chave'),
    path('chaves/editar/<int:chave_id>/', views.editar_chave, name='editar_chave'),
    path('chaves/excluir/<int:chave_id>/', views.excluir_chave, name='excluir_chave'),
    path('chave/utilizar/<int:chave_id>/', views.utilizar_chave, name='utilizar_chave'),
    path('chave/devolver/<int:chave_id>/', views.devolver_chave, name='devolver_chave'),
    path('chave/indisponivel/', views.chave_indisponivel, name='chave_indisponivel'),
    path('sem-permissao/', views.sem_permissao, name='sem_permissao'),

    path('acesso-negado/', views.acesso_negado, name='acesso_negado'),

    path('primeiro-acesso/', primeiro_acesso, name='primeiro_acesso'),

    path('registros/', views.listar_registros, name='listar_registros'),
]
