import pandas as pd
import chromadb

# 1. Leemos solo 100 filas del CSV
df = pd.read_csv("wiki_movie_plots_deduped.csv", nrows=100)

# 2. Conectamos Chroma a una carpeta fija llamada 'cine_db'
chroma_client = chromadb.PersistentClient(path="./cine_db")
collection = chroma_client.get_or_create_collection(name="peliculas")

print("⏳ Guardando 100 películas en Chroma...")

# 3. Guardamos los datos
for index, row in df.iterrows():
    collection.add(
        documents=[row['Plot']],
        metadatas=[{"titulo": row['Title'], "anio": int(row['Release Year'])}],
        ids=[str(index)]
    )

print("✅ ¡Películas guardadas con éxito en la carpeta './cine_db'!")