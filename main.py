# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from ai_agent import ai_yanit_ver

models.Base.metadata.create_all(bind=engine)

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
def get_dashboard_data():
    db = SessionLocal()
    urunler = db.query(models.Product).all()
    siparisler = db.query(models.Order).all()
    
    toplam_siparis = len(siparisler)
    bekleyen_siparis = len([s for s in siparisler if s.status not in ["Teslim Edildi", "İptal"]])
    kritik_stok = [u.name for u in urunler if u.stock_quantity <= 5]
    
    # YENİ: Grafik için sipariş durumlarının dağılımını hesaplıyoruz
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

@app.post("/sohbet")
def sohbet_et(istek: MesajIstegi):
    cevap = ai_yanit_ver(istek.mesaj, istek.rol)
    return {"ai_cevabi": cevap}

@app.get("/api/temizle")
def hafizayi_temizle():
    sohbet_gecmisini_temizle()
    return {"mesaj": "Sohbet hafızası başarıyla temizlendi."}