# Akıllı Gezi Planlayıcı (AI Travel Planner)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://triva-app.streamlit.app/)

Kullanıcıların ilgi alanlarına, bütçelerine ve seyahat sürelerine göre kişiselleştirilmiş seyahat rotaları oluşturan, Google Gemini API destekli bir web uygulaması.

---

## 🚀 Canlı Demo

Uygulamanın canlı versiyonuna aşağıdaki linkten ulaşabilirsiniz:

**[https://triva-app.streamlit.app/](https://triva-app.streamlit.app/)**

![Uygulama Ekran Görüntüsü](https://i.imgur.com/bYSVDAT.png) 


---

## ✨ Özellikler

* **Kişiselleştirilmiş Planlama:** Gidilecek yer, gün sayısı, ilgi alanları ve bütçeye göre özel gezi planları.
* **Yapay Zeka Destekli:** Google'ın güçlü dil modeli Gemini 1.5 Flash kullanılarak dinamik içerik üretimi.
* **Yapısal Veri Çıktısı:** Gemini API'den JSON formatında veri alıp işleyerek tutarlı ve düzenli bir sunum.
* **İnteraktif Harita:** Plandaki tüm mekanların Folium ile oluşturulmuş, tıklanabilir bir harita üzerinde gösterimi.

---

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python
* **Web Arayüzü:** Streamlit
* **Yapay Zeka Modeli:** Google Gemini API
* **Haritalama:** Folium, Geopy (OpenStreetMap/Nominatim ile)
* **Veri İşleme:** Pandas
* **Dağıtım (Deployment):** Streamlit Community Cloud

---

## ⚙️ Lokalde Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/osnn96/Trivia-App.git](https://github.com/osnn96/Trivia-App.git)
    cd Trivia-App
    ```

2.  **Sanal ortam oluşturun ve aktif edin:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **`.env` dosyasını oluşturun:**
    Proje ana dizininde `.env` adında bir dosya oluşturun ve içine Google Gemini API anahtarınızı aşağıdaki formatta ekleyin:
    ```
    GEMINI_API_KEY="SIZIN_API_ANAHTARINIZ_BURAYA"
    ```

5.  **Uygulamayı çalıştırın:**
    ```bash
    streamlit run app.py
    ```

---

Bu proje, Gemini AI ve Streamlit ile bir proje geliştirme sürecini öğrenmek amacıyla yapılmıştır.