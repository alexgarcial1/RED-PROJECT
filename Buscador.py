import chromadb
import ollama
import chromadb
import ollama

def ejecutar_agente(consulta):
    # 1. Nos conectamos a la carpeta de datos
    chroma_client = chromadb.PersistentClient(path="./cine_db")
    collection = chroma_client.get_collection(name="peliculas")

    # 2. Hacemos la consulta pidiendo 3 resultados
    resultados = collection.query(
        query_texts=[consulta],
        n_results=3
    )

    lista_sinopsis = resultados['documents'][0]
    lista_metadatas = resultados['metadatas'][0]

    # Lista donde guardaremos las respuestas de Ollama para la web
    respuestas_finales = []

    # 3. Procesamos las 3 películas con Ollama
    for i in range(len(lista_sinopsis)):
        titulo = lista_metadatas[i]['titulo']
        anio = lista_metadatas[i]['anio']
        sinopsis_individual = lista_sinopsis[i]
        
        prompt_sistema = (
            "Eres un agente experto en cine. El usuario te pedirá una recomendación. "
            "Debes usar ÚNICAMENTE la siguiente información de la película que encontramos en nuestra base de datos "
            "para responderle de forma amable, entusiasta y completamente en español.\n\n"
            f"Película: {titulo} ({anio})\n"
            f"Sinopsis: {sinopsis_individual}"
        )

        respuesta_ollama = ollama.chat(
            model='llama3.2', 
            messages=[
                {'role': 'system', 'content': prompt_sistema},
                {'role': 'user', 'content': consulta}
            ]
        )

        try:
            contenido = respuesta_ollama['message']['content']
        except (KeyError, TypeError):
            contenido = respuesta_ollama.message.content
            
        # Guardamos un diccionario con todo lo necesario para pintar en la web
        respuestas_finales.append({
            "titulo": titulo,
            "anio": anio,
            "sinopsis_original": sinopsis_individual,
            "respuesta_agente": contenido
        })
        