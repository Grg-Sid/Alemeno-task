from django.utils import timezone
from core.models import Loan, Customer


def get_sum_of_loan_amount(customer_id) -> int:
    loans = Loan.objects.filter(customer=customer_id)
    sum_of_loan_amount = sum([loan.loan_amount for loan in loans])
    return sum_of_loan_amount


def check_loan_approval(customer_id, loan_amount) -> bool:
    customer = Customer.objects.get(pk=customer_id)
    sum_of_loan_amount = get_sum_of_loan_amount(customer_id=customer_id)
    credit_rating = get_credit_rating(customer_id=customer_id)
    if sum_of_loan_amount + loan_amount > customer.approved_limit:
        return False
    if credit_rating < 10:
        return False
    return True


def corrected_interest_rate(customer_id) -> int:
    corrected_interest_rate = 12
    credit_rating = get_credit_rating(customer_id=customer_id)
    if credit_rating > 50:
        corrected_interest_rate = 8
    if 50 > credit_rating > 30:
        corrected_interest_rate = 12
    if 30 > credit_rating > 10:
        corrected_interest_rate = 16
    print(credit_rating, corrected_interest_rate)
    return corrected_interest_rate


def calculate_monthaly_installment(loan_amount, tenure, interest_rate) -> int:
    monthly_interest_rate = interest_rate / (12 * 100)
    monthly_installment = (
        loan_amount
        * monthly_interest_rate
        * (1 + monthly_interest_rate) ** tenure
        / ((1 + monthly_interest_rate) ** tenure - 1)
    )
    return monthly_installment


def get_current_debt(customer_id) -> int:
    loans = Loan.objects.filter(customer=customer_id)
    current_debt = sum([loan.emi * loan.tenure for loan in loans])
    current_debt = current_debt - sum(
        [loan.emi_paid_on_time * loan.emi for loan in loans]
    )
    return current_debt


def get_credit_rating(customer_id) -> int:
    credit_score = 100
    customer = Customer.objects.get(pk=customer_id)
    current_debt = get_current_debt(customer_id=customer_id)
    customer_loan = Loan.objects.filter(customer=customer_id)
    total_loans = customer_loan.count()
    current_year_loan_taken = customer_loan.filter(
        start_date__year=timezone.now().year
    ).count()
    active_loans = 0
    if current_debt > customer.approved_limit:
        print(credit_score)
        return 0
    if current_year_loan_taken:
        credit_score -= 7.5 * current_year_loan_taken
    if active_loans:
        credit_score -= 5 * active_loans
    if total_loans:
        credit_score -= 5 * total_loans
    # return 69
    return credit_score if credit_score > 0 else 0
