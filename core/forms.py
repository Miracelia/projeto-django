import re
from django import forms
from .models import Vendedor

def formatar_cpf(cpf):
    d = re.sub(r'\D', '', cpf)
    return f'{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}' if len(d) == 11 else cpf

def formatar_telefone(tel):
    d = re.sub(r'\D', '', tel)
    if len(d) == 11: return f'({d[:2]}) {d[2:7]}-{d[7:]}'
    if len(d) == 10: return f'({d[:2]}) {d[2:6]}-{d[6:]}'
    return tel

def validar_cpf(cpf):
    d = re.sub(r'\D', '', cpf)
    if len(d) != 11 or len(set(d)) == 1:
        return False
    for i in range(9, 11):
        soma = sum(int(d[j]) * (i + 1 - j) for j in range(i))
        if (soma * 10 % 11) % 10 != int(d[i]):
            return False
    return True

class VendedorForm(forms.ModelForm):
    class Meta:
        model  = Vendedor
        fields = ['nome', 'telefone', 'email', 'cpf']

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if len(nome) < 3:
            raise forms.ValidationError('Nome deve ter ao menos 3 caracteres.')
        return nome

    def clean_telefone(self):
        tel = self.cleaned_data['telefone']
        if len(re.sub(r'\D', '', tel)) not in (10, 11):
            raise forms.ValidationError('Telefone inválido. Use DDD + número.')
        return formatar_telefone(tel)

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not validar_cpf(cpf):
            raise forms.ValidationError('CPF inválido.')
        cpf_fmt = formatar_cpf(cpf)
        qs = Vendedor.objects.filter(cpf=cpf_fmt)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('CPF já cadastrado.')
        return cpf_fmt