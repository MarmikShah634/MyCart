from django import forms
from multiupload.fields import MultiFileField
from .models import ProductImage, Product

class ProductImageForm(forms.ModelForm):
    product_id = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    images = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, required=False)

    class Meta:
        model = ProductImage
        fields = ['product_id', 'images']