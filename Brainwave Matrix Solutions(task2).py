import json
import hashlib



def load_users():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}



def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        print("Username already exists!")
        return False
    users[username] = hash_password(password)
    save_users(users)
    print("User registered successfully!")
    return True


def authenticate_user(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False

def load_products():
    try:
        with open('products.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_products(products):
    with open('products.json', 'w') as file:
        json.dump(products, file)

def add_product(name, quantity, price):
    products = load_products()
    product_id = len(products) + 1
    products.append({"id": product_id, "name": name, "quantity": quantity, "price": price})
    save_products(products)
    print(f"Product '{name}' added successfully!")


def edit_product(product_id, name, quantity, price):
    products = load_products()
    for product in products:
        if product['id'] == product_id:
            product['name'] = name
            product['quantity'] = quantity
            product['price'] = price
            break
    save_products(products)
    print(f"Product ID {product_id} edited successfully!")

def delete_product(product_id):
    products = load_products()
    products = [product for product in products if product['id'] != product_id]
    save_products(products)
    print(f"Product ID {product_id} deleted successfully!")

def get_all_products():
    return load_products()

def low_stock_alert(threshold=5):
    products = load_products()
    return [product for product in products if product['quantity'] <= threshold]

if __name__ == "__main__":
    # User Registration and Authentication
    username = input("Enter username: ")
    password = input("Enter password: ")

    if not register_user(username, password):
        print("Trying to authenticate...")
        if authenticate_user(username, password):
            print("Login successful!")
        else:
            print("Login failed!")
    
    # Inventory Management
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Edit Product")
        print("3. Delete Product")
        print("4. View All Products")
        print("5. Low Stock Alert")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            quantity = int(input("Enter product quantity: "))
            price = float(input("Enter product price: "))
            add_product(name, quantity, price)
        elif choice == '2':
            product_id = int(input("Enter product ID to edit: "))
            name = input("Enter new product name: ")
            quantity = int(input("Enter new product quantity: "))
            price = float(input("Enter new product price: "))
            edit_product(product_id, name, quantity, price)
        elif choice == '3':
            product_id = int(input("Enter product ID to delete: "))
            delete_product(product_id)
        elif choice == '4':
            products = get_all_products()
            print("\nAll Products:")
            for product in products:
                print(f"ID: {product['id']}, Name: {product['name']}, Quantity: {product['quantity']}, Price: {product['price']}")
        elif choice == '5':
            threshold = int(input("Enter low stock threshold: "))
            low_stock_products = low_stock_alert(threshold)
            print("\nLow Stock Products:")
            for product in low_stock_products:
                print(f"ID: {product['id']}, Name: {product['name']}, Quantity: {product['quantity']}, Price: {product['price']}")
        elif choice == '6':
            break
        else:
            print("Invalid choice! Please try again.")
