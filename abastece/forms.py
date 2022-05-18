from django import forms
from django.forms import inlineformset_factory, Select, NumberInput

from .models import ItemPedido, Pedido, ProductoVariedadCiclo

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('nombre',)

class ItemPedidoForm(forms.ModelForm):
    def __init__(self, ciclo, *args, **kwargs):
        super(ItemPedidoForm, self).__init__(*args, **kwargs)
        self.fields['producto_variedad_ciclo'].queryset = ProductoVariedadCiclo.objects.filter(ciclo=ciclo).order_by(
            "producto_variedad")

    class Meta:
        model = ItemPedido
        exclude = ()
        widgets = {
            'producto_variedad_ciclo': Select(attrs={
                'class': "pedido-item_producto-variedad form-control",
                'style': 'width: 100%;',
                }),
            'cantidad': NumberInput(attrs={
                'class': "pedido-item_cantidad form-control",
                'style': 'width: 80px;',
            }),
        }

ItemPedidoFormset = inlineformset_factory(Pedido,
                                          ItemPedido,
                                          form=ItemPedidoForm,
                                          extra=0,
                                          can_delete=True,
                                          min_num=1,
                                          validate_min=True,
                                          can_delete_extra=True
                                          )
