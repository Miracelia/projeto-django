from django.shortcuts import render
from .models import Produto

def home(request):
    aviso = None
    
    if request.method == "POST":
        nome = request.POST.get('nome_produto')
        data_cadastro = request.POST.get('data_cadastro')
        categoria = request.POST.get('categoria')
        
        Produto.objects.create(
            nome=nome,
            data_cadastro=data_cadastro,
            categoria=categoria
        )
        
        aviso = f"Produto '{nome}' cadastrado com sucesso!"
        
    return render(request, 'index.html', {'mensagem': aviso})

from .models import Vendedor
from .forms import VendedorForm

def lista_vendedores(request):
    q = request.GET.get('q', '')
    vendedores = Vendedor.objects.all()
    if q:
        vendedores = vendedores.filter(nome__icontains=q) | vendedores.filter(cpf__icontains=q)
    form = VendedorForm()
    return render(request, 'vendedores/lista.html', {
        'vendedores': vendedores,
        'form': form,
        'q': q,
        'total': Vendedor.objects.count(),
    })

def criar_vendedor(request):
    if request.method == 'POST':
        form = VendedorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'vendedores/lista.html', {
                'vendedores': Vendedor.objects.all(),
                'form': VendedorForm(),
                'mensagem': 'Vendedor cadastrado com sucesso!',
                'total': Vendedor.objects.count(),
            })
    else:
        form = VendedorForm()
    return render(request, 'vendedores/lista.html', {
        'vendedores': Vendedor.objects.all(),
        'form': form,
        'total': Vendedor.objects.count(),
    })

def editar_vendedor(request, pk):
    vendedor = Vendedor.objects.get(pk=pk)
    if request.method == 'POST':
        form = VendedorForm(request.POST, instance=vendedor)
        if form.is_valid():
            form.save()
            return render(request, 'vendedores/lista.html', {
                'vendedores': Vendedor.objects.all(),
                'form': VendedorForm(),
                'mensagem': 'Vendedor atualizado com sucesso!',
                'total': Vendedor.objects.count(),
            })
    else:
        form = VendedorForm(instance=vendedor)
    return render(request, 'vendedores/lista.html', {
        'vendedores': Vendedor.objects.all(),
        'form': form,
        'editando': vendedor,
        'total': Vendedor.objects.count(),
    })

def excluir_vendedor(request, pk):
    vendedor = Vendedor.objects.get(pk=pk)
    nome = vendedor.nome
    vendedor.delete()
    return render(request, 'vendedores/lista.html', {
        'vendedores': Vendedor.objects.all(),
        'form': VendedorForm(),
        'mensagem': f'"{nome}" excluído com sucesso.',
        'total': Vendedor.objects.count(),
    })