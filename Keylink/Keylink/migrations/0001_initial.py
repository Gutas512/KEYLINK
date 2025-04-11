# Generated by Django 5.1.3 on 2025-03-30 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id_funcionario', models.AutoField(db_column='id_funcionario', primary_key=True, serialize=False)),
                ('nome_funcionario', models.CharField(max_length=255)),
                ('usuario_funcionario', models.CharField(max_length=255)),
                ('telefone_funcionario', models.CharField(blank=True, max_length=20, null=True)),
                ('endereco_funcionario', models.CharField(blank=True, max_length=255, null=True)),
                ('funcao_funcionario', models.CharField(blank=True, max_length=255, null=True)),
                ('cpf_funcionario', models.CharField(max_length=14)),
                ('senha', models.CharField(max_length=128)),
                ('tipo_funcionario', models.CharField(default='Quadro', max_length=20)),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
                'db_table': 'funcionarios',
                'ordering': ['nome_funcionario'],
                'constraints': [models.CheckConstraint(condition=models.Q(('tipo_funcionario__in', ['Quadro', 'Extra Quadro'])), name='tipo_funcionario_valido')],
            },
        ),
        migrations.CreateModel(
            name='Chave',
            fields=[
                ('id_chaves', models.AutoField(db_column='id_chaves', primary_key=True, serialize=False)),
                ('numero_chave', models.CharField(max_length=10)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('disponivel', models.BooleanField(default=True)),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('usuario', models.ForeignKey(blank=True, db_column='usuario_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chaves_utilizadas', to='Keylink.funcionario')),
            ],
            options={
                'verbose_name': 'Chave',
                'verbose_name_plural': 'Chaves',
                'db_table': 'chaves',
                'ordering': ['numero_chave'],
            },
        ),
    ]
