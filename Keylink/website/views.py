from pyexpat.errors import messages
from django.shortcuts import render, redirect
from Keylink.models import *
from Keylink.forms import *

def login_funcionario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            funcionario = Funcionario.objects.get(usuario_funcionario=username, senha=password)
            return redirect('index')  # ou qualquer página desejada após login
        except Funcionario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})

    return render(request, 'login.html')

# views.py (continuação)
def logout_funcionario(request):
    request.session.flush()
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('login')

# views.py
def index(request):

    return render(request, 'index.html')

def listar_funcionarios(request):
    return render(request, 'listar_funcionarios.html')

def listar_salas(request):
    return render(request, 'listar_salas.html')

def listar_registros(request):
    return render(request, 'listar_registros.html')