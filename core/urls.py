from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_vendedores, name='lista'),
    path('novo/', views.criar_vendedor, name='criar'),
    path('<int:pk>/editar/', views.editar_vendedor, name='editar'),
    path('<int:pk>/excluir/', views.excluir_vendedor, name='excluir'),
]