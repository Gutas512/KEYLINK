from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from Keylink.models import *
from Keylink.forms import *


def login_funcionario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Procurar o funcionário pelo nome de usuário
            funcionario = Funcionario.objects.get(usuario_funcionario=username)

            # Verificar se a senha fornecida corresponde à senha do funcionário
            if check_password(password, funcionario.senha):  # Verificação da senha hash
                # Armazenar o ID do funcionário na sessão
                request.session['funcionario_id'] = funcionario.id
                return redirect('index')  # Redirecionar para a página inicial após o login
            else:
                return render(request, 'login.html', {'error': 'Senha incorreta'})

        except Funcionario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuário não encontrado'})

    return render(request, 'login.html')

def logout_funcionario(request):
    logout(request)  # Realiza o logout do usuário
    return redirect('login')

# views.py
def index(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')

    funcionario = Funcionario.objects.get(id=request.session['funcionario_id'])

    return render(request, 'index.html', {'funcionario': funcionario})

def listar_funcionarios(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')  # Se não houver o ID do funcionário na sessão, redireciona para o login

    # Recuperar o funcionário logado
    funcionario_logado = Funcionario.objects.get(id=request.session['funcionario_id'])

    # Recuperar a lista de todos os funcionários
    funcionarios = Funcionario.objects.all()

    # Passar os dados para o template
    return render(request, 'listar_funcionarios.html', {
        'funcionario': funcionario_logado,
        'funcionarios': funcionarios
    })


# Adicionar um novo funcionário
def adicionar_funcionario(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_funcionarios')
    else:
        form = FuncionarioForm()
    return render(request, 'funcionarios/adicionar.html', {'form': form})

# Editar um funcionário
def editar_funcionario(request, id):
    if 'funcionario_id' not in request.session:
        return redirect('login')
    funcionario = get_object_or_404(Funcionario, id=id)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('listar_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'funcionarios/editar.html', {'form': form})


# Excluir um funcionário
def excluir_funcionario(request, id):
    if 'funcionario_id' not in request.session:
        return redirect('login')
    funcionario = get_object_or_404(Funcionario, id=id)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('listar_funcionarios')
    return render(request, 'funcionarios/excluir.html', {'funcionario': funcionario})

def listar_salas(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')
    return render(request, 'listar_salas.html')

def listar_registros(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')
    return render(request, 'listar_registros.html')