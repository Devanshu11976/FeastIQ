from app import create_app
from app.extensions import db
from app.models import MenuItem, AdminUser

def seed_data():
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Seed menu items
        menu_items = [
            # Burgers
            {'name': 'Classic Burger', 'category': 'Burgers', 'price': 199},
            {'name': 'Cheese Burger', 'category': 'Burgers', 'price': 229},
            {'name': 'Double Patty Burger', 'category': 'Burgers', 'price': 299},
            
            # Pizza
            {'name': 'Margherita Pizza', 'category': 'Pizza', 'price': 349},
            {'name': 'Pepperoni Pizza', 'category': 'Pizza', 'price': 399},
            {'name': 'BBQ Chicken Pizza', 'category': 'Pizza', 'price': 449},
            
            # Drinks
            {'name': 'Coca Cola', 'category': 'Drinks', 'price': 49},
            {'name': 'Fresh Lime Soda', 'category': 'Drinks', 'price': 79},
            {'name': 'Mango Smoothie', 'category': 'Drinks', 'price': 129},
            
            # Sides
            {'name': 'French Fries', 'category': 'Sides', 'price': 99},
            {'name': 'Onion Rings', 'category': 'Sides', 'price': 119},
            {'name': 'Garlic Bread', 'category': 'Sides', 'price': 89},
            
            # Desserts
            {'name': 'Chocolate Brownie', 'category': 'Desserts', 'price': 149},
            {'name': 'Ice Cream Sundae', 'category': 'Desserts', 'price': 179},
            {'name': 'Cheesecake', 'category': 'Desserts', 'price': 199},
        ]
        
        for item_data in menu_items:
            existing = MenuItem.query.filter_by(name=item_data['name']).first()
            if not existing:
                item = MenuItem(**item_data)
                db.session.add(item)
        
        # Seed admin users
        admins = [
            {'username': 'admin', 'password': 'admin123'},
            {'username': 'manager', 'password': 'manager123'},
            {'username': 'supervisor', 'password': 'super123'},
        ]
        
        for admin_data in admins:
            existing = AdminUser.query.filter_by(username=admin_data['username']).first()
            if not existing:
                admin = AdminUser(username=admin_data['username'])
                admin.set_password(admin_data['password'])
                db.session.add(admin)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
