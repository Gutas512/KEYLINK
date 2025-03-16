from django.db import models


class Sala(models.Model):
    numero_sala = models.IntegerField()
    tipo_de_sala = models.CharField(max_length=255)

    def __str__(self):
        return f"Sala {self.numero_sala} - {self.tipo_de_sala}"


class Chave(models.Model):
    salas = models.ForeignKey(Sala, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chave {self.id_chaves} - Sala {self.salas.numero_sala}"


class Funcionario(models.Model):
    QUADRO = 'Quadro'
    EXTRA_QUADRO = 'Extra Quadro'

    TIPOS_FUNCIONARIO = [
        (QUADRO, 'Quadro'),
        (EXTRA_QUADRO, 'Extra Quadro'),
    ]

    nome_funcionario = models.CharField(max_length=255)
    usuario_funcionario = models.CharField(max_length=255)
    telefone_funcionario = models.CharField(max_length=20, blank=True, null=True)
    endereco_funcionario = models.CharField(max_length=255, blank=True, null=True)
    funcao_funcionario = models.CharField(max_length=255, blank=True, null=True)
    cpf_funcionario = models.CharField(max_length=14, unique=True)
    senha = models.CharField(max_length=128)
    tipo_funcionario = models.CharField(
        max_length=20,
        choices=TIPOS_FUNCIONARIO,
        default=QUADRO
    )

    def __str__(self):
        return self.nome_funcionario


class RegistroSaida(models.Model):
    chaves = models.ForeignKey(Chave, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    registro_saida_horario = models.DateTimeField()

    def __str__(self):
        return f"Registro de Saída {self.id_registro}"


class RegistroEntrada(models.Model):
    registro_saida = models.ForeignKey(RegistroSaida, on_delete=models.CASCADE)
    chaves = models.ForeignKey(Chave, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    registro_entrada_horario = models.DateTimeField()

    def __str__(self):
        return f"Registro de Entrada {self.id_registro_entrada}"
