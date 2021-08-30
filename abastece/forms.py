from django import forms
from django.forms import inlineformset_factory

from .models import ItemPedido, Pedido


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido


ItemPedidoFormset = inlineformset_factory(Pedido, ItemPedido, form=ItemPedidoForm, extra=1, can_delete=True)
