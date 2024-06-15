from django import forms
from .models import Author, Quote



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
        
class QuoteForm(forms.ModelForm):
    quote = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Separated by commas'}))
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label="Select an author")

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']

