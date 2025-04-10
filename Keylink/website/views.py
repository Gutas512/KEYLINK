from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Keylink.forms import *

def login_funcionario(request):
    if 'funcionario_id' in request.session:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            funcionario = Funcionario.objects.get(usuario_funcionario=username)
            if funcionario.senha == password:
                request.session['funcionario_id'] = funcionario.id_funcionario
                return redirect('index')
            else:
                messages.error(request, 'Senha incorreta')
        except Funcionario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')

        return render(request, 'login.html')

    return render(request, 'login.html')

def logout_funcionario(request):
    request.session.flush()
    return redirect('login')

def index(request):
    if 'funcionario_id' not in request.session:
        return redirect('login')

    try:
        funcionario = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
        return render(request, 'index.html', {'funcionario': funcionario})
    except Funcionario.DoesNotExist:
        messages.error(request, 'Sessão inválida')
        return redirect('login')

@login_required
def listar_funcionarios(request):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    funcionarios = Funcionario.objects.all()
    return render(request, 'listar_funcionarios.html', {
        'funcionario': funcionario_logado,
        'funcionarios': funcionarios
    })

@login_required
def adicionar_funcionario(request):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_funcionarios')
    else:
        form = FuncionarioForm()
    return render(request, 'funcionarios/adicionar.html', {
        'form': form,
        'funcionario': funcionario_logado
    })

@login_required
def editar_funcionario(request, id):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    funcionario = get_object_or_404(Funcionario, id_funcionario=id)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('listar_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'funcionarios/editar.html', {
        'form': form,
        'funcionario': funcionario_logado
    })

@login_required
def excluir_funcionario(request, id):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    funcionario = get_object_or_404(Funcionario, id_funcionario=id)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('listar_funcionarios')
    return render(request, 'funcionarios/excluir.html', {
        'funcionario': funcionario_logado,
        'funcionario_a_excluir': funcionario
    })

@login_required
def listar_chaves(request):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    chaves = Chave.objects.all()
    return render(request, 'listar_chaves.html', {
        'chaves': chaves,
        'funcionario': funcionario_logado
    })

@login_required
def adicionar_chave(request):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    if request.method == 'POST':
        form = ChaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_chaves')
    else:
        form = ChaveForm()
    return render(request, 'chaves/adicionar.html', {
        'form': form,
        'funcionario': funcionario_logado
    })

@login_required
def editar_chave(request, id):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    chave = Chave.objects.get(id_chaves=id)
    if request.method == 'POST':
        form = ChaveForm(request.POST, instance=chave)
        if form.is_valid():
            form.save()
            return redirect('listar_chaves')
    else:
        form = ChaveForm(instance=chave)
    return render(request, 'chaves/editar.html', {
        'form': form,
        'chave': chave,
        'funcionario': funcionario_logado
    })

@login_required
def utilizar_chave(request, chave_id):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    chave = get_object_or_404(Chave, id_chaves=chave_id)

    if chave.disponivel:
        chave.usuario = funcionario_logado
        chave.disponivel = False
        chave.save()

        timestamp = int(timezone.now().timestamp())
        registro_id = f"SAIDA-{timestamp}-{chave_id}-{funcionario_logado.id_funcionario}"

        RegistroSaida.objects.create(
            id_registro=registro_id,
            chaves=chave,
            funcionario=funcionario_logado,
            registro_saida_horario=timezone.now()
        )

        messages.success(request, f'Chave {chave.numero_chave} utilizada com sucesso!')
        return redirect('listar_chaves')
    else:
        messages.error(request, 'Esta chave já está em uso!')
        return redirect('listar_chaves')

@login_required
def devolver_chave(request, chave_id):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    chave = get_object_or_404(Chave, id_chaves=chave_id)

    if chave.usuario and chave.usuario.id_funcionario == funcionario_logado.id_funcionario:
        registro_saida = RegistroSaida.objects.filter(
            chaves=chave,
            funcionario=funcionario_logado
        ).order_by('-registro_saida_horario').first()

        if registro_saida:
            RegistroEntrada.objects.create(
                registro_saida=registro_saida,
                chaves=chave,
                funcionario=funcionario_logado,
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
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    chave = Chave.objects.get(id_chaves=id)
    if request.method == 'POST':
        chave.delete()
        return redirect('listar_chaves')
    return render(request, 'chaves/excluir.html', {
        'chave': chave,
        'funcionario': funcionario_logado
    })

@login_required
def listar_registros(request):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    registros_saida = RegistroSaida.objects.all().order_by('-registro_saida_horario')
    registros_entrada = RegistroEntrada.objects.all().order_by('-registro_entrada_horario')

    return render(request, 'listar_registros.html', {
        'registros_saida': registros_saida,
        'registros_entrada': registros_entrada,
        'funcionario': funcionario_logado
    })

@login_required
def registrar_saida(request, chave_id):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    try:
        chave = Chave.objects.get(id_chaves=chave_id)
        if chave.disponivel:
            RegistroSaida.objects.create(
                chaves=chave,
                funcionario=funcionario_logado,
                registro_saida_horario=timezone.now()
            )
            chave.disponivel = False
            chave.save()
            return redirect('listar_registros')
    except Chave.DoesNotExist:
        pass
    return redirect('listar_registros')

@login_required
def registrar_entrada(request, chave_id):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    try:
        chave = Chave.objects.get(id_chaves=chave_id)
        if not chave.disponivel:
            registro_saida = RegistroSaida.objects.filter(chaves=chave).last()
            if registro_saida:
                RegistroEntrada.objects.create(
                    registro_saida=registro_saida,
                    chaves=chave,
                    funcionario=funcionario_logado,
                    registro_entrada_horario=timezone.now()
                )
                chave.disponivel = True
                chave.save()
    except Chave.DoesNotExist:
        pass
    return redirect('listar_registros')

@login_required
def registros_chaves(request):
    funcionario_logado = Funcionario.objects.get(id_funcionario=request.session['funcionario_id'])
    registros_saida = RegistroSaida.objects.all()
    registros_entrada = RegistroEntrada.objects.all()

    return render(request, 'listar_registros.html', {
        'registros_saida': registros_saida,
        'registros_entrada': registros_entrada,
        'funcionario': funcionario_logado
    })