from django.db import models

class Collector(models.Model):
    client_reference_no = models.CharField(max_length=36, null=False)
    balance = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    status = models.CharField(max_length=13, null=False)
    consumer_name = models.CharField(max_length=100, null=False)
    consumer_address = models.CharField(max_length=200, null=False)
    ssn = models.CharField(max_length=11, null=False)

    def __str__(self):
        return f"client_reference_no: {self.client_reference_no}, balance: {self.balance}, status: {self.status}, consumer_name: {self.consumer_name}, consumer_address: {self.consumer_address}, ssn: {self.ssn}"