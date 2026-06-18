import chromadb

# 1. Nos conectamos a la carpeta que ya tiene los datos guardados
chroma_client = chromadb.PersistentClient(path="./cine_db")
collection = chroma_client.get_collection(name="peliculas")

# 2. Hacemos la pregunta
consulta = "A movie about spaceships, space battles or aliens"
print(f"\n🔍 Buscando películas relacionadas con: '{consulta}'...\n")

resultados = collection.query(
    query_texts=[consulta],
    n_results=1
)

# 3. Mostramos el resultado
for i in range(len(resultados['documents'][0])):
    print(f"🎬 Película {i+1}:")
    print(f"📄 Sinopsis: {resultados['documents'][0][i]}")
    print(f"📋 Metadatos: {resultados['metadatas'][0][i]}")
    print("-" * 50)