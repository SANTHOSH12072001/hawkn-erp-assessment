from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

from stock.models import Branch, Product, Stock, StockTransfer


class StockTransferTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="demo",
            password="demo123",
            is_staff=True
        )

        self.client.force_authenticate(user=self.user)

        self.branch1 = Branch.objects.create(
            name="cuddalore",
            location="Tamil Nadu"
        )

        self.branch2 = Branch.objects.create(
            name="chennai",
            location="Tamil Nadu"
        )

        self.product = Product.objects.create(
            name="OPPO",
            sku="OPPO-A52"
        )

        self.stock = Stock.objects.create(
            branch=self.branch1,
            product=self.product,
            quantity=20
        )

    def test_Transfer(self):
        transfer = StockTransfer.objects.create(
            source_branch=self.branch1,
            destination_branch=self.branch2,
            product=self.product,
            quantity=5,
            created_by=self.user
        )

        response = self.client.post(f"/api/transfers/{transfer.id}/approve/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 15)

    def test_non_staff_cannot_approve(self):
        normal_user = User.objects.create_user(
            username="user1",
            password="pass123"
        )

        self.client.force_authenticate(user=normal_user)

        transfer = StockTransfer.objects.create(
            source_branch=self.branch1,
            destination_branch=self.branch2,
            product=self.product,
            quantity=5,
            created_by=normal_user
        )

        response = self.client.post(
            f"/api/transfers/{transfer.id}/approve/"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_insufficient(self):
        transfer = StockTransfer.objects.create(
            source_branch=self.branch1,
            destination_branch=self.branch2,
            product=self.product,
            quantity=26,
            created_by=self.user
        )

        response = self.client.post(f"/api/transfers/{transfer.id}/approve/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_approve(self):
        transfer = StockTransfer.objects.create(
            source_branch=self.branch1,
            destination_branch=self.branch2,
            product=self.product,
            quantity=5,
            created_by=self.user
        )

        self.client.post(f"/api/transfers/{transfer.id}/approve/")
        response = self.client.post(f"/api/transfers/{transfer.id}/approve/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stock_report(self):
        response = self.client.get(
            f"/api/branches/{self.branch1.id}/stock-summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transfer_history(self):
        response = self.client.get("/api/transfers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
