# ai_agent.py
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from database import SessionLocal
import models
import random

load_dotenv()

# En baştaki orijinal bağlantı yöntemimiz
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# --- 1. MEVCUT ARAÇLAR ---
def stok_sorgula(urun_adi: str) -> str:
    db = SessionLocal()
    urun = db.query(models.Product).filter(models.Product.name.ilike(f"%{urun_adi}%")).first()
    db.close()
    if urun: return f"{urun.name} ürününden stoklarımızda {urun.stock_quantity} adet bulunmaktadır."
    return f"{urun_adi} adında bir ürün bulunamadı."

def siparis_sorgula(siparis_id: int) -> str:
    db = SessionLocal()
    siparis = db.query(models.Order).filter(models.Order.id == siparis_id).first()
    if siparis:
        urun = db.query(models.Product).filter(models.Product.id == siparis.product_id).first()
        db.close()
        return f"{siparis_id} numaralı siparişiniz ({urun.name}) şu anda '{siparis.status}' durumundadır."
    db.close()
    return f"{siparis_id} numaralı bir sipariş bulunamadı."

def siparis_durumu_guncelle(siparis_id: int, yeni_durum: str) -> str:
    db = SessionLocal()
    siparis = db.query(models.Order).filter(models.Order.id == siparis_id).first()
    if siparis:
        siparis.status = yeni_durum
        db.commit()
        db.close()
        return f"BAŞARILI: {siparis_id} numaralı siparişin durumu '{yeni_durum}' olarak güncellendi."
    db.close()
    return f"HATA: {siparis_id} numaralı sipariş bulunamadı."

def satis_analizi_yap() -> str:
    db = SessionLocal()
    siparisler = db.query(models.Order).all()
    urunler = db.query(models.Product).all()
    satis_miktarlari = {}
    for s in siparisler:
        satis_miktarlari[s.product_id] = satis_miktarlari.get(s.product_id, 0) + 1

    rapor = "VERİTABANI ANALİZ RAPORU:\n"
    for u in urunler:
        satis = satis_miktarlari.get(u.id, 0)
        rapor += f"- {u.name}: Toplam {satis} sipariş. Güncel Stok: {u.stock_quantity}. "
        if u.stock_quantity <= 5: rapor += "[KRİTİK STOK UYARISI!]"
        rapor += "\n"
    db.close()
    return rapor

def tarih_bazli_rapor_getir(zaman_dilimi: str) -> str:
    """Belirli bir zaman dilimi ('bugun', 'bu_hafta', 'bu_ay', 'tumu') için satış analiz raporu getirir."""
    db = SessionLocal()
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    
    query = db.query(models.Order)
    if zaman_dilimi == "bugun":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Order.created_at >= start)
    elif zaman_dilimi == "bu_hafta" or zaman_dilimi == "bu-hafta":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Order.created_at >= start)
    elif zaman_dilimi == "bu_ay" or zaman_dilimi == "bu-ay":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Order.created_at >= start)
    else:
        zaman_dilimi = "tumu"

    siparisler = query.all()
    urunler = db.query(models.Product).all()
    urun_isimleri = {u.id: u.name for u in urunler}
    
    satis_miktarlari = {}
    for s in siparisler:
        satis_miktarlari[s.product_id] = satis_miktarlari.get(s.product_id, 0) + 1

    toplam_satis = len(siparisler)
    rapor = f"ZAMAN BAZLI SATIŞ ANALİZİ ({zaman_dilimi}):\n"
    rapor += f"Bu dönemde toplam {toplam_satis} sipariş alındı.\n\n"
    
    for urun_id, miktar in satis_miktarlari.items():
        isim = urun_isimleri.get(urun_id, f"Ürün {urun_id}")
        rapor += f"- {isim}: {miktar} adet satıldı.\n"
        
    db.close()
    
    html_button = f'<br><br><a href="/api/export/orders?period={zaman_dilimi}" target="_blank" style="display:inline-block; padding:10px 15px; background-color:#10b981; color:white; text-decoration:none; border-radius:8px; font-weight:bold; font-family:sans-serif;">📥 Raporu CSV Olarak İndir</a>'
    return rapor + html_button


def urun_ekle(urun_adi: str, stok_miktari: int) -> str:
    db = SessionLocal()
    yeni_urun = models.Product(name=urun_adi, stock_quantity=stok_miktari)
    db.add(yeni_urun)
    db.commit()
    db.close()
    return f"BAŞARILI: '{urun_adi}' sisteme eklendi."

def stok_guncelle(urun_adi: str, yeni_stok: int) -> str:
    db = SessionLocal()
    urun = db.query(models.Product).filter(models.Product.name.ilike(f"%{urun_adi}%")).first()
    if urun:
        urun.stock_quantity = yeni_stok
        db.commit()
        db.close()
        return f"BAŞARILI: Stok güncellendi."
    db.close()
    return "HATA: Ürün bulunamadı."

# --- 2. YENİ GELİŞTİRİLEN ARAÇLAR (E-TİCARET & İADE) ---

def katalog_getir() -> str:
    db = SessionLocal()
    urunler = db.query(models.Product).filter(models.Product.stock_quantity > 0).all()
    db.close()
    if not urunler: return "Şu an stokta satışa hazır ürünümüz bulunmamaktadır."
    
    katalog = "DÜKKANDAKİ AKTİF ÜRÜNLER (Bu ürünleri kullanarak müşteriye satış yap/öneri sun):\n"
    for u in urunler:
        katalog += f"- {u.name}\n"
    return katalog

def siparis_iptal_et(siparis_id: int) -> str:
    db = SessionLocal()
    siparis = db.query(models.Order).filter(models.Order.id == siparis_id).first()
    
    if siparis:
        if siparis.status == "Hazırlanıyor":
            siparis.status = "İptal"
            db.commit()
            db.close()
            return f"BAŞARILI: {siparis_id} numaralı sipariş iptal edildi."
        elif siparis.status == "Kargoda":
            iade_kodu = f"IADE-{random.randint(1000, 9999)}"
            db.close()
            return f"İPTAL REDDEDİLDİ: Sipariş kargoya verildiği için iptal edilemez. Müşteriye kargoyu teslim almayarak iade edebileceğini söyle ve şu iade kodunu ver: {iade_kodu}"
        else:
            db.close()
            return f"İPTAL REDDEDİLDİ: Sipariş '{siparis.status}' durumunda."
            
    db.close()
    return f"HATA: {siparis_id} numaralı sipariş bulunamadı."


# --- 3. KİMLİK (PROMPT) VE YETKİLENDİRME ---

sistem_yonergesi = """Sen KOBİ-Pilot adında otonom bir işletme asistanısın.

- [PATRON] ETİKETİ VARSA: İşletme sahibisin. Ürün ekle, analiz yap, stok güncelle, sipariş durumlarını değiştir.
Eğer kullanıcı siparişleri/raporları indirmek isterse, KESİNLİKLE 'tarih_bazli_rapor_getir' aracını kullan ve kullanıcıya indirme linkini sun. 'Bunu yapamam' deme!

- [MÜŞTERİ] ETİKETİ VARSA: Harika bir satış danışmanı ve müşteri temsilcisisin.
  1) Müşteri tavsiye veya ürün sorarsa KESİNLİKLE 'katalog_getir' aracını kullanıp uygun ürünleri pazarlayarak öner.
  2) İptal istenirse 'siparis_iptal_et' aracını kullan. Kargodaysa sistemin sana verdiği iade kodunu müşteriye kibarca ilet.
  3) ASLA stok güncelleme veya ürün ekleme yetkini kullanma.
"""

tum_araclar = [
    stok_sorgula, siparis_sorgula, siparis_durumu_guncelle, 
    satis_analizi_yap, tarih_bazli_rapor_getir, urun_ekle, stok_guncelle, 
    katalog_getir, siparis_iptal_et
]

config = types.GenerateContentConfig(
    system_instruction=sistem_yonergesi,
    tools=tum_araclar,
    temperature=0.0
)

# En başta sorunsuz çalışan model ismimiz:
chat = client.chats.create(model="gemini-2.5-flash", config=config)

def ai_yanit_ver(kullanici_mesaji: str, rol: str) -> str:
    mesaj_formati = f"[{rol.upper()}] {kullanici_mesaji}"
    response = chat.send_message(mesaj_formati)
    return response.text

def sohbet_gecmisini_temizle():
    global chat
    chat = client.chats.create(model="gemini-2.5-flash", config=config)
    return "Hafıza sıfırlandı."