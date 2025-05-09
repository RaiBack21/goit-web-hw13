from django.forms import ModelForm, CharField, DateField, TextInput, ModelChoiceField
from .models import Author, Quote, Tag


class AuthorForm(ModelForm):

    fullname = CharField(max_length=100, required=True)
    born_date = DateField(required=True)
    born_location = CharField(max_length=150, required=True)
    description = CharField(required=True)
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):

    quote = CharField(required=True)
    author = ModelChoiceField(queryset=Author.objects.all(), empty_label="-------")

    class Meta:
        model = Quote
        fields = ['quote', 'author']
        exclude = ['tags']