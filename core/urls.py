from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import (
    background_task,
    CustomerViewSet,
    CheckLoanView,
    CustomerLoanView,
    LoanViewSet,
    LoanView,
)

router = DefaultRouter()

router.register("register", CustomerViewSet, basename="register")
router.register("create-loan", LoanViewSet, basename="loan")

urlpatterns = [
    path("", include(router.urls)),
    path("background-task/", background_task, name="background-task"),
    path("check-eligibility/", CheckLoanView.as_view(), name="check-eligibility"),
    path("view-loan/<int:loan_id>/", LoanView.as_view(), name="view-loan"),
    path(
        "view-loans/<int:customer_id>/", CustomerLoanView.as_view(), name="view-loans"
    ),
]
