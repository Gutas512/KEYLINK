from django.contrib import admin
from Keylink.models import Funcionario, RegistroSaida, RegistroEntrada, Chave

admin.site.register(Funcionario)
admin.site.register(Chave)
admin.site.register(RegistroSaida)
admin.site.register(RegistroEntrada)