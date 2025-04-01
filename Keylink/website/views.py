from pyexpat.errors import messages
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from datetime import datetime
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
                request.session['funcionario_id'] = funcionario.id_funcionario
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
    if 'funcionario_id' in request.session:
        funcionario_id = request.session['funcionario_id']
        try:
            funcionario = Funcionario.objects.get(id_funcionario=funcionario_id)
            return render(request, 'index.html', {'funcionario': funcionario})
        except Funcionario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Funcionário não encontrado'})
    else:
        return render(request, 'login.html')


def listar_funcionarios(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')  # Se não houver o ID do funcionário na sessão, redireciona para o login

    # Recuperar o funcionário logado
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])

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
    funcionario = get_object_or_404(Funcionario, id_funcionario=id)  # Corrigido aqui
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
    funcionario = get_object_or_404(Funcionario, id_funcionario=id)  # Corrigido aqui
    if request.method == 'POST':
        funcionario.delete()
        return redirect('listar_funcionarios')
    return render(request, 'funcionarios/excluir.html', {'funcionario': funcionario})

def listar_chaves(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')  # Se não houver o ID do funcionário na sessão, redireciona para o login

    # Recuperar o funcionário logado
    funcionario_id = request.session['funcionario_id']
    try:
        funcionario = Funcionario.objects.get(id_funcionario=funcionario_id)
    except Funcionario.DoesNotExist:
        return redirect('sem_permissao')  # Caso não encontre o funcionário, redireciona para "sem_permissao"

    # Recuperar a lista de todas as chaves
    chaves = Chave.objects.all()

    # Passar os dados para o template
    return render(request, 'listar_chaves.html', {'chaves': chaves, 'funcionario': funcionario})


def adicionar_chave(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')  # Redireciona para o login se não houver funcionário logado

    if request.method == 'POST':
        form = ChaveForm(request.POST)  # Cria um formulário com os dados enviados
        if form.is_valid():
            form.save()  # Salva a chave no banco de dados
            return redirect('listar_chaves')  # Redireciona para a lista de chaves
    else:
        form = ChaveForm()  # Cria um formulário vazio para exibir no template

    return render(request, 'chaves/adicionar.html', {'form': form})

def editar_chave(request, id):
    if 'funcionario_id' not in request.session:
        return redirect('login')  # Redireciona para o login se não houver funcionário logado

    chave = Chave.objects.get(id_chaves=id)  # Recupera a chave a ser editada
    if request.method == 'POST':
        form = ChaveForm(request.POST, instance=chave)  # Preenche o formulário com os dados da chave
        if form.is_valid():
            form.save()  # Salva as alterações no banco de dados
            return redirect('listar_chaves')  # Redireciona para a lista de chaves
    else:
        form = ChaveForm(instance=chave)  # Cria o formulário com os dados da chave

    return render(request, 'chaves/editar.html', {'form': form, 'chave': chave})


def utilizar_chave(request, chave_id):
    if 'funcionario_id' not in request.session:
        return redirect('login')

    funcionario_id = request.session['funcionario_id']
    try:
        funcionario = Funcionario.objects.get(id_funcionario=funcionario_id)
    except Funcionario.DoesNotExist:
        return redirect('sem_permissao')

    chave = get_object_or_404(Chave, id_chaves=chave_id)

    if chave.disponivel:
        # Atualiza o status da chave
        chave.usuario = funcionario
        chave.disponivel = False
        chave.save()

        # Cria o registro de saída com ID único baseado em timestamp
        timestamp = int(timezone.now().timestamp())
        registro_id = f"SAIDA-{timestamp}-{chave_id}-{funcionario_id}"

        RegistroSaida.objects.create(
            id_registro=registro_id,
            chaves=chave,
            funcionario=funcionario,
            registro_saida_horario=timezone.now()
        )

        messages.success(request, f'Chave {chave.numero_chave} utilizada com sucesso!')
        return redirect('listar_chaves')
    else:
        messages.error(request, 'Esta chave já está em uso!')
        return redirect('listar_chaves')




def devolver_chave(request, chave_id):
    if 'funcionario_id' not in request.session:
        return redirect('login')

    funcionario_id = request.session['funcionario_id']
    try:
        funcionario = Funcionario.objects.get(id_funcionario=funcionario_id)
    except Funcionario.DoesNotExist:
        return redirect('sem_permissao')

    chave = get_object_or_404(Chave, id_chaves=chave_id)

    if chave.usuario and chave.usuario.id_funcionario == funcionario_id:
        # Encontra o registro de saída correspondente
        registro_saida = RegistroSaida.objects.filter(
            chaves=chave,
            funcionario=funcionario
        ).order_by('-registro_saida_horario').first()

        if registro_saida:
            # Cria o registro de entrada
            RegistroEntrada.objects.create(
                registro_saida=registro_saida,
                chaves=chave,
                funcionario=funcionario,
                registro_entrada_horario=timezone.now()
            )

            # Atualiza o status da chave
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
    # Retorna uma página indicando que a chave está indisponível
    return render(request, 'chave_indisponivel.html')

def sem_permissao(request):
    return render(request, 'sem_permissao.html')

def excluir_chave(request, id):
    if 'funcionario_id' not in request.session:
        return redirect('login')  # Redireciona para o login se não houver funcionário logado

    chave = Chave.objects.get(id_chaves=id)  # Recupera a chave a ser excluída
    if request.method == 'POST':
        chave.delete()  # Exclui a chave do banco de dados
        return redirect('listar_chaves')  # Redireciona para a lista de chaves

    return render(request, 'chaves/excluir.html', {'chave': chave})

def listar_registros(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')
    return render(request, 'listar_registros.html')

def registrar_saida(request, chave_id):
    try:
        chave = Chave.objects.get(id_chaves=chave_id)
        funcionario = request.user.funcionario  # Assumindo que você tem um modelo de Usuário associado ao Funcionario
        if chave.disponivel:  # Verifica se a chave está disponível
            registro_saida = RegistroSaida.objects.create(
                chaves=chave,
                funcionario=funcionario,
                registro_saida_horario=timezone.now()
            )
            chave.disponivel = False  # Marca a chave como não disponível
            chave.save()
            return redirect('listar_registros')  # Redireciona para a página de registros
        else:
            # Caso a chave já tenha sido retirada, você pode mostrar um erro ou algo do tipo
            return redirect('listar_registros')  # Exemplo, ou pode mostrar um erro
    except Chave.DoesNotExist:
        # Se a chave não for encontrada, você pode redirecionar ou mostrar uma mensagem de erro
        return redirect('listar_registros')

def registrar_entrada(request, chave_id):
    try:
        chave = Chave.objects.get(id_chaves=chave_id)
        funcionario = request.user.funcionario  # Assumindo que você tem um modelo de Usuário associado ao Funcionario
        if not chave.disponivel:  # Verifica se a chave está registrada como saída
            # Encontrar o último registro de saída relacionado à chave
            registro_saida = RegistroSaida.objects.filter(chaves=chave).last()
            if registro_saida:
                RegistroEntrada.objects.create(
                    registro_saida=registro_saida,
                    chaves=chave,
                    funcionario=funcionario,
                    registro_entrada_horario=timezone.now()
                )
                chave.disponivel = True  # Marca a chave como disponível novamente
                chave.save()
                return redirect('listar_registros')  # Redireciona para a página de registros
            else:
                # Se não encontrar um registro de saída correspondente
                return redirect('listar_registros')
        else:
            # Caso a chave já esteja disponível, você pode mostrar um erro ou algo do tipo
            return redirect('listar_registros')  # Exemplo, ou pode mostrar um erro
    except Chave.DoesNotExist:
        # Se a chave não for encontrada, você pode redirecionar ou mostrar uma mensagem de erro
        return redirect('listar_registros')


def registros_chaves(request):
    # Obtenha todos os registros de saída e entrada
    registros_saida = RegistroSaida.objects.all()
    registros_entrada = RegistroEntrada.objects.all()

    # Passe os registros para o template
    return render(request, 'listar_registros.html', {
        'registros_saida': registros_saida,
        'registros_entrada': registros_entrada,
    })

def listar_registros(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')

    try:
        funcionario = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    except Funcionario.DoesNotExist:
        return redirect('sem_permissao')

    registros_saida = RegistroSaida.objects.all().order_by('-registro_saida_horario')
    registros_entrada = RegistroEntrada.objects.all().order_by('-registro_entrada_horario')

    return render(request, 'listar_registros.html', {
        'registros_saida': registros_saida,
        'registros_entrada': registros_entrada,
        'funcionario': funcionario
    })