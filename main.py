# main.py
from fastapi import FastAPI
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

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

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

@app.post("/sohbet")
def sohbet_et(istek: MesajIstegi):
    cevap = ai_yanit_ver(istek.mesaj, istek.rol)
    return {"ai_cevabi": cevap}

@app.get("/api/temizle")
def hafizayi_temizle():
    sohbet_gecmisini_temizle()
    return {"mesaj": "Sohbet hafızası başarıyla temizlendi."}