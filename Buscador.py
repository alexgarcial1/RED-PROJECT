import chromadb
import ollama
import chromadb
import ollama

def ejecutar_agente(consulta):
    chroma_client = chromadb.PersistentClient(path="./cine_db")
    collection = chroma_client.get_collection(name="peliculas")

    resultados = collection.query(
        query_texts=[consulta],
        n_results=3
    )

    lista_sinopsis = resultados['documents'][0]
    lista_metadatas = resultados['metadatas'][0]

    respuestas_finales = []

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
            
        respuestas_finales.append({
            "titulo": titulo,
            "anio": anio,
            "sinopsis_original": sinopsis_individual,
            "respuesta_agente": contenido
        })
    
    return respuestas_finales  # <-- ESTO es lo que faltaba