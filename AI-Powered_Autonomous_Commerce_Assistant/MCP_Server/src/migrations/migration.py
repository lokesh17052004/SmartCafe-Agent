from src.repository.database import engine, Base, get_db
from src.repository.schema import MenuItemSchema, Customer

def _run_migrations() -> None:
    print("[Migration] Starting database migration...")
    Base.metadata.create_all(bind=engine)
    print("[Migration] Tables created successfully:")

def _run_seed() -> None:
    print("[Seed] Starting data seeding...")
    with get_db() as session:
        if session.query(MenuItemSchema).first():
            print("Menu items already exist. Skipping seed.")
            return
        items =  [
            MenuItemSchema(item_name= "Espresso",description= "Strong and bold espresso shot",item_price= 180.00,tax_rate= 5.0,stock=50,is_active= True,created_by= "SYSTEM"),
            MenuItemSchema(item_name= "Cappuccino",description= "Espresso with steamed milk and foam",item_price= 250.00,tax_rate= 5.0,stock= 40,is_active= True,created_by= "SYSTEM"),
            MenuItemSchema(item_name= "Latte",description= "Smooth espresso with steamed milk",item_price= 260.00,tax_rate= 5.0,stock= 35,is_active= True,created_by= "SYSTEM"),
            MenuItemSchema(item_name= "Iced Mocha",description= "Chilled espresso with chocolate and milk",item_price= 290.00,tax_rate= 5.0,stock=25,is_active= True,created_by="SYSTEM"),
            MenuItemSchema(item_name= "Cold Brew",description= "Slow brewed coffee served cold",item_price=240.00,tax_rate= 5.0,stock= 30,is_active= True,created_by= "SYSTEM"),
            MenuItemSchema(item_name= "Matcha Latte",description= "Green tea latte with milk",item_price= 270.00,tax_rate= 5.0,stock= 20,is_active= True,created_by= "SYSTEM")
        ]
        session.add_all(items)

        if session.query(Customer).first():
            return 
        customers=[
            Customer(customer_name= "Lokesh",mobile_number="+91 99955 85858"),
            Customer(customer_name= "Alice",mobile_number="+91 99955 87878"),
            Customer(customer_name= "Bob",mobile_number="+91 99955 20202"),
            Customer(customer_name= "Charlie",mobile_number="+91 99955 10101"),
            Customer(customer_name= "Sekar",mobile_number="+91 99955 98765"),
            Customer(customer_name= "Rizhwan",mobile_number="+91 99955 85857"),
        ]
        session.add_all(customers)
        session.commit()





def run_migration_and_seed() -> None:
    _run_migrations()
    _run_seed()
    print("[Setup] Migration and seeding complete.")


