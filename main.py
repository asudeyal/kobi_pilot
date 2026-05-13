# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from ai_agent import ai_yanit_ver

from datetime import datetime, timedelta
import csv
import io
from fastapi.responses import Response

models.Base.metadata.create_all(bind=engine)

# Veritabanı Göçü (Migration): Eski siparişlerin tarihi boşsa şu anki tarihi ata
db = SessionLocal()
null_orders = db.query(models.Order).filter(models.Order.created_at == None).all()
for order in null_orders:
    order.created_at = datetime.utcnow()
if null_orders:
    db.commit()
db.close()

app = FastAPI(title="KOBİ-Pilot")

class MesajIstegi(BaseModel):
    mesaj: str
    rol: str = "Müşteri"

class AuthRequest(BaseModel):
    username: str
    password: str
    role: str = "musteri" # patron veya musteri

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/register")
def register(req: AuthRequest):
    # EKLENEN KISIM: Boşluk kontrolü
    if not req.username.strip() or not req.password.strip():
        raise HTTPException(status_code=400, detail="Kullanıcı adı ve şifre boş bırakılamaz!")

    db = SessionLocal()
    existing_user = db.query(models.User).filter(models.User.username == req.username).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten alınmış.")
    new_user = models.User(username=req.username, password=req.password, role=req.role)
    db.add(new_user)
    db.commit()
    db.close()
    return {"message": "Kayıt başarılı"}

@app.post("/login")
def login(req: AuthRequest):
    # EKLENEN KISIM: Boşluk kontrolü
    if not req.username.strip() or not req.password.strip():
        raise HTTPException(status_code=400, detail="Lütfen kullanıcı adı ve şifre giriniz.")

    db = SessionLocal()
    user = db.query(models.User).filter(models.User.username == req.username, models.User.password == req.password).first()
    db.close()
    if not user:
        raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre.")
    return {"message": "Giriş başarılı", "role": user.role}
@app.get("/api/dashboard")
def get_dashboard_data(period: str = "all"):
    db = SessionLocal()
    urunler = db.query(models.Product).all()
    
    query = db.query(models.Order)
    now = datetime.utcnow()
    if period == "bugun":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Order.created_at >= start_date)
    elif period == "bu-hafta":
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Order.created_at >= start_date)
    elif period == "bu-ay":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Order.created_at >= start_date)
        
    siparisler = query.all()
    
    toplam_siparis = len(siparisler)
    bekleyen_siparis = len([s for s in siparisler if s.status not in ["Teslim Edildi", "İptal"]])
    kritik_stok = [u.name for u in urunler if u.stock_quantity <= 5]
    
    # Grafik için sipariş durumlarının dağılımını hesaplıyoruz
    durumlar = {"Hazırlanıyor": 0, "Kargoda": 0, "Teslim Edildi": 0, "İptal": 0}
    for s in siparisler:
        if s.status in durumlar:
            durumlar[s.status] += 1
        else:
            durumlar[s.status] = 1
            
    db.close()
    return {
        "toplam_urun": len(urunler),
        "bekleyen_siparis": bekleyen_siparis,
        "kritik_stok_sayisi": len(kritik_stok),
        "kritik_stok_urunler": ", ".join(kritik_stok) if kritik_stok else "Yok",
        "siparis_dagilimi": durumlar # Grafiği besleyecek veri
    }

@app.get("/api/detay/bekleyen-kargolar")
def get_bekleyen_kargolar():
    db = SessionLocal()
    orders = db.query(models.Order, models.Product.name)\
               .join(models.Product, models.Order.product_id == models.Product.id)\
               .filter(models.Order.status.in_(["Hazırlanıyor", "Kargoda"])).all()
    db.close()
    
    result = []
    for order, product_name in orders:
        result.append({
            "id": order.id,
            "product_name": product_name,
            "status": order.status
        })
    return result

@app.get("/api/detay/kritik-stoklar")
def get_kritik_stoklar():
    db = SessionLocal()
    products = db.query(models.Product).filter(models.Product.stock_quantity <= 5).all()
    db.close()
    
    return [{"id": p.id, "name": p.name, "stock_quantity": p.stock_quantity} for p in products]

@app.get("/api/export/orders")
def export_orders(period: str = "all"):
    db = SessionLocal()
    query = db.query(models.Order, models.Product.name)\
              .join(models.Product, models.Order.product_id == models.Product.id)
    
    now = datetime.utcnow()
    if period == "bugun":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Order.created_at >= start_date)
    elif period == "bu-hafta":
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Order.created_at >= start_date)
    elif period == "bu-ay":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Order.created_at >= start_date)
        
    orders = query.all()
    db.close()
    
    output = io.StringIO()
    output.write('\ufeff') # Türkçe karakter (BOM) desteği
    writer = csv.writer(output, delimiter=';') # Sütunları bölmek için noktalı virgül
    writer.writerow(["Sipariş ID", "Ürün Adı", "Durum", "Tarih"])
    
    for order, product_name in orders:
        date_str = order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else ""
        writer.writerow([order.id, product_name, order.status, date_str])
        
    # Daha önce StreamingResponse eklendiği varsayılıyor ancak import listesinde hala Response kullanılmış.
    # Ben StreamingResponse veya Response ile dönmeyi koruyacağım, kullanıcının kodunu aynen devam ettiriyorum:
    output.seek(0)
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=orders_{period}.csv"})

@app.post("/sohbet")
def sohbet_et(istek: MesajIstegi):
    cevap = ai_yanit_ver(istek.mesaj, istek.rol)
    return {"ai_cevabi": cevap}

@app.get("/api/temizle")
def hafizayi_temizle():
    sohbet_gecmisini_temizle()
    return {"mesaj": "Sohbet hafızası başarıyla temizlendi."}