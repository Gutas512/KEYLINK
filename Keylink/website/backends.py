from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from Keylink.models import Funcionario

class FuncionarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            funcionario = Funcionario.objects.get(usuario_funcionario=username)
            if check_password(password, funcionario.senha):  # Alterado para usar 'senha'
                return funcionario
        except Funcionario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Funcionario.objects.get(pk=user_id)
        except Funcionario.DoesNotExist:
            return None