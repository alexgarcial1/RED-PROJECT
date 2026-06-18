import streamlit as st
# IMPORTAMOS LA LÓGICA DE TU BUSCADOR (Nota: asegúrate de guardar el archivo como buscador.py en minúsculas)
from Buscador import ejecutar_agente 

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA (STREAMLIT)
# ==========================================
st.set_page_config(
    page_title="AI Movie Finder - GenAI Mavericks", 
    page_icon="🎬", 
    layout="wide"
)

st.title("🎬 Buscador de Películas Inteligente")
st.subheader("MVP de RAG Local con ChromaDB y Llama 3.2 (Hackathon Barcelona)")
st.markdown("---")

# Métricas de negocio
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    st.metric(label="Base de Datos", value="ChromaDB Local", delta="Conectada")
with col_kpi2:
    st.metric(label="Modelo LLM", value="Llama 3.2 (Ollama)", delta="En Local")
with col_kpi3:
    st.metric(label="Agente Experto", value="Cine-Bot Español", delta="3 Resultados")

st.markdown("---")

# ==========================================
# 2. ENTRADA DE USUARIO
# ==========================================
consulta = st.text_input(
    "¿Qué tipo de historia o premisa estás buscando?", 
    placeholder="Ej: A movie about spaceships, space battles or aliens..."
)

# ==========================================
# 3. EJECUCIÓN DEL SCRIPT EXTERNO
# ==========================================
if st.button("🚀 Preguntar al Agente de Cine", type="primary"):
    if not consulta:
        st.warning("Por favor, escribe una descripción o frase clave para iniciar la búsqueda.")
    else:
        with st.spinner("🤖 Llamando a Buscador.py y ejecutando Ollama para las 3 películas..."):
            try:
                # LLAMAMOS AL SCRIPT EXTERNO DIRECTAMENTE
                resultados_agente = ejecutar_agente(consulta)
                
                st.success("🎯 ¡Resultados procesados por el agente!")
                st.markdown("### 🍿 Recomendaciones del Catálogo")
                
                # Pintamos de forma elegante las 3 respuestas devueltas
                for i, peli in enumerate(resultados_agente):
                    with st.expander(f"🎥 Opción {i+1}: {peli['titulo']} ({peli['anio']})", expanded=True):
                        st.markdown("**🤖 Análisis en Español:**")
                        st.info(peli['respuesta_agente'])
                        
                        st.markdown("**📄 Sinopsis Original Indexada (Data):**")
                        st.caption(peli['sinopsis_original'])
                        
            except Exception as e:
                st.error(f"❌ Error al ejecutar el agente de búsqueda: {e}")
                st.info("Revisa que el archivo se llame exactamente 'buscador.py' y que Ollama esté encendido.")

st.markdown("---")
st.caption("GenAI Mavericks Challenge 2026 - Capa Frontend Desacoplada de la Lógica del Agente.")