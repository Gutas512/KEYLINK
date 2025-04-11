from django import forms
from django.contrib.auth.hashers import make_password
from .models import *

class ChaveForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = ['numero_chave', 'descricao', 'disponivel']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class FuncionarioForm(forms.ModelForm):
    # Campo de senha com widget de password
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha'
        }),
        label="Senha"
    )

    # Confirmação de senha (opcional)
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        }),
        label="Confirmar Senha",
        required=False
    )

    class Meta:
        model = Funcionario
        fields = [
            'nome_funcionario',
            'telefone_funcionario',
            'endereco_funcionario',
            'funcao_funcionario',
            'cpf_funcionario',
            'senha',
            'tipo_funcionario',
            'usuario_funcionario'
        ]
        widgets = {
            'tipo_funcionario': forms.Select(attrs={'class': 'form-control'}),
            'usuario_funcionario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário único'
            }),
            'nome_funcionario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'cpf_funcionario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
        }
        labels = {
            'usuario_funcionario': 'Usuário',
            'nome_funcionario': 'Nome Completo',
            'tipo_funcionario': 'Tipo de Funcionário'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes CSS a todos os campos automaticamente
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.widgets:
                field.widget.attrs.update({'class': 'form-control'})

            # Adiciona placeholders
            if not field.widget.attrs.get('placeholder'):
                field.widget.attrs['placeholder'] = f'Digite {field.label.lower()}'

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        # Validação de confirmação de senha (se o campo existir)
        if 'confirmar_senha' in self.fields and senha != confirmar_senha:
            self.add_error('confirmar_senha', "As senhas não coincidem")

        return cleaned_data

    def save(self, commit=True):
        funcionario = super().save(commit=False)
        funcionario.set_password(self.cleaned_data['senha'])  # Criptografa a senha

        if commit:
            funcionario.save()
        return funcionario

    def save(self, commit=True):
        # Verificar se a senha foi fornecida e hasheá-la
        funcionario = super().save(commit=False)
        if funcionario.senha:
            funcionario.senha = make_password(funcionario.senha)
        if commit:
            funcionario.save()
        return funcionario



    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if len(senha) < 8:
            raise forms.ValidationError("A senha deve ter no mínimo 8 caracteres.")
        return senha


class LoginForm(forms.Form):
    cpf_funcionario = forms.CharField(max_length=14, label="CPF", widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}))


class RegistroSaidaForm(forms.ModelForm):
    class Meta:
        model = RegistroSaida
        fields = ['chaves', 'funcionario', 'registro_saida_horario']

class RegistroEntradaForm(forms.ModelForm):
    class Meta:
        model = RegistroEntrada
        fields = ['registro_saida', 'chaves', 'funcionario', 'registro_entrada_horario']