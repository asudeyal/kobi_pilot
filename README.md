# 🚀 KOBİ-Pilot: Yapay Zeka Destekli Otonom İşletme Asistanı

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg) ![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-orange.svg) ![Chart.js](https://img.shields.io/badge/Chart.js-Data_Viz-pink.svg)

## 📖 Proje Hakkında

**KOBİ-Pilot**, küçük ve orta ölçekli işletmelerin (KOBİ'ler) stok, sipariş ve müşteri ilişkilerini tamamen otonom bir şekilde yönetmelerini sağlayan yeni nesil bir **SaaS platformudur**. Standart soru-cevap botlarının aksine, gücünü **Google Gemini 2.5 Flash API**'den alan KOBİ-Pilot, veritabanı ile doğrudan konuşabilir, kararlar alabilir ve işletme operasyonlarını (CRUD) sizin adınıza yürüten otonom bir dijital çalışan gibi hareket eder.

---

## ✨ Öne Çıkan Özellikler

* 🎭 **Rol Bazlı Yönetim (Dual-Persona):** 
  * **Patron Modu:** Tam yetkili işletme yöneticisidir. Sisteme yeni ürün ekler, stok günceller, sipariş durumlarını değiştirir ve genel veri analizlerini otonom olarak yapar.
  * **Müşteri Modu:** Harika bir satış danışmanıdır. Müşteriye ürün önerir, iptal taleplerini değerlendirir. Ürün kargodaysa iptali reddedip otonom olarak iade kodu üretir; yetkisi dışına çıkıp asla stok/ürün manipülasyonu yapmaz.
* 🤖 **Otonom Agent (Function Calling):** Doğal dil (sohbet) kullanılarak verilen komutları anlar, gerekli API/Veritabanı araçlarını tetikler ve işlemleri insan müdahalesi olmadan gerçekleştirir.
* 📊 **İnteraktif Dashboard:** Chart.js ile görselleştirilmiş canlı veri grafikleri. "Kritik Stok" veya "Bekleyen Kargo" gibi tıklanabilir durum kartları ile anlık operasyonel detayları gösterir. Sayfa yenilenmeden, yapay zekanın yaptığı işlemler anında grafiklere yansır.
* 🎙️ **Sesli Komut (Voice-to-Text):** Entegre Web Speech API sayesinde klavyeye ihtiyaç duymadan, eller serbest (hands-free) bir şekilde doğal dil komutlarınızı sisteme iletebilirsiniz.
* 📈 **Akıllı Raporlama:** "Bugünkü satışları raporla" gibi komutlarla Günlük/Haftalık/Aylık özetler çıkarır. Ek olarak, Türkçe Excel uyumluluğu için BOM (Byte Order Mark) destekli, dinamik bir **CSV dışa aktarma (Export)** butonu sunar.

---

## 🛠️ Teknoloji Yığını (Tech Stack)

### Backend & AI
* **Dil & Framework:** Python, FastAPI, Uvicorn
* **Veritabanı:** SQLAlchemy & SQLite (Hızlı prototipleme için)
* **Yapay Zeka:** Google Gemini SDK (Gemini 2.5 Flash)

### Frontend
* **Core:** HTML5, Vanilla JavaScript, CSS3
* **Tasarım Dili:** Modern Dark SaaS Theme, Responsive UI
* **Araçlar & Kütüphaneler:** Chart.js (Veri Görselleştirme), FontAwesome (İkonlar), Marked.js (Markdown Parse)

---

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel ortamınızda saniyeler içinde ayağa kaldırabilir, yapay zekanın gücünü hemen test edebilirsiniz.

**1. Projeyi Klonlayın:**
```bash
git clone https://github.com/KULLANICI_ADIN/kobi-pilot.git
cd kobi-pilot
```

**2. Gerekli Kütüphaneleri Kurun:**
```bash
pip install -r requirements.txt
```

**3. API Anahtarını Ekleyin:**
Proje ana dizininde bir `.env` dosyası oluşturun ve içerisine Google Gemini API anahtarınızı ekleyin:
```env
GEMINI_API_KEY=sizin_api_anahtariniz_buraya
```

**4. Sunucuyu Başlatın:**
```bash
uvicorn main:app --reload
```
*Tarayıcınızda `http://127.0.0.1:8000` adresine giderek uygulamayı kullanmaya başlayabilirsiniz.*

---

## 🎯 Jüri Demo Senaryoları

Sistemin otonom karar alma yeteneklerini test etmek için aşağıdaki senaryoları deneyebilirsiniz:

1. **Satış Danışmanı (Müşteri Modunda):** "Bana güzel bir kahvaltılık ürün önerebilir misin?" diyerek RAG benzeri ürün öneri mantığını test edin.
2. **Otonom İade Kontrolü (Müşteri Modunda):** Kargoya verilmiş bir siparişi iptal etmeyi deneyin. Sistem iptali reddedip akıllı bir iade kodu (Örn: `IADE-4821`) üretecektir.
3. **Aksiyon ve Dashboard Senkronizasyonu (Patron Modunda):** Mikrofonu kullanarak sesli komutla "Sisteme yeni bir ürün ekle: Köy Tereyağı, stok 50 adet" deyin. İşlem tamamlandığında dashboard'un anında güncellendiğini görün.
4. **Akıllı CSV Raporlama (Patron Modunda):** "Bugünkü siparişleri indir" komutunu verin. Yapay zekanın oluşturduğu butona tıklayarak Türkçe karakter destekli CSV dosyanızı dışa aktarın.

---

## 👥 Geliştirici Ekip

* **Berk Yücedağ**
* **Asude Yalçın**
* **Senanur Topal**
