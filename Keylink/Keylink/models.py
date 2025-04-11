
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class Funcionario(models.Model):
    # Opções para tipo_funcionario
    QUADRO = 'Quadro'
    EXTRA_QUADRO = 'Extra Quadro'
    TIPO_CHOICES = [
        (QUADRO, 'Quadro'),
        (EXTRA_QUADRO, 'Extra Quadro'),
    ]

    # Campos do modelo
    id_funcionario = models.AutoField(primary_key=True, db_column='id_funcionario')
    nome_funcionario = models.CharField(max_length=255)
    usuario_funcionario = models.CharField(max_length=255, unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    telefone_funcionario = models.CharField(max_length=20, null=True, blank=True)
    endereco_funcionario = models.CharField(max_length=255, null=True, blank=True)
    funcao_funcionario = models.CharField(max_length=255, null=True, blank=True)
    cpf_funcionario = models.CharField(max_length=14, unique=True)
    senha = models.CharField(max_length=128)
    tipo_funcionario = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default=QUADRO,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'funcionarios'
        ordering = ['nome_funcionario']
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        constraints = [
            models.CheckConstraint(
                check=models.Q(tipo_funcionario__in=['QUADRO', 'EXTRA_QUADRO']),
                name='tipo_funcionario_valido'
            )
        ]

    def __str__(self):
        return self.nome_funcionario

    # Métodos necessários para autenticação
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)

    def get_username(self):
        return self.usuario_funcionario

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])


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
