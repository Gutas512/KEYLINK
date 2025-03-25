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
    # Verifique se o funcionário está logado na sessão
    if 'funcionario_id' not in request.session:
        return redirect('login')  # Redireciona para o login se não houver funcionário logado

    funcionario_id = request.session['funcionario_id']
    try:
        funcionario = Funcionario.objects.get(id_funcionario=funcionario_id)
    except Funcionario.DoesNotExist:
        return redirect('sem_permissao')  # Caso não seja um funcionário válido, redireciona para "sem_permissao"

    # Obtém a chave
    chave = get_object_or_404(Chave, id_chaves=chave_id)

    # Verifique o estado da chave
    print(f"Chave {chave.numero_chave} está disponível? {chave.disponivel}")

    # Verifique se a chave está disponível
    if chave.disponivel:
        chave.usuario = funcionario  # Atribui o funcionário à chave
        chave.disponivel = False  # Marca a chave como indisponível
        chave.save()



        return redirect('listar_chaves')  # Redirecionar para a lista de chaves após a utilização
    else:
        return redirect('chave_indisponivel')  # Redirecionar se a chave já foi utilizada



def devolver_chave(request, chave_id):
    # Verifique se o funcionário está logado na sessão
    if 'funcionario_id' not in request.session:
        return redirect('login')  # Redireciona para o login se não houver funcionário logado

    funcionario_id = request.session['funcionario_id']
    try:
        funcionario = Funcionario.objects.get(id_funcionario=funcionario_id)
    except Funcionario.DoesNotExist:
        return redirect('sem_permissao')  # Caso não seja um funcionário válido, redireciona para "sem_permissao"

    # Obtém a chave
    chave = get_object_or_404(Chave, id_chaves=chave_id)

    # Verifique se a chave foi emprestada para o funcionário
    if chave.usuario == funcionario:  # Verifica se o funcionário é o responsável pela chave
        chave.usuario = None  # Remove o funcionário da chave
        chave.disponivel = True  # Marca a chave como disponível novamente


        chave.save()

        return redirect('listar_chaves')  # Redirecionar para a lista de chaves após a devolução
    else:
        return redirect('chave_nao_emprestada')  # Caso a chave não tenha sido emprestada ao funcionário


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