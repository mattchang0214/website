from books.models import Book
from django import forms

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = [
            'seller',
            'posted',
            'updated',
        ]
        labels = {
            'isbn': 'ISBN',
            'class_id': 'Class',
            'details': 'Details (Optional)',
        }
        widgets = {
            'details': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }