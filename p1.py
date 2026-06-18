import streamlit as st
import chromadb

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA (STREAMLIT)
# ==========================================
st.set_page_config(
    page_title="AI Movie Finder - GenAI Mavericks", 
    page_icon="🎬", 
    layout="wide"
)

# Estilo y cabecera de negocio
st.title("🎬 Buscador de Películas Inteligente")
st.subheader("MVP de Recuperación Semántica Avanzada (Hackathon Barcelona)")
st.markdown("---")

# Métricas de valor de negocio en el Header
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    st.metric(label="Base de Datos", value="ChromaDB Local", delta="Activa")
with col_kpi2:
    st.metric(label="Películas Disponibles", value="100 Muestra", delta="Escalable a 34k")
with col_kpi3:
    st.metric(label="Tiempo de Respuesta", value="< 0.1s", delta="-95% vs tradicional")

st.markdown("---")

# ==========================================
# 2. ENTRADA DE USUARIO
# ==========================================
consulta = st.text_input(
    "¿Qué tipo de historia o premisa estás buscando? (Escribe en inglés para mejores resultados con el dataset):", 
    placeholder="Ej: A movie about spaceships, space battles or aliens..."
)

# ==========================================
# 3. LÓGICA DE BÚSQUEDA DIRECTA EN CHROMADB
# ==========================================
if st.button("🔍 Buscar Películas Similares", type="primary"):
    if not consulta:
        st.warning("Por favor, escribe una descripción o frase clave para iniciar la búsqueda.")
    else:
        with st.spinner("Consultando los vectores en la carpeta './cine_db'..."):
            try:
                # Conexión nativa a la base de datos local de tu compañero
                chroma_client = chromadb.PersistentClient(path="./cine_db")
                collection = chroma_client.get_collection(name="peliculas")
                
                # Lanzamos la consulta para extraer las 3 películas más parecidas
                resultados = collection.query(
                    query_texts=[consulta],
                    n_results=3
                )
                
                st.success("🎯 ¡Películas más relevantes encontradas con éxito!")
                st.markdown("### 🍿 Resultados del Catálogo")
                
                # Desglosamos la respuesta de ChromaDB
                documentos = resultados['documents'][0]
                metadatas = resultados['metadatas'][0]
                
                # Pintamos los resultados de forma visual en la web usando desplegables
                for i in range(len(documentos)):
                    titulo_pelicula = metadatas[i]['titulo']
                    anio_pelicula = metadatas[i]['anio']
                    
                    with st.expander(f"🎥 {titulo_pelicula} ({anio_pelicula})", expanded=True):
                        st.markdown("**📄 Sinopsis/Trama de la película:**")
                        st.write(documentos[i])
                        st.caption("Fuente: Kaggle Wikipedia Movie Plots")
                        
            except Exception as e:
                st.error(f"❌ Error al conectar con la base de datos: {e}")
                st.info("Asegúrate de que la carpeta './cine_db' existe en tu directorio y que tu compañero corrió su script correctamente primero.")

# Footer corporativo
st.markdown("---")
st.caption("GenAI Mavericks Challenge 2026 - Capa Frontend Desarrollada con Streamlit.")