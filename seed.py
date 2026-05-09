# seed.py
from database import SessionLocal
from models import Product, Order

def seed_data():
    db = SessionLocal()
    
    # 1. Ürünleri Oluştur
    p1 = Product(name="Organik Çam Balı 1kg", stock_quantity=15)
    p2 = Product(name="Ev Yapımı Domates Salçası", stock_quantity=5)
    p3 = Product(name="Soğuk Sıkım Zeytinyağı 5L", stock_quantity=2) # Stoğu bitmek üzere olan ürün
    
    db.add_all([p1, p2, p3])
    db.commit()
    
    # 2. Siparişleri Oluştur
    # product_id=1 demek, 1 numaralı ürün (Çam Balı) sipariş edilmiş demek.
    o1 = Order(product_id=1, status="Hazırlanıyor")
    o2 = Order(product_id=2, status="Kargoda")
    
    db.add_all([o1, o2])
    db.commit()
    db.close()
    
    print("Harika! Sahte veriler veritabanına başarıyla eklendi!")

if __name__ == "__main__":
    seed_data()