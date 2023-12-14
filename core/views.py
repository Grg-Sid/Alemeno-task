import os

from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Customer, Loan
from core.serializers import CustomerSerializer, LoanSerializer
from core.tasks import add_customer_to_db, add_loan_to_db
import core.utils as utils

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)


# Create your views here.
def background_task(request):
    add_customer_to_db.delay(os.path.join(DATA_DIR, "customer_data.xlsx"))
    add_loan_to_db.delay(os.path.join(DATA_DIR, "loan_data.xlsx"))

    return HttpResponse("Background task is running")


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class CheckLoanView(APIView):
    def post(self, request, *args, **kwargs):
        customer_id = request.data.get("customer")
        loan_amount = request.data.get("loan_amount")
        tenure = request.data.get("tenure")
        interest_rate = request.data.get("interest_rate")
        if not customer_id:
            return Response(
                {"error": "Customer is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not loan_amount:
            return Response(
                {"error": "Loan amount is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not tenure:
            return Response(
                {"error": "Tenure is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not interest_rate:
            return Response(
                {"error": "Interest rate is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        approval_status = utils.check_loan_approval(customer_id, loan_amount)
        corrected_interest_rate = utils.corrected_interest_rate(customer_id)
        monthaly_installments = utils.calculate_monthaly_installment(
            loan_amount, tenure, corrected_interest_rate
        )
        monthaly_installments = round(monthaly_installments, 2)
        response_data = {
            "loan_amount": loan_amount,
            "tenure": tenure,
            "corrected_interest_rate": corrected_interest_rate,
            "approval_status": approval_status,
            "monthaly_installments": monthaly_installments,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class LoanView(APIView):
    def get(self, request, *args, **kwargs):
        loan_id = kwargs.get("loan_id")
        print(loan_id)
        if not loan_id:
            return Response(
                {"error": "Loan id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        loan = Loan.objects.get(pk=loan_id)
        customer_id = loan.customer.id
        customer = Customer.objects.get(pk=customer_id)
        response_data = {
            "loan_id": loan_id,
            "customer": {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "age": customer.age,
                "phone": customer.phone,
            },
            "loan_amount": loan.loan_amount,
            "tenure": loan.tenure,
            "interest_rate": loan.interest_rate,
            "emi": loan.emi,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class CustomerLoanView(APIView):
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get("customer_id")
        if not customer_id:
            return Response(
                {"error": "Customer id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        loans = Loan.objects.filter(customer=customer_id)
        response_data = []
        for loan in loans:
            repayment_left = loan.tenure - loan.emi_paid_on_time
            if repayment_left < 0:
                repayment_left = 0
            response_data.append(
                {
                    "loan_id": loan.id,
                    "loan_amount": loan.loan_amount,
                    "tenure": loan.tenure,
                    "interest_rate": loan.interest_rate,
                    "emi": loan.emi,
                    "repayment_left": repayment_left,
                }
            )
        return Response(response_data, status=status.HTTP_200_OK)
