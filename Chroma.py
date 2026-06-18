import pandas as pd
import chromadb
from tqdm import tqdm  # <--- Esta librería hace la magia del porcentaje

# 1. Leemos el CSV (Muestra recomendada de 2000 para el MVP, cámbialo si quieres)
df = pd.read_csv("wiki_movie_plots_deduped.csv")

# Aseguramos que no haya datos vacíos en las columnas clave
df = df.dropna(subset=['Plot', 'Title', 'Release Year'])

# 2. Conectamos Chroma
chroma_client = chromadb.PersistentClient(path="./cine_db")
collection = chroma_client.get_or_create_collection(name="peliculas")

print(f"⏳ Preparando la carga masiva de {len(df)} películas en Chroma...")

# Agrupamos los datos en listas masivas
todos_los_plots = df['Plot'].tolist()
todos_los_ids = [str(i) for i in df.index]
todos_los_metadatas = [
    {"titulo": row['Title'], "anio": int(row['Release Year'])} 
    for _, row in df.iterrows()
]

# 3. OPTIMIZACIÓN CON PORCENTAJE EN TIEMPO REAL
tamano_bloque = 500

# Metemos el rango dentro de 'tqdm' para que pinte la barra y el % automáticamente
for i in tqdm(range(0, len(todos_los_plots), tamano_bloque), desc="📦 Guardando películas en ChromaDB"):
    fin = i + tamano_bloque
    
    collection.add(
        documents=todos_los_plots[i:fin],
        metadatas=todos_los_metadatas[i:fin],
        ids=todos_los_ids[i:fin]
    )

print("\n✅ ¡Películas guardadas con éxito en la carpeta './cine_db'!")