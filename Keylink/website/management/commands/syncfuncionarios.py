from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Keylink.models import Funcionario

class Command(BaseCommand):
    help = 'Cria usuários Django para funcionários existentes'

    def handle(self, *args, **options):
        for funcionario in Funcionario.objects.all():
            User.objects.get_or_create(
                username=funcionario.usuario_funcionario,
                defaults={
                    'first_name': funcionario.nome_funcionario.split()[0],
                    'last_name': ' '.join(funcionario.nome_funcionario.split()[1:])
                               if ' ' in funcionario.nome_funcionario else ''
                }
            )
        self.stdout.write(self.style.SUCCESS('Usuários sincronizados com sucesso!'))