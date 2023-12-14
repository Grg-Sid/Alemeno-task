from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField(default=18)
    phone = models.CharField(max_length=20, unique=True)
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField()


class Loan(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="loans"
    )
    loan_amount = models.IntegerField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    emi = models.FloatField()
    emi_paid_on_time = models.SmallIntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
