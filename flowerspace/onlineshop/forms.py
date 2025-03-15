from django import forms
from .models import Product, Category, Coupons
from django.utils.text import slugify


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'available', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter product title'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Describe your product'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 49.99'}),
            'image': forms.FileInput(attrs={'class': 'form-file'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox-list'}),
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        product.slug = slugify(product.title)
        product.save()
        product.category.set(self.cleaned_data["category"])
        return product



class CouponForm(forms.Form):
    code = forms.CharField(max_length=200, min_length=1, widget=forms.TextInput(attrs={'class':'coupon-input', 'placeholder':'Enter your coupon code'}))


class UserOrderInfoForm(forms.Form):
    name = forms.CharField(max_length=200, min_length=3, widget=forms.TextInput(attrs={'class':'form-input', 'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=200, min_length=3, widget=forms.TextInput(attrs={'class':'form-input', 'placeholder':'Last Name'}))

    address = forms.CharField(max_length=500, min_length=1, widget=forms.Textarea(attrs={
    'class':"form-textarea", 'placeholder':"Enter your address", 'name':"address",'rows':3, 'type':'textarea'}))