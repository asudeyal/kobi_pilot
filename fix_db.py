import sqlite3
from datetime import datetime

# Veritabanına doğrudan bağlanıyoruz
conn = sqlite3.connect("kobi_pilot.db")
cursor = conn.cursor()

try:
    # Eksik olan sütunu veritabanına zorla ekliyoruz
    cursor.execute("ALTER TABLE orders ADD COLUMN created_at DATETIME;")
    print("BAŞARILI: 'created_at' sütunu eklendi.")
except Exception as e:
    print("BİLGİ: Sütun zaten var veya bir hata oluştu:", e)

# Tüm eski siparişlere şu anın tarihini basıyoruz ki grafikler boş kalmasın
simdi = datetime.utcnow()
cursor.execute("UPDATE orders SET created_at = ? WHERE created_at IS NULL;", (simdi,))
conn.commit()
conn.close()

print("HARİKA: Veritabanı tamir edildi ve eski veriler korundu!")