import requests

def evaluar_juego_conversacional(descripcion_juego):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer sk-66e9a7220f06460f834464618252410d",
        "Content-Type": "application/json"
    }
    
    # Prompt para la API
    prompt = (
        f"Hola, actua como un experto en diseño de sistemas digitales, por lo que tu trabajo es realizar el análisis de cómo diseñarías un sistema para resolver el problema planteado"
        f"El problema a solucionar es: {descripcion_juego}. "
        f"como experto en diseño de sistemas digitales, ¿cuáles son los pasos que seguirías para abordar este problema?, incluye contextualización, análisis de requisitos, diseño de la arquitectura del sistema, implementación y pruebas. "
        f"Recuerda que el sistema debe ser capaz de resolver el problema planteado y cumplir con los requisitos especificados. Sé extenso y descriptivo en tu respuesta "
    )
    
    data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "Eres un asistente experto en evaluaciión y diseño de sistemas logicos de circuitos digitales."},
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 3000,
    "temperature": 0.7
}


    response = requests.post(url, headers=headers, json=data)
    
    # Imprime la respuesta completa para depuración
    print("Response JSON:", response.json())

    # Intenta extraer el mensaje de la respuesta
    try:
        content = response.json()['choices'][0]['message']['content']
        return content
    except (KeyError, IndexError) as e:
        return f"Error extrayendo el mensaje: {str(e)}"

# Ejemplo de uso
descripcion_juego = (
    "6. Control de Luz con 3 Interruptores"
	"Problema: Controlar una luz desde tres interruptores distintos en diferentes ubicaciones (como un circuito de escalera)."
	"Solución: Usar interruptores (entradas) para controlar una luz (salida)."
	"Entradas: Interruptores 1, 2 y 3 (1 si están activados, 0 si no)."
	"Salidas: Luz (1 para encender, 0 para apagar)."
	"Uso de compuertas: Utiliza una combinación de compuertas XOR y AND para crear una lógica que permita encender o apagar la luz con cualquiera de los interruptores."
)
evaluacion = evaluar_juego_conversacional(descripcion_juego)
print("API:", evaluacion)