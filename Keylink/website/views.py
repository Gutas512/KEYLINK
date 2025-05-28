from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from Keylink.models import *
from Keylink.forms import *
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import requests
from django.conf import settings

def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.tipo_usuario == 'admin',
        login_url='acesso_negado'
    )(view_func)


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

    if Funcionario.tipo_usuario == 'admin':
        return redirect('painel_admin')
    else:
        return redirect('listar_chaves')

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

@admin_required
@login_required
def listar_funcionarios(request):
    funcionario_logado = request.user
    funcionarios = Funcionario.objects.all()
    return render(request, 'listar_funcionarios.html', {
        'funcionario': funcionario_logado,
        'funcionarios': funcionarios
    })

@admin_required
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

@admin_required
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

@admin_required
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

@admin_required
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

@admin_required
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
        # Enviar comando "Abra" para o ESP8266
        try:
            response = requests.post(
                f'http://{settings.ESP8266_IP}/comando',
                json={'comando': 'Abra', 'chave_id': chave_id},
                timeout=5
            )
            if response.status_code != 200:
                messages.warning(request, 'Chave liberada, mas dispositivo não respondeu')
        except requests.exceptions.RequestException:
            messages.warning(request, 'Chave liberada, mas não foi possível comunicar com o dispositivo')

        chave.usuario = funcionario
        chave.disponivel = False
        chave.save()

        RegistroSaida.objects.create(
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
            # Enviar comando "Feche" para o ESP8266
            try:
                response = requests.post(
                    f'http://{settings.ESP8266_IP}/comando',
                    json={'comando': 'Feche', 'chave_id': chave_id},
                    timeout=5
                )
                if response.status_code != 200:
                    messages.warning(request, 'Chave devolvida, mas dispositivo não respondeu')
            except requests.exceptions.RequestException:
                messages.warning(request, 'Chave devolvida, mas não foi possível comunicar com o dispositivo')

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

@admin_required
@login_required
def excluir_chave(request, chave_id):  # Mude o parâmetro para chave_id
    chave = Chave.objects.get(id_chaves=chave_id)
    if request.method == 'POST':
        chave.delete()
        return redirect('listar_chaves')
    return render(request, 'chaves/excluir.html', {'chave': chave})

@admin_required
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

def acesso_negado(request):
    return render(request, 'acesso_negado.html')


def primeiro_acesso(request):
    if request.method == 'POST':
        # Validação dos dados
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('primeiro_acesso')

        # Verificar se usuário já existe
        if Funcionario.objects.filter(usuario_funcionario=request.POST.get('usuario_funcionario')).exists():
            messages.error(request, 'Nome de usuário já está em uso!')
            return redirect('primeiro_acesso')

        if Funcionario.objects.filter(cpf_funcionario=request.POST.get('cpf_funcionario')).exists():
            messages.error(request, 'CPF já cadastrado!')
            return redirect('primeiro_acesso')

        # Criar novo funcionário
        try:
            novo_funcionario = Funcionario(
                nome_funcionario=request.POST.get('nome_funcionario'),
                usuario_funcionario=request.POST.get('usuario_funcionario'),
                telefone_funcionario=request.POST.get('telefone_funcionario'),
                endereco_funcionario=request.POST.get('endereco_funcionario'),
                funcao_funcionario=request.POST.get('funcao_funcionario'),
                cpf_funcionario=request.POST.get('cpf_funcionario'),
                tipo_funcionario=request.POST.get('tipo_funcionario'),
                tipo_usuario='usuario',  # Sempre usuário comum
                is_active=True,
                is_staff=False,
                is_superuser=False
            )

            # Criptografar senha
            novo_funcionario.senha = make_password(senha)
            novo_funcionario.save()

            messages.success(request, 'Cadastro realizado com sucesso! Faça login para acessar o sistema.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
            return redirect('primeiro_acesso')

    return render(request, 'primeiro_acesso.html')