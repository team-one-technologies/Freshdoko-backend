# FreshDoko Backend

FreshDoko is an organic food supply platform integrating **real-time weather data, user preferences, and nutritional information** to provide **personalized food recommendations**. The backend is built using **Django** and supports **payment processing (Khalti & Payoneer), order tracking, and shop owner dashboards**.

## **Features**
### User Management
User authentication using JWT tokens.
Support for Google and Facebook login via OAuth.
Role-based access control (shop owner and customer).
User registration, login, and password reset.

#### Product Management

CRUD operations for products (for shop owners).
Product listing with search and pagination.
Product details view (description, price, stock, etc.).

### Cart Operations
Add/remove products to/from the cart.
View cart contents, quantity, and total price.
Checkout process with price calculation (including taxes and shipping).

### Payment Gateway Integration
- Secure payment processing via **Khalti** and **Payoneer APIs**
- Payment status tracking (**Success, Pending, Failed**)
- Webhook support for real-time status updates

### Shop Owner Dashboard
- View **total sales, sales by date, and top-selling products**
- Customer details with **order history and contact information**

### Authentication & Security
- **Django authentication system** for user management
- **CORS and session authentication** for secure API calls
- **HTTPS and API key protection**

## **Tech Stack**
- **Backend:** Django, Django REST Framework (DRF)
- **Database:** PostgreSQL (or MongoDB for NoSQL support)
- **Payment APIs:** Khalti, Payoneer
- **Deployment:** DigitalOcean (Optional: AWS, GCP)

## **Installation & Setup**

### **1. Clone the Repository**
```sh
git clone https://github.com/yourusername/freshdoko-backend.git
cd freshdoko-backend
```

### **2. Create a Virtual Environment & Install Dependencies**
```sh
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
pip install -r requirements.txt
```

### **3. Configure Environment Variables**
Create a `.env` file and add the required secrets:
```
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/freshdoko_db
KHALTI_SECRET_KEY=your_khalti_secret_key
PAYONEER_API_KEY=your_payoneer_api_key
```

### **4. Apply Migrations & Start the Server**
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

The backend will now run at: `http://127.0.0.1:8000/`

## **API Endpoints**

### **Payment APIs**
| Method | Endpoint | Description |
|--------|------------|-------------|
| POST | `/api/payment/khalti/` | Process payment via Khalti |
| POST | `/api/payment/payoneer/` | Process payment via Payoneer |
| GET | `/api/payment/status/` | Get payment status |

### **Dashboard APIs**
| Method | Endpoint | Description |
|--------|------------|-------------|
| GET | `/api/dashboard/sales/` | Get shop owner sales dashboard |
| GET | `/api/dashboard/customers/` | Get customer order history |

## **Deployment**
### **Using DigitalOcean**
1. Create a **Droplet** (Ubuntu 22.04 recommended)
2. Install **Docker, PostgreSQL, and Gunicorn**
3. Run the Django app using **Gunicorn & Nginx**

```sh
gunicorn --workers 3 --bind 0.0.0.0:8000 freshdoko.wsgi:application
```

### **Using Digtial Ocean**
- Configure **PostgreSQL RDS** 
- Use **Cloud Run** for serverless deployment

## **Contributing**
- Fork the repository and create a new branch.
- Implement your changes and create a pull request.
- Follow PEP 8 guidelines for coding standards.

## **License**
This project is licensed under the MIT License - see the LICENSE file for details.



