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
    class Meta:
        model = Funcionario
        fields = ['nome_funcionario', 'telefone_funcionario', 'endereco_funcionario',
                  'funcao_funcionario', 'cpf_funcionario', 'senha', 'tipo_funcionario', 'usuario_funcionario']

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
