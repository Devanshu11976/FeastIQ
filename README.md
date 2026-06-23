# FeastIQ - Restaurant Order and Feedback Management System

A full-stack restaurant management system with customer ordering, feedback collection, and admin analytics dashboard.

## Tech Stack

- **Backend**: Python, Flask, PostgreSQL, SQLAlchemy, Flask-JWT-Extended, Flask-Migrate
- **Frontend**: Bootstrap 5, Chart.js, Vanilla JavaScript
- **Database**: PostgreSQL

## Features

### Customer Features
- Browse menu items by category
- Add items to cart and place orders
- Track order status in real-time
- Submit feedback for delivered orders

### Admin Features
- JWT-based authentication
- Menu management (CRUD operations)
- Order management with status updates
- Feedback viewing and filtering
- Analytics dashboard with charts:
  - Daily orders trend
  - Rating distribution
  - Customer segments (VIP, Regular, Occasional, Inactive)
  - Popular items
  - Loyalty metrics

## Project Structure

```
FeastIQ/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── models/
│   │   │   ├── customer.py
│   │   │   ├── menu_item.py
│   │   │   ├── order.py
│   │   │   ├── order_item.py
│   │   │   ├── feedback.py
│   │   │   └── admin_user.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── menu.py
│   │   │   ├── orders.py
│   │   │   ├── feedback.py
│   │   │   └── analytics.py
│   │   └── services/
│   │       ├── order_service.py
│   │       ├── segmentation_service.py
│   │       └── analytics_service.py
│   ├── migrations/
│   ├── .env
│   ├── requirements.txt
│   ├── run.py
│   └── seed_data.py
└── frontend/
    ├── customer/
    │   ├── index.html
    │   ├── order.html
    │   ├── status.html
    │   └── feedback.html
    └── admin/
        ├── login.html
        ├── dashboard.html
        ├── orders.html
        ├── feedback.html
        └── customers.html
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**
   - Create a database named `restaurant_db`
   - Update the `DATABASE_URL` in `.env` file with your PostgreSQL credentials

5. **Initialize database and seed data**
   ```bash
   python seed_data.py
   ```

6. **Run the Flask server**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:5000`

### Frontend Setup

The frontend is static HTML files. You can serve them using any static file server:

**Option 1: Using Python**
```bash
cd frontend
python -m http.server 8000
```

**Option 2: Using VS Code Live Server extension**
- Install the Live Server extension
- Right-click on `index.html` and select "Open with Live Server"

### Access the Application

**Customer Interface**
- Menu: `http://localhost:8000/customer/index.html`
- Order: `http://localhost:8000/customer/order.html`
- Status: `http://localhost:8000/customer/status.html`
- Feedback: `http://localhost:8000/customer/feedback.html`

**Admin Dashboard**
- Login: `http://localhost:8000/admin/login.html`
- Dashboard: `http://localhost:8000/admin/dashboard.html`
- Orders: `http://localhost:8000/admin/orders.html`
- Feedback: `http://localhost:8000/admin/feedback.html`
- Customers: `http://localhost:8000/admin/customers.html`

## Default Admin Users

After seeding the database, you can login with these credentials:

- **Username**: `admin`, **Password**: `admin123`
- **Username**: `manager`, **Password**: `manager123`
- **Username**: `supervisor`, **Password**: `super123`

## API Endpoints

### Authentication
- `POST /auth/login` - Admin login (returns JWT token)

### Menu
- `GET /menu` - Get all available menu items
- `GET /menu?category=Pizza` - Filter by category
- `POST /menu` - Add new menu item (Admin only)
- `PUT /menu/<id>` - Update menu item (Admin only)
- `DELETE /menu/<id>` - Soft delete menu item (Admin only)

### Orders
- `POST /orders` - Create new order
- GET /orders - Get all orders (Admin only, paginated)
- `GET /orders/<id>` - Get specific order
- `PATCH /orders/<id>/status` - Update order status (Admin only)

### Feedback
- `POST /feedback` - Submit feedback
- `GET /feedback` - Get all feedback (Admin only, paginated)
- `GET /feedback/order/<order_id>` - Get feedback for specific order

### Analytics
- `GET /analytics/orders` - Order analytics
- `GET /analytics/feedback` - Feedback analytics
- `GET /analytics/segments` - Customer segment counts
- `GET /analytics/loyalty` - Loyalty metrics

## Business Rules

- Order totals are calculated server-side (never trust client data)
- Unit prices are snapshotted at order time to protect against menu price changes
- Feedback is only allowed on delivered orders (one per order)
- Status transitions are strictly enforced (pending → confirmed → preparing → ready → delivered)
- All list endpoints support pagination (`?page=1&per_page=20`)

## Customer Segmentation

Customers are automatically segmented based on their order history (last 90 days):

- **VIP**: 10+ orders OR average order value ≥ ₹1000
- **Regular**: 4-9 orders AND average order value ₹400-₹999
- **Occasional**: 1-3 orders
- **Inactive**: 0 orders in last 90 days

## License

This project is for educational purposes.
