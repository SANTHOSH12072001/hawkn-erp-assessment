# Architecture / Deployment Notes

## Key Design Choices

* Built with **Django REST Framework + APIView** for better control over custom stock transfer and approval workflows.
* Used **separate models** for Branch, Product, Stock, and StockTransfer to keep inventory logic clean and scalable.
* Added **transaction.atomic() + select_for_update()** during approval to prevent duplicate approvals and stock mismatch.

## Trade-offs

* **SQLite** is used for quick local setup and assessment simplicity.
* For production, **Oracle** is better for enterprise-grade ERP systems with strong transaction support.

## Deployment

* **Backend:** Nginx + Gunicorn
* **Frontend:** React
* **Database:** Oracle
* **Static files:** Nginx

This design keeps the service **safe, simple, and suitable for real ERP use cases**.
