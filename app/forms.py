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
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SelectClientForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label='Cliente',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class BudgetItemForm(forms.ModelForm):
    ticket_value = CommaSeparatedDecimalField(max_digits=10, decimal_places=2)
    departure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data de Partida')
    arrive_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data de Chegada')

    class Meta:
        model = BudgetItem
        fields = ['origin_city', 'origin_iata', 'departure_date', 'departure_time', 'destiny_city', 'destiny_iata', 'arrive_date', 'arrive_time', 'ticket_value']
        labels = {
            'origin_city': 'Cidade de Origem',
            'origin_iata': 'IATA',
            'departure_date': 'Data de Partida',
            'departure_time': 'Hora de Partida',
            'destiny_city': 'Cidade de Destino',
            'destiny_iata': 'IATA',
            'arrive_date': 'Data de Chegada',
            'arrive_time': 'Hora de Chegada',
            'ticket_value': 'Valor do Bilhete',
        }
        widgets = {
            'origin_city': forms.TextInput(attrs={'class': 'form-control'}),
            'origin_iata': forms.TextInput(attrs={'class': 'form-control'}),
            # 'departure_date': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_time': forms.TextInput(attrs={'class': 'form-control'}),
            'destiny_city': forms.TextInput(attrs={'class': 'form-control'}),
            'destiny_iata': forms.TextInput(attrs={'class': 'form-control'}),
            # 'arrive_date': forms.DateInput(attrs={'class': 'form-control'}),
            'arrive_time': forms.DateInput(attrs={'class': 'form-control'}),
            # 'ticket_value': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))