from django.shortcuts import render
from Keylink.models import *
from Keylink.forms import *

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf_funcionario']
            senha = form.cleaned_data['senha']
            try:
                funcionario = Funcionario.objects.get(cpf_funcionario=cpf)
                if funcionario.senha == senha:
                    # Realiza o login no sistema
                    login(request, funcionario)
                    return redirect('home')  # Redireciona para a página inicial ou dashboard
                else:
                    messages.error(request, "Senha incorreta.")
            except Funcionario.DoesNotExist:
                messages.error(request, "CPF não encontrado.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
