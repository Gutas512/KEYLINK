from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from Keylink.models import *
from Keylink.forms import *
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages


def login_funcionario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autenticação usando o backend personalizado
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciais inválidas')

    return render(request, 'login.html')


@login_required
def index(request):
    # Agora request.user será uma instância de Funcionario com todos os atributos necessários
    return render(request, 'index.html', {'funcionario': request.user})

def logout_funcionario(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    # O usuário logado é o próprio Funcionario
    funcionario = request.user
    return render(request, 'index.html', {'funcionario': funcionario})


@login_required
def listar_funcionarios(request):
    funcionario_logado = request.user
    funcionarios = Funcionario.objects.all()
    return render(request, 'listar_funcionarios.html', {
        'funcionario': funcionario_logado,
        'funcionarios': funcionarios
    })


@login_required
def adicionar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save(commit=False)
            funcionario.set_password(form.cleaned_data['senha'])  # Criptografa a senha
            funcionario.save()
            messages.success(request, 'Funcionário cadastrado com sucesso!')
            return redirect('listar_funcionarios')
    else:
        form = FuncionarioForm()

    return render(request, 'funcionarios/adicionar.html', {'form': form})


@login_required
def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id_funcionario=id)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('listar_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'funcionarios/editar.html', {'form': form})


@login_required
def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id_funcionario=id)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('listar_funcionarios')
    return render(request, 'funcionarios/excluir.html', {'funcionario': funcionario})


@login_required
def listar_chaves(request):
    funcionario = request.user
    chaves = Chave.objects.all()
    return render(request, 'listar_chaves.html', {'chaves': chaves, 'funcionario': funcionario})


@login_required
def adicionar_chave(request):
    if request.method == 'POST':
        form = ChaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_chaves')
    else:
        form = ChaveForm()
    return render(request, 'chaves/adicionar.html', {'form': form})


@login_required
def editar_chave(request, id):
    chave = Chave.objects.get(id_chaves=id)
    if request.method == 'POST':
        form = ChaveForm(request.POST, instance=chave)
        if form.is_valid():
            form.save()
            return redirect('listar_chaves')
    else:
        form = ChaveForm(instance=chave)
    return render(request, 'chaves/editar.html', {'form': form, 'chave': chave})


@login_required
def utilizar_chave(request, chave_id):
    funcionario = request.user
    chave = get_object_or_404(Chave, id_chaves=chave_id)

    if chave.disponivel:
        chave.usuario = funcionario
        chave.disponivel = False
        chave.save()

        timestamp = int(timezone.now().timestamp())
        registro_id = f"SAIDA-{timestamp}-{chave_id}-{funcionario.id_funcionario}"

        RegistroSaida.objects.create(
            id_registro=registro_id,
            chaves=chave,
            funcionario=funcionario,
            registro_saida_horario=timezone.now()
        )

        messages.success(request, f'Chave {chave.numero_chave} utilizada com sucesso!')
    else:
        messages.error(request, 'Esta chave já está em uso!')

    return redirect('listar_chaves')


@login_required
def devolver_chave(request, chave_id):
    funcionario = request.user
    chave = get_object_or_404(Chave, id_chaves=chave_id)

    if chave.usuario and chave.usuario.id_funcionario == funcionario.id_funcionario:
        registro_saida = RegistroSaida.objects.filter(
            chaves=chave,
            funcionario=funcionario
        ).order_by('-registro_saida_horario').first()

        if registro_saida:
            RegistroEntrada.objects.create(
                registro_saida=registro_saida,
                chaves=chave,
                funcionario=funcionario,
                registro_entrada_horario=timezone.now()
            )

            chave.usuario = None
            chave.disponivel = True
            chave.save()

            messages.success(request, f'Chave {chave.numero_chave} devolvida com sucesso!')
        else:
            messages.error(request, 'Registro de saída não encontrado para esta chave!')
    else:
        messages.error(request, 'Esta chave não foi emprestada para você!')

    return redirect('listar_chaves')


def chave_nao_emprestada(request):
    return render(request, 'chave_nao_emprestada.html')


def chave_indisponivel(request):
    return render(request, 'chave_indisponivel.html')


def sem_permissao(request):
    return render(request, 'sem_permissao.html')


@login_required
def excluir_chave(request, id):
    chave = Chave.objects.get(id_chaves=id)
    if request.method == 'POST':
        chave.delete()
        return redirect('listar_chaves')
    return render(request, 'chaves/excluir.html', {'chave': chave})


@login_required
def listar_registros(request):
    funcionario = request.user
    registros_saida = RegistroSaida.objects.all().order_by('-registro_saida_horario')
    registros_entrada = RegistroEntrada.objects.all().order_by('-registro_entrada_horario')

    return render(request, 'listar_registros.html', {
        'registros_saida': registros_saida,
        'registros_entrada': registros_entrada,
        'funcionario': funcionario
    })