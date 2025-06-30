import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import pandas as pd
from geopy.geocoders import Nominatim
import time
import folium
from streamlit_folium import st_folium

# --- Konfigürasyon ve Fonksiyonlar (Değişiklik Yok) ---
load_dotenv()

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("API Anahtarı bulunamadı! Lütfen .env dosyanızı kontrol edin.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API konfigürasyonunda bir hata oluştu: {e}")


def get_coordinates(place_name, city):
    try:
        geolocator = Nominatim(user_agent="travel_planner_app")
        location = geolocator.geocode(f"{place_name}, {city}")
        time.sleep(1)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        st.warning(f"'{place_name}' için koordinat bulunamadı: {e}")
    return None, None


def generate_travel_plan(destination, duration, interests, budget):
    prompt = f"""
    Sen, deneyimli bir yerel seyahat rehberisin.
    Çıktıyı MUTLAKA ve SADECE JSON formatında ver. Başka hiçbir açıklama ekleme.
    JSON yapısı şu şekilde olmalı:
    {{
      "sehir": "{destination}",
      "gun_sayisi": {duration},
      "plan": [
        {{
          "gun": 1,
          "tema": "Günün kısa başlığı",
          "aktiviteler": [
            {{"zaman": "09:00-12:00", "yer": "Aktivite Adı", "aciklama": "Kısa açıklama"}}
          ]
        }}
      ]
    }}
    Kullanıcı Bilgileri: {destination}, {duration} gün, {', '.join(interests)}, {budget} bütçe.
    Lütfen bu bilgilere göre yukarıdaki JSON formatında bir plan oluştur.
    """
    try:
        with st.spinner("Seyahat planınız yapay zeka tarafından oluşturuluyor... Bu işlem biraz zaman alabilir."):
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        st.error(f"Plan oluşturulurken bir hata meydana geldi: {e}")
        return None


# --- Streamlit Arayüzü ---
st.set_page_config(page_title="Akıllı Gezi Planlayıcı", page_icon="🌍")
st.title("🌍 Akıllı Gezi Planlayıcı")
st.write("Yapay zeka destekli kişisel seyahat asistanınız.")

# --- YENİ YAPI: Session State'i başlatma ---
# Eğer hafızada 'plan_data' yoksa, onu None olarak oluştur.
if 'plan_data' not in st.session_state:
    st.session_state.plan_data = None

# --- Formun Yeni Görevi: Sadece Veriyi Alıp Hafızaya Yazmak ---
with st.form("travel_form"):
    st.header("Seyahat Detaylarınızı Girin")
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Nereye gitmek istersiniz?", placeholder="Örn: Roma, İtalya")
    with col2:
        duration = st.number_input("Kaç gün kalacaksınız?", min_value=1, max_value=30, value=3)
    interests = st.multiselect("İlgi alanlarınız neler?",
                               ["Tarih", "Sanat", "Doğa", "Macera", "Yemek", "Gece Hayatı", "Alışveriş"],
                               default=["Tarih", "Yemek"])
    budget = st.select_slider("Bütçeniz nasıl?", options=["Ekonomik 💸", "Orta 💰", "Lüks 💎"], value="Orta 💰")
    submitted = st.form_submit_button("Planımı Oluştur!")

    if submitted:
        if not destination:
            st.warning("Lütfen bir destinasyon girin.")
        else:
            plan_json_text = generate_travel_plan(destination, duration, interests, budget)
            if plan_json_text:
                clean_json_text = plan_json_text.replace("```json", "").replace("```", "").strip()
                try:
                    # Gelen veriyi hafızaya (session_state) kaydet
                    st.session_state.plan_data = json.loads(clean_json_text)
                except json.JSONDecodeError:
                    st.error("Yapay zekadan gelen yanıt geçerli bir JSON formatında değil. Lütfen tekrar deneyin.")
                    st.session_state.plan_data = None  # Hata durumunda hafızayı temizle

# --- YENİ YAPI: Görüntüleme Bloğu (Formun Dışında) ---
# Eğer hafızada (session_state) bir plan varsa, onu ekrana çiz.
if st.session_state.plan_data:
    plan_data = st.session_state.plan_data
    st.header(f"✨ {plan_data['sehir']} için Harika Bir Gezi Planı ✨")

    locations = []
    for day in plan_data['plan']:
        with st.expander(f"🗓️ **Gün {day['gun']}: {day['tema']}**"):
            for aktivite in day['aktiviteler']:
                st.markdown(f"- **⏰ {aktivite['zaman']}**: **{aktivite['yer']}**\n  - *{aktivite['aciklama']}*")
                # Not: Her seferinde koordinat almak yavaş olabilir. Daha ileri bir versiyonda bu da state'e alınabilir.
                lat, lon = get_coordinates(aktivite['yer'], plan_data['sehir'])
                if lat and lon:
                    locations.append({'name': aktivite['yer'], 'latitude': lat, 'longitude': lon})

    if locations:
        st.markdown("---")
        st.subheader("📍 Plandaki Mekanlar Haritası")
        map_center = [locations[0]['latitude'], locations[0]['longitude']]
        m = folium.Map(location=map_center, zoom_start=13)
        for loc in locations:
            folium.Marker([loc['latitude'], loc['longitude']], popup=loc['name']).add_to(m)
        st_folium(m, width=725, key="map1")  # Haritaya bir 'key' eklemek state yönetimini daha stabil hale getirir.