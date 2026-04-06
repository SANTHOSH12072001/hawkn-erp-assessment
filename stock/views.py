from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from stock.permissions import CanApproveTransfer


from stock.models import StockTransfer, Stock
from stock.serializers import StockTransferSerializer, StockSerializer

# Create your views here.

class StockTransferAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = StockTransferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_by=request.user,
                status="PENDING"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
    def get(self, request):

        queryset=(StockTransfer.objects.select_related("source_branch", "destination_branch", "product", "created_by").order_by("-created_at"))
        source_branch=request.GET.get("source_branch")
        status_filter=request.GET.get("status_filter")

        if source_branch:
            queryset=queryset.filter(source_branch_id=source_branch)
        if status_filter:
            queryset=queryset.filter(status=status_filter)

        serializer=StockTransferSerializer(queryset, many=True)

        return Response(serializer.data)
        
class StockTransferApproveAPI(APIView):
    permission_classes = [IsAuthenticated , CanApproveTransfer]
    def post(self, request, pk):
        with transaction.atomic():
            transfer = StockTransfer.objects.select_for_update().get(pk=pk)

            if transfer.status == "APPROVED":
                return Response({"error": "transfer process already done"},status=status.HTTP_400_BAD_REQUEST)

            source_stock = Stock.objects.select_for_update().get(branch=transfer.source_branch,product=transfer.product)

            if source_stock.quantity < transfer.quantity:
                return Response({"error": "insufficient stock quantity"},status=status.HTTP_400_BAD_REQUEST)

            destination_stock, created = Stock.objects.get_or_create(
                branch=transfer.destination_branch,
                product=transfer.product,
                defaults={"quantity": 0}
            )

            source_stock.quantity -= transfer.quantity
            destination_stock.quantity += transfer.quantity

            source_stock.save()
            destination_stock.save()

            transfer.status = "APPROVED"
            transfer.approved_at = timezone.now()
            transfer.save()

            return Response({"message": "transferred successfully"},status=status.HTTP_200_OK)
        
class BranchStocksReportAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,branch_id):
        stocks=Stock.objects.filter(branch_id=branch_id).select_related('branch','product').order_by('product__name')
        serializer=StockSerializer(stocks, many=True)
        return Response(serializer.data)
    

