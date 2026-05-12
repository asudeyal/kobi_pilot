# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
import models
from database import engine, SessionLocal
import ai_agent

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
    cevap = ai_agent.ai_yanit_ver(istek.mesaj, istek.rol)
    mesaj_lower = istek.mesaj.lower()
    rapor_durum = any(keyword in mesaj_lower for keyword in ["satış analiz", "satış raporu", "satis analiz", "satis raporu"])
    return {"ai_cevabi": cevap, "rapor_durum": rapor_durum}

@app.get("/api/sales-report")
def get_sales_report_csv():
    csv_content = ai_agent.satis_analizi_csv()
    return PlainTextResponse(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=\"satis_raporu.csv\""}
    )
