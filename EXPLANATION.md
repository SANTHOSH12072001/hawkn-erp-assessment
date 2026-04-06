# Project Design Explanation

##  Problem Statement
The project simulates an ERP inventory workflow where stock is moved from one branch to another safely.

---

##  Core Models
### Branch
Stores branch name and location.

### Product
Stores product name and unique SKU.

### Stock
Stores branch-product quantity.

**Constraint:** one stock row per branch + product.

### StockTransfer
Stores transfer request lifecycle:
- PENDING
- APPROVED

Tracks:
- source branch
- destination branch
- product
- quantity
- created_by
- created_at

---

##  Authentication & Authorization
- Global authentication via DRF Token Authentication
- `IsAuthenticated` applied globally
- Custom permission for approval endpoint
- Only staff users can approve transfers

---

##  Concurrency Safety
Approval logic uses:
- `transaction.atomic()`
- `select_for_update()`

This ensures:
- no race conditions
- safe stock deduction
- duplicate approval prevention

---

##  Performance Optimization
Used `select_related()` in transfer history and stock summary APIs to avoid **N+1 query issues**.

---

##  Testing Strategy
Covered:
- successful transfer approval
- insufficient stock
- duplicate approval
- stock summary
- transfer history
- non-staff authorization restriction

---

##  Frontend Scope
React UI intentionally kept minimal because backend correctness is the primary evaluation criteria.

Implemented screens:
- login
- create transfer
- approve transfer
- stock summary

---

##  Assumptions
- Branch names are unique by name + location
- SKU is globally unique
- Only staff can approve
- SQLite used for assessment simplicity

---

##  Final Note
The project prioritizes **correctness, concurrency safety, authorization, and testability**, matching the assessment requirements.
