from celery import shared_task, chain
from celery.utils.log import get_task_logger
import pandas as pd

from core.models import Customer, Loan

logger = get_task_logger(__name__)


@shared_task
def add_customer_to_db(file_path):
    try:
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            customer = Customer.objects.create(
                first_name=row["First Name"],
                last_name=row["Last Name"],
                age=row["Age"],
                phone=row["Phone Number"],
                monthaly_salary=row["Monthly Salary"],
                approved_limit=row["Approved Limit"],
            )
            customer.save()

        return "Customer data added successfully"
    except Exception as e:
        logger.error(f"Error adding customer data: {e}")
        return "Error adding customer data"


@shared_task
def add_loan_to_db(file_path):
    try:
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            customer = Customer.objects.get(pk=row["Customer ID"])
            loan = Loan.objects.create(
                customer=customer,
                loan_amount=row["Loan Amount"],
                tenure=row["Tenure"],
                interest_rate=row["Interest Rate"],
                emi=row["Monthly payment"],
                emi_paid_on_time=row["EMIs paid on Time"],
                start_date=row["Date of Approval"],
                end_date=row["End Date"],
            )
            loan.save()

        return "Loan data added successfully"
    except Exception as e:
        logger.error(f"Error adding loan data: {e}")
        return "Error adding loan data"


# Chain the tasks
@shared_task
def process_data(file_path):
    # Chain the tasks: add_customer_to_db -> add_loan_to_db
    result = chain(add_customer_to_db.s(file_path), add_loan_to_db.s(file_path))()

    return result.get()
