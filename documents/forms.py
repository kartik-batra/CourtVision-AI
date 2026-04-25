from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file', 'case_number', 'court_name', 'filing_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., ABC Corp vs XYZ Ltd - Appeal'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'case_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CS(COMM) 123/2024'}),
            'court_name': forms.Select(attrs={'class': 'form-control'}),
            'filing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of the document...'}),
        }
