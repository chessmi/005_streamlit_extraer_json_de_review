import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI


template = """\
Para el siguiente texto, extrae la siguiente información:

sentimiento: ¿Está el cliente satisfecho con el producto?  
Responde **Positivo** si sí, **Negativo** si no, **Neutral** si no está claro, o **Desconocido** si no se menciona.

días_entrega: ¿Cuántos días tardó en llegar el producto?  
Si esta información no está disponible, responde **No hay información sobre esto**.

percepción_precio: ¿Cómo percibe el cliente el precio?  
Responde **Caro** si el cliente considera que el producto es caro,  
**Barato** si el cliente lo percibe como barato,  
**Neutral** si no menciona si es caro o barato, o **Desconocido** si no hay información.

Formatea la salida como una lista con los siguientes elementos:
- Sentimiento
- ¿Cuánto tiempo tardó en llegar?
- ¿Cómo se percibió el precio?

### Ejemplo de entrada:
Este vestido es realmente increíble. Llegó en dos días, justo a tiempo para el aniversario de mi esposa. Es más barato que otros vestidos en el mercado, pero creo que vale la pena por las características adicionales.

### Ejemplo de salida:
- **Sentimiento:** Positivo  
- **¿Cuánto tiempo tardó en llegar?** 2 días  
- **¿Cómo se percibió el precio?** Barato  

Texto: {review}
"""

# Definición de variables del PromptTemplate
prompt = PromptTemplate(
    input_variables=["review"],
    template=template,
)


# Función para cargar el modelo LLM y la clave de OpenAI
def cargar_LLM(api_key_openai):
    """Lógica para cargar el modelo de lenguaje a utilizar."""
    # Asegúrate de que tu clave API de OpenAI esté configurada correctamente
    llm = OpenAI(temperature=0, openai_api_key=api_key_openai)
    return llm


# Configuración de la página
st.set_page_config(page_title="Extraer Información Clave de Reseñas de Productos")
st.header("Extraer Información Clave de Reseñas de Productos")


# Introducción e instrucciones
col1, = st.columns(1)

with col1:
    st.markdown("Extrae información clave de una reseña de producto:")
    st.markdown("""
        - Sentimiento
        - ¿Cuánto tiempo tardó en llegar?
        - ¿Cómo se percibió su precio?
        """)


# Entrada de la clave API de OpenAI
st.markdown("## Ingresa tu Clave API de OpenAI")

def obtener_api_key():
    input_text = st.text_input(label="Clave API de OpenAI", placeholder="Ejemplo: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

api_key_openai = obtener_api_key()


# Entrada de la reseña del producto
st.markdown("## Ingresa la reseña del producto")

def obtener_resena():
    texto_resena = st.text_area(label="Reseña del Producto", label_visibility='collapsed', placeholder="Escribe aquí tu reseña del producto...", key="review_input")
    return texto_resena

resena_input = obtener_resena()

if len(resena_input.split(" ")) > 700:
    st.write("Por favor, ingresa una reseña más corta. El máximo permitido es de 700 palabras.")
    st.stop()


# Salida de datos clave extraídos
st.markdown("### Datos Clave Extraídos:")

if resena_input:
    if not api_key_openai:
        st.warning('Por favor, ingresa tu clave API de OpenAI. \
            Instrucciones [aquí](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = cargar_LLM(api_key_openai=api_key_openai)

    prompt_con_resena = prompt.format(
        review=resena_input
    )

    datos_extraidos = llm(prompt_con_resena)

    st.write(datos_extraidos)
