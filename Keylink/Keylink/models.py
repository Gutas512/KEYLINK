from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Funcionario(models.Model):
    # Mantenha todos os seus campos atuais
    id_funcionario = models.AutoField(primary_key=True, db_column='id_funcionario')
    nome_funcionario = models.CharField(max_length=255)
    usuario_funcionario = models.CharField(max_length=255, unique=True)
    telefone_funcionario = models.CharField(max_length=20, null=True, blank=True)
    endereco_funcionario = models.CharField(max_length=255, null=True, blank=True)
    funcao_funcionario = models.CharField(max_length=255, null=True, blank=True)
    cpf_funcionario = models.CharField(max_length=14)
    senha = models.CharField(max_length=128)
    tipo_funcionario = models.CharField(max_length=20, default='Quadro')

    # Adicione a relação com User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='funcionario'
    )

    class Meta:
        db_table = 'funcionarios'
        ordering = ['nome_funcionario']
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        constraints = [
            models.CheckConstraint(
                check=models.Q(tipo_funcionario__in=['Quadro', 'Extra Quadro']),
                name='tipo_funcionario_valido'
            )
        ]

    def __str__(self):
        return self.nome_funcionario


# Sinal para criar/atualizar User quando Funcionario for salvo
@receiver(post_save, sender=Funcionario)
def create_user_for_funcionario(sender, instance, created, **kwargs):
    if created or not instance.user:
        user, user_created = User.objects.get_or_create(
            username=instance.usuario_funcionario,
            defaults={
                'first_name': instance.nome_funcionario.split()[0],
                'last_name': ' '.join(instance.nome_funcionario.split()[1:]) if ' ' in instance.nome_funcionario else ''
            }
        )
        if user_created:
            user.set_password(instance.senha)
            user.save()
        instance.user = user
        instance.save()


class Chave(models.Model):
    id_chaves = models.AutoField(primary_key=True, db_column='id_chaves')
    numero_chave = models.CharField(max_length=10)
    descricao = models.TextField(null=True, blank=True)
    disponivel = models.BooleanField(default=True)
    data_cadastro = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(
        'Funcionario', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='chaves_utilizadas', db_column='usuario_id'
    )

    class Meta:
        db_table = 'chaves'
        ordering = ['numero_chave']
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return f"Chave {self.numero_chave}"


class RegistroSaida(models.Model):
    id_registro = models.CharField(max_length=45, primary_key=True)
    chaves = models.ForeignKey(Chave, on_delete=models.CASCADE, related_name="registros_saida")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name="registros_saida")
    registro_saida_horario = models.DateTimeField()

    def __str__(self):
        return f"Saída {self.id_registro} - {self.chaves.numero_chave}"

class RegistroEntrada(models.Model):
    id_registro_entrada = models.AutoField(primary_key=True)
    registro_saida = models.ForeignKey(RegistroSaida, on_delete=models.CASCADE, related_name="registros_entrada")
    chaves = models.ForeignKey(Chave, on_delete=models.CASCADE, related_name="registros_entrada")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name="registros_entrada")
    registro_entrada_horario = models.DateTimeField()

    def __str__(self):
        return f"Entrada {self.id_registro_entrada} - {self.chaves.numero_chave}"


class FuncionarioBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            funcionario = Funcionario.objects.get(usuario_funcionario=username)
            if funcionario.senha == password:  # Ou use check_password se estiver hash
                return funcionario.user  # Usa a property user que criamos
        except Funcionario.DoesNotExist:
            return None
        return None