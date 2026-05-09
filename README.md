# 🚀 KOBİ-Pilot: Otonom AI İşletme Yönetimi & Copilot

Küçük ve orta ölçekli işletmeler (KOBİ'ler) için tasarlanmış; müşteri iletişimini, stok takibini ve operasyonel süreçleri **sadece doğal dil (sohbet) kullanarak** yöneten yeni nesil "Aksiyon Odaklı" Yapay Zeka Ajanı (AI Agent).

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg) ![Gemini](https://img.shields.io/badge/Google_Gemini-Agent-orange.svg) 

---

## 💡 Neden KOBİ-Pilot? (Farkımız Nedir?)

Hackathon gereksinimlerini incelerken, piyasadaki standart çözümlerin sadece **"bilgi veren" (Soru-Cevap) chatbotlar** olduğunu fark ettik. KOBİ-Pilot ise sıradan bir chatbot değildir; veritabanı ile konuşabilen, karar alabilen ve sistemi güncelleyen **otonom bir çalışandır**.

**Fark Yaratan Özelliklerimiz:**
1. 🎭 **Çift Karakterli Mimari (Dual-Persona):**
   * **Müşteri Modu:** Harika bir satış danışmanıdır. Müşteriye ürün önerir (RAG benzeri mantık), iptal taleplerini alır. Ürün kargodaysa otonom olarak iade kodu üretir. ASLA yetkisi dışına çıkıp stok değiştiremez.
   * **Patron Modu:** Tam yetkili operasyon müdürüdür. Sisteme yeni ürün ekler, stok günceller, kargo durumlarını değiştirir ve genel veri analizi yapar.
2. ⚡ **Dinamik Hibrit Dashboard:**
   * Ekran sadece bir sohbet kutusu değildir. Patron modunda ekran genişler ve **Chart.js** destekli, gerçek zamanlı bir kontrol paneli açılır.
   * *Sihir burada:* Yapay zekaya sohbetten bir komut verdiğinizde (Örn: "1 nolu siparişi kargoya ver"), yapay zeka işlemi yapar ve **ekrandaki grafikler sayfa yenilenmeden canlı olarak güncellenir.**
3. 🛠️ **Function Calling (Aksiyon Alma):**
   * LLM sadece metin üretmez. `google-generativeai` tool mantığı ile CRUD (Create, Read, Update, Delete) operasyonlarını otonom yürütür.

---

## 🛠️ Kullanılan Teknolojiler

* **Yapay Zeka:** Google Gemini 1.5 Flash (Hızlı, fonksiyon çağırma kapasitesi yüksek)
* **Backend:** FastAPI, Uvicorn (Asenkron, yüksek performanslı API)
* **Veritabanı:** SQLAlchemy (SQLite - Hızlı prototipleme için)
* **Frontend:** Saf HTML/CSS, Vanilla JS, Chart.js, FontAwesome

---

## 🚀 Kurulum ve Çalıştırma (Jüri Testi İçin)

Projeyi kendi bilgisayarınızda saniyeler içinde ayağa kaldırabilirsiniz.

**1. Projeyi Klonlayın:**
```bash
git clone [https://github.com/KULLANICI_ADIN/kobi-pilot.git](https://github.com/KULLANICI_ADIN/kobi-pilot.git)
cd kobi-pilot