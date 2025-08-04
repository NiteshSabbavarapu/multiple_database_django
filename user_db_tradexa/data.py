import threading
import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tradexa_project.settings")
django.setup()





from user_db_tradexa.models import User, Product, Order

users_data = [
    (1, "Alice", "alice@example.com"),
    (2, "Bob", "bob@example.com"),
    (3, "Charlie", "charlie@example.com"),
    (4, "David", "david@example.com"),
    (5, "Eve", "eve@example.com"),
    (6, "Frank", "frank@example.com"),
    (7, "Grace", "grace@example.com"),
    (8, "Alice", "alice@example.com"),
    (9, "Henry", "henry@example.com"),
    (10, "Jane", "jane@example.com")
]

products_data = [
    (1, "Laptop", 1000.00),
    (2, "Smartphone", 700.00),
    (3, "Headphones", 150.00),
    (4, "Monitor", 300.00),
    (5, "Keyboard", 50.00),
    (6, "Mouse", 30.00),
    (7, "Laptop", 1000.00),
    (8, "Smartwatch", 250.00),
    (9, "Gaming Chair", 500.00),
    (10, "Earbuds", -50.00)
]

orders_data = [
    (1, 1, 1, 2),
    (2, 2, 2, 1),
    (3, 3, 3, 5),
    (4, 4, 4, 1),
    (5, 5, 5, 3),
    (6, 6, 6, 4),
    (7, 7, 7, 2),
    (8, 8, 8, 0),
    (9, 9, 1, -1),
    (10, 10, 11, 2)
]

def insert_users():
    for id_, name, email in users_data:
        if not email:
            continue
        if not User.objects.using("users").filter(id=id_).exists():
            User.objects.using("users").create(id=id_, name=name, email=email)

def insert_products():
    for id_, name, price in products_data:
        if price < 0:
            continue
        if not Product.objects.using("products").filter(id=id_).exists():
            Product.objects.using("products").create(id=id_, name=name, price=price)


def insert_orders():
    for id_, user_id, product_id, quantity in orders_data:
        if quantity <= 0:
            continue

        if Order.objects.using("orders").filter(id=id_).exists():
            continue  # Skip if already exists

        try:
            user = User.objects.using('users').get(id=user_id)
            product = Product.objects.using('products').get(id=product_id)
        except User.DoesNotExist:
            print(f"User {user_id} not found")
            continue
        except Product.DoesNotExist:
            print(f"Product {product_id} not found")
            continue

        Order.objects.using('orders').create(
            id=id_,
            user_id=user.id,
            product_id=product.id,
            quantity=quantity
        )


def show_all_data():
    print("Users:")
    for u in User.objects.using('users').all():
        print(u.id, u.name, u.email)

    print("\nProducts:")
    for p in Product.objects.using('products').all():
        print(p.id, p.name, p.price)

    print("\nOrders:")
    for o in Order.objects.using('orders').all():
        print(o.id, o.user_id, o.product_id, o.quantity)

def main():
    t1 = threading.Thread(target=insert_users)
    t2 = threading.Thread(target=insert_products)
    t3 = threading.Thread(target=insert_orders)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    t3.start()
    t3.join()

    show_all_data()

if __name__ == "__main__":
    main()
