from django.contrib import admin
from Keylink.models import Funcionario, RegistroSaida, RegistroEntrada, Chave
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry

LogEntry._meta.get_field('user').remote_field.model = Funcionario

# Remove o registro existente (se houver)
if admin.site.is_registered(Funcionario):
    admin.site.unregister(Funcionario)

# Registra com a classe personalizada (usando decorador)
@admin.register(Funcionario)
class FuncionarioAdmin(UserAdmin):
    list_display = ('usuario_funcionario', 'nome_funcionario', 'tipo_usuario', 'is_staff')
    list_filter = ('tipo_usuario', 'is_staff')
    fieldsets = (
        (None, {'fields': ('usuario_funcionario', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_funcionario', 'cpf_funcionario',
                                          'telefone_funcionario', 'endereco_funcionario',
                                          'funcao_funcionario')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                'tipo_usuario', 'tipo_funcionario',
                                'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('usuario_funcionario', 'nome_funcionario', 'password1', 'password2',
                     'is_staff', 'tipo_usuario'),
        }),
    )
    search_fields = ('usuario_funcionario', 'nome_funcionario')
    ordering = ('nome_funcionario',)
    filter_horizontal = ('groups', 'user_permissions',)

# Registra os outros modelos normalmente
admin.site.register(Chave)
admin.site.register(RegistroSaida)
admin.site.register(RegistroEntrada)