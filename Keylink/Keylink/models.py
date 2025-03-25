from django.db import models

class Chave(models.Model):
    id_chaves = models.AutoField(primary_key=True)
    numero_chave = models.CharField(max_length=10)
    descricao = models.TextField(null=True, blank=True)
    disponivel = models.BooleanField(default=True)
    data_cadastro = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey('Funcionario', null=True, blank=True, on_delete=models.SET_NULL, related_name='chaves_utilizadas')

    class Meta:
        db_table = 'chaves'
        ordering = ['numero_chave']
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return f"Chave {self.numero_chave}"

class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    nome_funcionario = models.CharField(max_length=255)
    usuario_funcionario = models.CharField(max_length=255)
    telefone_funcionario = models.CharField(max_length=20, null=True, blank=True)
    endereco_funcionario = models.CharField(max_length=255, null=True, blank=True)
    funcao_funcionario = models.CharField(max_length=255, null=True, blank=True)
    cpf_funcionario = models.CharField(max_length=14)
    senha = models.CharField(max_length=128)
    tipo_funcionario = models.CharField(max_length=20, default='Quadro')

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
