import chromadb
import ollama

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

sinopsis=resultados['documents'][0][0]
titulo_encontrado=resultados['metadatas'][0][0]['titulo']
anio_encontrado=resultados['metadatas'][0][0]['anio']

print(f"✅ Película encontrada: '{titulo_encontrado}' ({anio_encontrado})")
print(f"pasando información a ollama para generar un resumen de la sinopsis"  )
prompt_sistema=("Eres un agente experto en cine. El usuario te pedirá una recomendación. "
    "Debes usar ÚNICAMENTE la siguiente información de la película que encontramos en nuestra base de datos "
    "para responderle de forma amable, entusiasta y completamente en español.\n\n"
    f"Película: {titulo_encontrado} ({anio_encontrado})\n"
    f"Sinopsis: {sinopsis}"
)

respuesta_ollama = ollama.chat(
    model='llama3.2', 
    messages=[
        {'role': 'system', 'content': prompt_sistema},
        {'role': 'user', 'content': consulta}
    ]
)
# 5. Mostramos el resultado final en la pantalla
print("================= RESPUESTA DEL AGENTE =================")
# Intentamos con la estructura estándar de Ollama
try:
    print(respuesta_ollama['message']['content'])
except (KeyError, TypeError):
    # Si la librería se actualizó o cambia el formato, esto asegura que imprima igual
    print(respuesta_ollama.message.content)
print("========================================================")

