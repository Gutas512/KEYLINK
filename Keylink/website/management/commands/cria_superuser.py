from django.core.management.base import BaseCommand
from Keylink.models import Funcionario

class Command(BaseCommand):
    help = 'Cria um superusuário personalizado'

    def handle(self, *args, **options):
        Funcionario.objects.create_superuser(
            usuario_funcionario='admin',
            nome_funcionario='Admin',
            cpf_funcionario='12345678901',
            password='senhaforte123',
            is_staff=True,
            is_superuser=True
        )
        self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso!'))