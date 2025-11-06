from django import forms
from .models import Client  # o Supplier para el otro caso

class ClientForm(forms.ModelForm):  # SupplierForm en el otro caso
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.Textarea):
                widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md bg-white shadow-sm focus:outline-none focus:ring focus:ring-blue-200'
                })
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({
                    'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
                })
            else:
                widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md bg-white shadow-sm focus:outline-none focus:ring focus:ring-blue-200'
                })