from rest_framework import serializers
from stock.models import StockTransfer, Stock


class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model=StockTransfer
        fields="__all__"
        read_only_fields=("status","created_by","created_at","approve_at")

    def validate(self, attrs):
        if attrs["source_branch"] == attrs["destination_branch"]:
            raise serializers.ValidationError("Source and Destination Branch cannot be same")
        if attrs["quantity"] < 0:
            raise serializers.ValidationError("Quantity must be greater than zero ")
        return attrs
    

class StockSerializer(serializers.ModelSerializer):

    branch_name = serializers.CharField(source="branch.name", read_only=True)
    product_name=serializers.CharField(source="product.name", read_only=True)
    sku=serializers.CharField(source="product.sku", read_only=True)

    class Meta:
        model=Stock
        fields = (
            "id",
            "branch",
            "branch_name",
            "product",
            "product_name",
            "sku",
            "quantity",
        )