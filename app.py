import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="FarmTech Solutions - Dashboard IoT", page_icon="🌱", layout="wide")

st.title("🌱 FarmTech Solutions - Monitoramento Agrícola Inteligente")
st.markdown("Painel de Controle e Monitoramento Manual (Projeto Ir Além - FIAP).")

DATA_FILE = "sensor_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- BARRA LATERAL DE CONTROLE MANUAL ---
st.sidebar.header("🎛️ Controle dos Sensores (Simulação)")
st.sidebar.markdown("Ajuste os valores abaixo para simular leituras em tempo real:")

input_temp = st.sidebar.slider("Temperatura (°C)", min_value=0.0, max_value=50.0, value=25.5, step=0.5)
input_hum = st.sidebar.slider("Umidade (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
input_light = st.sidebar.slider("Luminosidade (LDR)", min_value=0, max_value=1023, value=500, step=10)

if st.sidebar.button("📥 Registrar Nova Leitura"):
    data = load_data()
    new_entry = {
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": input_temp,
        "humidity": input_hum,
        "light": input_light
    }
    data.append(new_entry)
    # Mantém os últimos 30 registros no histórico
    if len(data) > 30:
        data = data[-30:]
    save_data(data)
    st.sidebar.success("Leitura registrada com sucesso!")

if st.sidebar.button("🗑️ Limpar Histórico"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    st.sidebar.warning("Histórico limpo!")
    st.rerun()

# --- CORPO PRINCIPAL DO DASHBOARD ---
data = load_data()

if len(data) > 0:
    df = pd.DataFrame(data)
    latest = df.iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temperatura Atual (DHT22)", f"{latest['temperature']} °C")
    col2.metric("💧 Umidade Atual (DHT22)", f"{latest['humidity']} %")
    col3.metric("☀️ Luminosidade Atual (LDR)", f"{latest['light']}")
    
    st.markdown("---")
    st.subheader("📈 Histórico de Leituras Registradas")
    
    st.line_chart(df.set_index("timestamp")[["temperature", "humidity"]])
    st.bar_chart(df.set_index("timestamp")["light"])
    
    with st.expander("📋 Ver Tabela de Dados Brutos"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhum dado registrado ainda. Use a barra lateral à esquerda para ajustar os valores e clicar em **'Registrar Nova Leitura'**.")