from django.db import models

class Vendedor(models.Model):
    nome     = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email    = models.EmailField(blank=True, default='')
    cpf      = models.CharField(max_length=14, blank=True, default='')
    cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    CATEGORIAS = [
        ('termogenicos', 'Termogênicos'),
        ('proteicos', 'Proteicos'),
        ('vitaminas', 'Vitaminas'),
    ]
    nome = models.CharField(max_length=100)
    data_cadastro = models.DateField(null=True, blank=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)

    def __str__(self):
        return self.nome