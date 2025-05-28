from django import forms
from django.contrib.auth.hashers import make_password
from .models import *
from django.core.exceptions import ValidationError

class ChaveForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = ['numero_chave', 'descricao', 'disponivel']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


    def clean_numero_chave(self):
        numero_chave = self.cleaned_data.get('numero_chave')
        if Chave.objects.filter(numero_chave=numero_chave).exists():
            raise ValidationError("Este número de chave já está cadastrado.")
        return numero_chave


from django import forms
from django.contrib.auth.hashers import make_password
from .models import Funcionario


class FuncionarioForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha (mínimo 8 caracteres)'
        }),
        label="Senha",
        required=False  # Tornando opcional para edição
    )

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
            'usuario_funcionario',
            'nome_funcionario',
            'cpf_funcionario',
            'telefone_funcionario',
            'endereco_funcionario',
            'funcao_funcionario',
            'tipo_funcionario',
            'tipo_usuario',
            'is_active',
            'is_staff',
            'senha'
        ]
        widgets = {
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
            'tipo_funcionario': forms.Select(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'usuario_funcionario': 'Usuário',
            'nome_funcionario': 'Nome Completo',
            'tipo_funcionario': 'Tipo de Funcionário',
            'tipo_usuario': 'Tipo de Usuário',
            'is_active': 'Ativo',
            'is_staff': 'Acesso ao Admin'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurações específicas para edição vs criação
        if self.instance.pk:
            self.fields['senha'].required = False
            self.fields['confirmar_senha'].required = False
            self.fields['usuario_funcionario'].disabled = True

        # Adiciona classes CSS e placeholders padrão
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if not isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = 'form-control'

            if not field.widget.attrs.get('placeholder') and not isinstance(field.widget,
                                                                            (forms.CheckboxInput, forms.Select)):
                field.widget.attrs['placeholder'] = f'Digite {field.label.lower()}'

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        # Validação apenas para criação ou quando senha é fornecida
        if (not self.instance.pk or senha) and senha != confirmar_senha:
            self.add_error('confirmar_senha', "As senhas não coincidem")

        return cleaned_data

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if senha and len(senha) < 8:
            raise forms.ValidationError("A senha deve ter no mínimo 8 caracteres.")
        return senha

    def clean_cpf_funcionario(self):
        cpf = self.cleaned_data.get('cpf_funcionario')
        # Aqui você pode adicionar validação de CPF se necessário
        return cpf

    def save(self, commit=True):
        funcionario = super().save(commit=False)

        # Apenas atualiza a senha se um novo valor foi fornecido
        if self.cleaned_data['senha']:
            funcionario.set_password(self.cleaned_data['senha'])

        if commit:
            funcionario.save()
        return funcionario


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