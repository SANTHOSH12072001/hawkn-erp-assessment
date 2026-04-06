from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from stock.views import StockTransferAPI, StockTransferApproveAPI, BranchStocksReportAPI

urlpatterns=[
    path("token/", obtain_auth_token),
    path("transfers/", StockTransferAPI.as_view()),
    path("transfers/<int:pk>/approve/", StockTransferApproveAPI.as_view()),
    path("branches/<int:branch_id>/stock-summary/", BranchStocksReportAPI.as_view()),
]