import threading
import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tradexa_project.settings")
django.setup()


from user_db_tradexa.models import User, Product, Order
from user_db_tradexa.insert_values import users_data, products_data, orders_data


def insert_users():
    for id_, name, email in users_data:
        if not email:
            continue
        if not User.objects.using("users").filter(name= name).exists():
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
            continue

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
