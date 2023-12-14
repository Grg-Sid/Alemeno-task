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
            "monthaly_salary",
        ]

    def validate(self, data):
        age = data.get("age")
        monthaly_salary = data.get("monthaly_salary")
        if age < 18:
            raise serializers.ValidationError("Age should be greater than 18")
        if monthaly_salary < 1:
            raise serializers.ValidationError(
                "Monthaly salary should be greater than 0"
            )
        return data

    def create(self, validated_data):
        monthaly_salary = validated_data.get("monthaly_salary")
        rounded_salary = monthaly_salary
        if monthaly_salary > 100000:
            rounded_salary = (monthaly_salary // 100000) * 100000
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
        data = super().to_representation(instance)
        data["loan_approved"] = utils.check_loan_approval(
            instance.customer.id, instance.loan_amount
        )
        data["message"] = (
            "Loan approved" if data["loan_approved"] else "Loan not approved"
        )
        emi = utils.calculate_monthaly_installment(
            instance.loan_amount, instance.tenure, instance.interest_rate
        )
        data["emi"] = round(emi, 2)
        return data

    def create(self, validated_data):
        emi = utils.calculate_monthaly_installment(
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
        return Loan.objects.create(**validated_data)
