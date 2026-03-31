import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
from deep_translator import GoogleTranslator

# Lista de 40 palabras en inglés para el juego
palabras = [
    "apple", "banana", "cat", "dog", "house", "car", "tree", "sun", "moon", "star",
    "water", "fire", "earth", "wind", "book", "pen", "table", "chair", "door", "window",
    "school", "teacher", "student", "friend", "family", "food", "drink", "music", "dance", "game",
    "computer", "phone", "watch", "shoe", "hat", "shirt", "pants", "bird", "fish", "flower"
]

duration = 3  # segundos de grabación
sample_rate = 44100  # frecuencia de muestreo

print("🌟 ¡Bienvenido al juego de pronunciación en inglés! 🌟")
print("Elige un nivel: fácil (10 palabras), medio (20 palabras), difícil (40 palabras)")

nivel = input("Ingresa 'facil', 'medio' o 'dificil': ").lower()
if nivel == 'facil':
    palabras_nivel = palabras[:10]
elif nivel == 'medio':
    palabras_nivel = palabras[:20]
elif nivel == 'dificil':
    palabras_nivel = palabras
else:
    print("Nivel no válido. Saliendo.")
    exit()

# Mezclar las palabras del nivel
random.shuffle(palabras_nivel)

acertadas = 0
total = len(palabras_nivel)

translator = GoogleTranslator(source='en', target='es')

for palabra in palabras_nivel:
    # Traducir la palabra al español
    traduccion = translator.translate(palabra)
    print(f"\n🔤 Traducción al español: {traduccion}")
    print("🎙️ Pronuncia la palabra en inglés ahora...")
    
    # Grabar audio
    recording = sd.rec(
        int(duration * sample_rate),  # el número de muestras a grabar
        samplerate=sample_rate,       # tasa de muestreo
        channels=1,                   # 1 significa grabación mono
        dtype="int16"                 # tipo de datos para las muestras grabadas
    )
    sd.wait()  # esperando a que termine la grabación

    # Guardar el audio
    wav.write("output.wav", sample_rate, recording)
    print("✅ Grabación completa, procesando...")

    # Reconocer el habla
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    text = None
    try:
        text = recognizer.recognize_google(audio, language="en")
        print(f"Dijiste: {text}")
        
        # Comparar con la palabra correcta
        if text and text.lower().strip() == palabra.lower():
            acertadas += 1
            print("🎉 ¡Correcto! +1 punto")
        else:
            print(f"❌ Incorrecto. La respuesta correcta era: '{palabra}'. Sigue practicando.")
    
    except sr.UnknownValueError:
        print("⚠️ No se pudo reconocer el habla. Intenta de nuevo.")
    except sr.RequestError as e:
        print(f"⚠️ Error del servicio: {e}")

    try:
        continuar = input("¿Quieres continuar? (s/n): ").lower()
    except EOFError:
        continuar = 'n'

    if continuar != 's':
        print("👋 Juego pausado. Vamos con resultados.")
        break

# Calcular estadísticas
falladas = total - acertadas
porcentaje = (acertadas / total) * 100 if total > 0 else 0

print("\n🏁 ¡Juego terminado!")
print(f"✅ Palabras acertadas: {acertadas}")
print(f"❌ Palabras falladas: {falladas}")
print(f"🎯 Porcentaje de acierto: {porcentaje:.2f}%")
