import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="FarmTech Solutions - SQLite IoT", page_icon="🌱", layout="wide")

st.title("🌱 FarmTech Solutions - Monitoramento Agrícola com SQLite")
st.markdown("Projeto Ir Além (FIAP) - Armazenamento persistente em Banco de Dados SQLite e Dashboard.")

DB_FILE = "sensores.db"

# Função para inicializar o banco de dados e a tabela
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            light INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Função para carregar os dados do SQLite para um DataFrame do Pandas
def load_data():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity", "light"])
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT timestamp, temperature, humidity, light FROM leituras ORDER BY id ASC", conn)
    conn.close()
    return df

# Inicializa o banco ao iniciar o app
init_db()

# --- BARRA LATERAL DE CONTROLE (Simulação de Envio dos Sensores) ---
st.sidebar.header("🎛️ Simulação de Envio (ESP32)")
st.sidebar.markdown("Ajuste os valores dos sensores e salve no Banco SQLite:")

input_temp = st.sidebar.slider("Temperatura do Ar (°C)", min_value=0.0, max_value=50.0, value=25.5, step=0.5)
input_hum = st.sidebar.slider("Umidade do Ar (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
input_light = st.sidebar.slider("Luminosidade (LDR)", min_value=0, max_value=1023, value=500, step=10)

if st.sidebar.button("📥 Enviar Leitura para o Banco"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO leituras (timestamp, temperature, humidity, light)
        VALUES (?, ?, ?, ?)
    ''', (current_time, input_temp, input_hum, input_light))
    conn.commit()
    conn.close()
    st.sidebar.success("Dado salvo com sucesso no SQLite!")
    st.rerun()

if st.sidebar.button("🗑️ Limpar Banco de Dados"):
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()
    st.sidebar.warning("Banco de dados limpo!")
    st.rerun()

# --- CORPO PRINCIPAL DO DASHBOARD ---
df = load_data()

if not df.empty:
    latest = df.iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Última Temperatura", f"{latest['temperature']} °C")
    col2.metric("💧 Última Umidade", f"{latest['humidity']} %")
    col3.metric("☀️ Última Luminosidade", f"{latest['light']}")
    
    st.markdown("---")
    st.subheader("📈 Histórico Cronológico (Consultado do SQLite)")
    
    st.line_chart(df.set_index("timestamp")[["temperature", "humidity"]])
    st.bar_chart(df.set_index("timestamp")["light"])
    
    with st.expander("📋 Ver Tabela Completa do Banco de Dados"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("O banco de dados SQLite está vazio. Use os controles na barra lateral para simular o envio das leituras dos sensores.")