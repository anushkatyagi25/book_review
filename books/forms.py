from django import forms
from .models import *
class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        exclude=['author']
        fields=['title','genre','description']

# class ReviewForm(forms.ModelForm):
    
#     class Meta:
#         model=Review
#         fields=['rating','comment']
#         widgets={'rating':forms.HiddenInput(),}
