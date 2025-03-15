from datetime import datetime
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BudgetItem(models.Model):
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE, related_name='items')
    airline = models.CharField(max_length=255)
    origin_city = models.CharField(max_length=255)
    origin_iata = models.CharField(max_length=3)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    destiny_city = models.CharField(max_length=255)
    destiny_iata = models.CharField(max_length=3)
    arrive_date = models.DateField()
    arrive_time = models.TimeField()
    ticket_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.origin_iata} to {self.destiny_iata}'


class Budget(models.Model):
    budget_id = models.CharField(max_length=255, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            now = datetime.now()
            self.budget_id = f'{now.year}{now.month:02d}{self.pk:06d}'
            kwargs['force_insert'] = False
        super().save(*args, **kwargs)

    def get_total_ticket_value(self):
            return self.items.aggregate(total=models.Sum('ticket_value'))['total'] or 0

    def __str__(self):
        return f"{self.client} - {self.budget_id}"
