from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["shop_db"]

products = db["products"]
sales = db["sales"]

# ----------- FUNCTIONS -----------

# Add Product
def add_product():
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))

    product = {
        "name": name,
        "price": price,
        "stock": stock
    }

    products.insert_one(product)
    print("✅ Product Added!\n")


# View Products
def view_products():
    print("\n📦 Product List:\n")
    for p in products.find():
        print(f"Name: {p['name']}")
        print(f"Price: ₹{p['price']}")
        print(f"Stock: {p['stock']}")
        print("-------------------")


# Buy Product (Generate Bill)
def buy_product():
    name = input("Enter Product Name: ")
    qty = int(input("Enter Quantity: "))

    product = products.find_one({"name": name})

    if product:
        if product["stock"] >= qty:
            total = product["price"] * qty

            # Update stock
            products.update_one(
                {"name": name},
                {"$set": {"stock": product["stock"] - qty}}
            )

            # Save sale
            sale = {
                "product": name,
                "quantity": qty,
                "total": total
            }
            sales.insert_one(sale)

            print(f"🧾 Bill Generated: ₹{total}")
        else:
            print("❌ Not enough stock")
    else:
        print("❌ Product not found")


# Delete Product
def delete_product():
    name = input("Enter Product Name to Delete: ")
    result = products.delete_one({"name": name})

    if result.deleted_count > 0:
        print("✅ Product Deleted")
    else:
        print("❌ Product Not Found")


# View Sales
def view_sales():
    print("\n📊 Sales History:\n")
    for s in sales.find():
        print(f"Product: {s['product']}")
        print(f"Qty: {s['quantity']}")
        print(f"Total: ₹{s['total']}")
        print("-------------------")


# ----------- MENU -----------

while True:
    print("\n===== 🛒 SHOP MANAGEMENT SYSTEM =====")
    print("1. Add Product")
    print("2. View Products")
    print("3. Buy Product")
    print("4. Delete Product")
    print("5. View Sales")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_product()
    elif choice == "2":
        view_products()
    elif choice == "3":
        buy_product()
    elif choice == "4":
        delete_product()
    elif choice == "5":
        view_sales()
    elif choice == "6":
        print("👋 Exit")
        break
    else:
        print("❌ Invalid choice")
