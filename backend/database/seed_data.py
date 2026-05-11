from datetime import datetime, timedelta
import random

from database.connection import SessionLocal, init_db
from database.models import Customer, Product, Order, Payment


def seed_database():
    """
    Seeds the database with realistic sample data across all 4 tables.
    Run this once after init_db() to populate the schema.
    """
    db = SessionLocal()
    try:
        # ---- Customers (25 records) ----
        customers = [
            Customer(name="Alice Johnson", email="alice.j@example.com", city="New York"),
            Customer(name="Bob Smith", email="bob.smith@example.com", city="Los Angeles"),
            Customer(name="Carol White", email="carol.white@example.com", city="Chicago"),
            Customer(name="David Brown", email="david.b@example.com", city="Houston"),
            Customer(name="Eva Martinez", email="eva.m@example.com", city="Phoenix"),
            Customer(name="Frank Davis", email="frank.davis@example.com", city="Philadelphia"),
            Customer(name="Grace Wilson", email="grace.wilson@example.com", city="San Antonio"),
            Customer(name="Henry Taylor", email="henry.t@example.com", city="San Diego"),
            Customer(name="Ivy Anderson", email="ivy.a@example.com", city="Dallas"),
            Customer(name="Jack Thomas", email="jack.t@example.com", city="San Jose"),
            Customer(name="Kate Moore", email="kate.moore@example.com", city="Austin"),
            Customer(name="Leo Jackson", email="leo.jackson@example.com", city="Jacksonville"),
            Customer(name="Mia Martin", email="mia.martin@example.com", city="Fort Worth"),
            Customer(name="Noah Lee", email="noah.lee@example.com", city="Columbus"),
            Customer(name="Olivia Harris", email="olivia.h@example.com", city="Charlotte"),
            Customer(name="Peter Clark", email="peter.c@example.com", city="Indianapolis"),
            Customer(name="Quinn Lewis", email="quinn.l@example.com", city="Seattle"),
            Customer(name="Rita Walker", email="rita.w@example.com", city="Denver"),
            Customer(name="Sam Hall", email="sam.hall@example.com", city="Boston"),
            Customer(name="Tina Young", email="tina.y@example.com", city="Nashville"),
            Customer(name="Uma King", email="uma.king@example.com", city="Detroit"),
            Customer(name="Victor Wright", email="victor.w@example.com", city="Portland"),
            Customer(name="Wendy Scott", email="wendy.s@example.com", city="Las Vegas"),
            Customer(name="Xavier Green", email="xavier.g@example.com", city="Memphis"),
            Customer(name="Yara Baker", email="yara.baker@example.com", city="Louisville"),
        ]
        db.add_all(customers)
        db.flush()

        # ---- Products (20 records) ----
        products = [
            Product(name="Wireless Headphones", category="Electronics", price=79.99),
            Product(name="Mechanical Keyboard", category="Electronics", price=129.99),
            Product(name="USB-C Hub", category="Electronics", price=49.99),
            Product(name="4K Monitor", category="Electronics", price=449.99),
            Product(name="Ergonomic Mouse", category="Electronics", price=59.99),
            Product(name="Webcam HD", category="Electronics", price=89.99),
            Product(name="Smart Watch", category="Electronics", price=199.99),
            Product(name="Running Shoes", category="Sports", price=119.99),
            Product(name="Yoga Mat", category="Sports", price=34.99),
            Product(name="Dumbbells 20lb", category="Sports", price=69.99),
            Product(name="Tennis Racket", category="Sports", price=149.99),
            Product(name="Bicycle Helmet", category="Sports", price=44.99),
            Product(name="Coffee Maker", category="Home", price=89.99),
            Product(name="Air Purifier", category="Home", price=159.99),
            Product(name="Desk Lamp", category="Home", price=39.99),
            Product(name="Blender", category="Home", price=59.99),
            Product(name="Toaster Oven", category="Home", price=79.99),
            Product(name="Plant Pot Set", category="Home", price=24.99),
            Product(name="Cookbook: Healthy Meals", category="Books", price=19.99),
            Product(name="Programming Guide", category="Books", price=34.99),
        ]
        db.add_all(products)
        db.flush()

        # ---- Orders (40 records) ----
        statuses = ["completed", "processing", "shipped"]
        order_date_base = datetime.utcnow() - timedelta(days=90)

        for i in range(40):
            # Spread orders over the last 90 days
            days_ago = random.randint(0, 90)
            order_dt = order_date_base + timedelta(hours=random.randint(0, 23))
            order = Order(
                customer_id=random.choice(customers).id,
                product_id=random.choice(products).id,
                quantity=random.randint(1, 5),
                order_date=order_dt,
            )
            db.add(order)
        db.flush()

        # ---- Payments (40 records — one per order) ----
        all_products = db.query(Product).all()
        product_price = {p.id: float(p.price) for p in all_products}
        for order in db.query(Order).all():
            order_id = int(order.id)
            order_pid = int(order.product_id)
            order_qty = int(order.quantity)
            amount = round(product_price[order_pid] * order_qty, 2)
            payment = Payment(
                order_id=order.id,
                amount=amount,
                payment_date=order.order_date + timedelta(hours=random.randint(1, 72)),
            )
            db.add(payment)

        db.commit()
        print("[seed] Database seeded successfully.")
        print(f"  - {len(customers)} customers")
        print(f"  - {len(products)} products")
        print(f"  - 40 orders")
        print(f"  - 40 payments")

    except Exception as e:
        db.rollback()
        print(f"[seed] Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("[seed] Initializing database schema...")
    init_db()
    print("[seed] Schema created. Seeding data...")
    seed_database()