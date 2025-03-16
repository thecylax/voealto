from django import forms
from .models import BudgetItem, Client


class CommaSeparatedDecimalField(forms.DecimalField):
    def clean(self, value):
        value = value.replace(',', '.')
        return super().clean(value)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'document']
        labels = {
            'name': 'Nome',
            'document': 'CPF/CNPJ'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control font'}),
            'document': forms.TextInput(attrs={'class': 'form-control font'}),
        }

class SelectClientForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label='Cliente',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class BudgetItemForm(forms.ModelForm):
    ticket_value = CommaSeparatedDecimalField(max_digits=10, decimal_places=2)
    departure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data de Ida')
    arrive_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data de Volta')

    class Meta:
        model = BudgetItem
        fields = ['airline', 'origin_city', 'origin_iata', 'departure_date', 'departure_time', 'destiny_city', 'destiny_iata', 'arrive_date', 'arrive_time', 'ticket_value']
        labels = {
            'airline': 'Companhia Aérea',
            'origin_city': 'Cidade de Origem',
            'origin_iata': 'IATA',
            'departure_date': 'Data de Ida',
            'departure_time': 'Hora de Ida',
            'destiny_city': 'Cidade de Destino',
            'destiny_iata': 'IATA',
            'arrive_date': 'Data de Volta',
            'arrive_time': 'Hora de Volta',
            'ticket_value': 'Valor do Bilhete',
        }
        widgets = {
            'airline': forms.TextInput(attrs={'class': 'form-control font'}),
            'origin_city': forms.TextInput(attrs={'class': 'form-control font'}),
            'origin_iata': forms.TextInput(attrs={'class': 'form-control font'}),
            'departure_time': forms.TextInput(attrs={'class': 'form-control font'}),
            'destiny_city': forms.TextInput(attrs={'class': 'form-control font'}),
            'destiny_iata': forms.TextInput(attrs={'class': 'form-control font'}),
            'arrive_time': forms.DateInput(attrs={'class': 'form-control font'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))


class BudgetItemSearchForm(forms.Form):
    budget_id = forms.CharField(
        label='ID do Orçamento',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control font', 'placeholder': 'Digite o ID do Orçamento'}))