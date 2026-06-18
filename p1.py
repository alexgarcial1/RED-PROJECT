import streamlit as st
from Buscador import ejecutar_agente 
# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA (UI LIMPIA)
# ==========================================
st.set_page_config(
    page_title="AI Movie Finder", 
    page_icon="🎬", 
    layout="wide"
)

# Estilos CSS inyectados (INCLUYE EL NUEVO HERO PREMIUM)
st.markdown("""
    <style>
    .reportview-container { background: #f5f7f8; }
    
    /* Nueva Hero Section Estilizada */
    .hero-container {
        background: linear-gradient(135px, #1e1e2f 0%, #111119 100%);
        padding: 40px 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    .hero-title {
        font-size: 36px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #b3b3b3;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.5;
    }
    
    /* Tarjetas de Películas */
    .movie-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border-left: 5px solid #FF4B4B;
        margin-bottom: 15px;
        height: 100%;
    }
    .movie-title {
        font-size: 20px;
        font-weight: bold;
        color: #1E1E1E;
        margin-bottom: 2px;
    }
    .movie-year {
        font-size: 14px;
        color: #888888;
        margin-bottom: 12px;
    }
    .tech-footer {
        font-size: 12px;
        color: #888888;
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #EEEEEE;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CABECERA PRINCIPAL (HERO PREMIUM)
# ==========================================
# Reemplaza tus líneas de st.title y st.markdown por este bloque HTML interactivo:
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">🎬 Encuentra tu próxima película</div>
        <div class="hero-subtitle">
            Describe lo que te apetece ver (una idea, un concepto o tu estado de ánimo) 
            y nuestra Inteligencia Artificial buscará de forma semántica en el catálogo completo.
        </div>
    </div>
""", unsafe_allow_html=True)


# Inicializar el historial de conversación si no existe
if "historial" not in st.session_state:
    st.session_state.historial = []

# ==========================================
# 3. RENDERIZADO PROFESIONAL DE TARJETAS
# ==========================================
def renderizar_peliculas(peliculas):
    # Creamos 3 columnas perfectas en horizontal estilo cartelera
    cols = st.columns(3)
    for i, peli in enumerate(peliculas):
        if i < 3: 
            with cols[i]:
                # Tarjeta visual limpia para el cliente
                st.markdown(f"""
                    <div class="movie-card">
                        <div class="movie-title">🍿 {peli['titulo']}</div>
                        <div class="movie-year">Año: {peli['anio']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Explicación del agente experto
                st.markdown("**🤖 Recomendación:**")
                st.write(peli['respuesta_agente'])
                
                # Datos técnicos en bruto ocultos por si el jurado quiere indagar
                with st.expander("Ver Metadata Original (Inglés)"):
                    st.caption(peli['sinopsis_original'])

# ==========================================
# 4. PINTAR EL HISTORIAL EXISTENTE
# ==========================================
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        if mensaje["role"] == "user":
            st.markdown(mensaje["content"])
        else:
            renderizar_peliculas(mensaje["content"])

# ==========================================
# 5. INPUT TIPO CHAT (FIJO EN LA PARTE INFERIOR)
# ==========================================
consulta = st.chat_input("Ej: A comedy about time travel or space wars...")

if consulta:
    # Registrar y pintar la duda del usuario
    st.session_state.historial.append({"role": "user", "content": consulta})
    with st.chat_message("user"):
        st.markdown(consulta)

    # Ejecutar el agente en segundo plano
    with st.chat_message("assistant"):
        with st.spinner("Consultando nuestro catálogo inteligente..."):
            try:
                # Llama directamente a tu archivo Buscador.py
                resultados_agente = ejecutar_agente(consulta)
                
                # Muestra el resultado maquetado en columnas
                renderizar_peliculas(resultados_agente)

                # Guardar en el estado de la sesión para mantener el hilo
                st.session_state.historial.append({"role": "assistant", "content": resultados_agente})

            except Exception as e:
                st.error(f"❌ Error al conectar con el motor de IA: {e}")

# ==========================================
# 6. PIE DE PÁGINA DISCRETO (SÓLO JURADO)
# ==========================================
# Una línea fina al fondo de la web con los datos técnicos resumidos de forma muy elegante
st.markdown("""
    <div class="tech-footer">
        <b>GenAI Mavericks MVP</b> | Arquitectura RAG Local: ChromaDB (Conectado) + Llama 3.2 via Ollama (Local) | Hackathon Barcelona 2026
    </div>
""", unsafe_allow_html=True)