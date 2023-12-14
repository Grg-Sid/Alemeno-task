import datetime

from django.utils import timezone
from rest_framework import serializers

from core.models import Customer, Loan
import core.utils as utils


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "age",
            "phone",
            "monthly_salary",
        ]

    def validate(self, data):
        age = data.get("age")
        monthly_salary = data.get("monthly_salary")
        if age < 18:
            raise serializers.ValidationError("Age should be greater than 18")
        if monthly_salary < 1:
            raise serializers.ValidationError("Monthly salary should be greater than 0")
        return data

    def create(self, validated_data):
        monthly_salary = validated_data.get("monthly_salary")
        rounded_salary = monthly_salary
        if monthly_salary > 100000:
            rounded_salary = (monthly_salary // 100000) * 100000
        approved_limit = 36 * rounded_salary
        validated_data["approved_limit"] = approved_limit
        return Customer.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["approved_limit"] = instance.approved_limit
        return data


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "customer",
            "loan_amount",
            "tenure",
            "interest_rate",
        ]

    def validate(self, data):
        loan_amount = data.get("loan_amount")
        tenure = data.get("tenure")
        interest_rate = data.get("interest_rate")

        if loan_amount < 1:
            raise serializers.ValidationError("Loan amount should be greater than 0")

        if tenure and tenure < 1:
            raise serializers.ValidationError("Tenure should be greater than 0")

        if interest_rate and interest_rate < 1:
            raise serializers.ValidationError("Interest rate should be greater than 0")
        return data

    def to_representation(self, instance):
        data = {}
        data["loan_id"] = None
        data["customer_id"] = instance.customer.id
        data["loan_approved"] = utils.check_loan_approval(
            instance.customer.id, instance.loan_amount
        )
        data["monthly_installment"] = 0
        if data["loan_approved"]:
            data["loan_id"] = instance.id
            emi = utils.calculate_monthly_installment(
                instance.loan_amount, instance.tenure, instance.interest_rate
            )
            data["monthly_installment"] = round(emi, 2)
        data["message"] = (
            "Loan approved" if data["loan_approved"] else "Loan not approved"
        )
        return data

    def create(self, validated_data):
        status = False
        emi = utils.calculate_monthly_installment(
            validated_data["loan_amount"],
            validated_data["tenure"],
            validated_data["interest_rate"],
        )
        validated_data["emi"] = round(emi, 2)
        validated_data["emi_paid_on_time"] = 0
        validated_data["start_date"] = timezone.now()
        validated_data["end_date"] = timezone.now() + datetime.timedelta(
            days=(validated_data["tenure"] + 1) * 30
        )
        utils.get_credit_rating(customer_id=validated_data["customer"].id)
        if utils.check_loan_approval(
            validated_data["customer"].id, validated_data["loan_amount"]
        ):
            status = True
        if status:
            validated_data["interest_rate"] = utils.corrected_interest_rate(
                validated_data["customer"].id
            )
            return Loan.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("Loan not approved")
