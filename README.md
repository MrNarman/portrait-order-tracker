# Portrait Order Tracker

A command-line order management system built for a portrait commission business, written in Python with JSON file storage. Built as a self-directed learning project to practice layered application architecture — separating storage, business rules, and orchestration into distinct, testable components rather than one flat script.

## Features

- **Create orders** — captures client details, size/subject specs, and add-ons (framing, rush, lamination, digital scan), with pricing calculated automatically from a rate table
- **Track order status** — moves orders through a defined lifecycle (`INQUIRY → CONFIRMED → IN_PROGRESS → COMPLETED → DELIVERED`, with `CANCELLED` as a branch), validated against a fixed set of legal transitions
- **Record payments** — tracks deposits and balances, automatically flipping payment status between `UNPAID`, `DEPOSIT`, and `PAID`
- **Search and filter** — find orders by status, client name (case-insensitive), or both
- **Dashboard view** — total order count, total pending balance, and a breakdown of orders by status

## Architecture

The project is split into layers, each with a single responsibility:

| File | Responsibility |
|---|---|
| `storage.py` | Reads and writes `data/orders.json`. The only file that touches disk. Falls back to a fresh empty dataset if the file is missing or corrupted. |
| `models.py` | Defines the shape of an order, the pricing table, the valid status-transition rules, and payment-status logic. Pure functions — no file I/O. |
| `orders_service.py` | Orchestrates order operations: `create_order`, `find_order`, `update_status`, `filter_orders`. Combines `models.py` logic with `storage.py` persistence. |
| `payments_service.py` | Handles `record_payment`, updating an order's balance and payment status. |
| `display.py` | Formats orders and summaries for terminal output. No business logic. |
| `main.py` | The CLI menu loop. Reads user input and delegates to the service layers — contains no business rules of its own. |

This separation means, for example, that pricing rules can be tested and changed without touching how data is saved, and the storage format could be swapped out later without any of the order logic needing to change.

## Data model

Each order is stored as a JSON object with:

- Identity — `order_id`, `created_date`
- Client info — `client_name`, `contact`
- Specs — `size`, `subject_type`, and add-on flags
- Pricing — `total`, `deposit_paid`, `balance`, `payment_status`
- Status — current `status`, plus a full `status_history` log

See `data/sample_orders.json` for a reference file showing the complete schema across a few different order states.

## Getting started

```bash
python main.py
```

On first run, if `data/orders.json` doesn't exist yet, the app starts with an empty dataset automatically — no setup required. To explore the app with example data first, copy `data/sample_orders.json` to `data/orders.json` before running.

## Project status

Core functionality is complete: all CRUD operations, pricing, status transitions, payment tracking, search, and the CLI are built and manually tested end-to-end.

Possible next steps:
- Automated tests (currently tested manually per function)
- Edge-case hardening (duplicate order IDs, invalid CLI input)
- Order class refactor (currently plain dicts)