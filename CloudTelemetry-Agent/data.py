import os
import json
import random
import time
from datetime import datetime
from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient, Message

# Carga las variables del archivo .env 
load_dotenv()

def generar_telemetria(device_id):
    # Generar los datos aleatorios
    cpu = random.randint(0, 100)
    
    # Generar los datos de red
    latencia = random.randint(5, 150)  
    perdida = random.randint(0, 5)

    # Hora actual en formato de texto ISO 8601
    ahora = datetime.now().isoformat()

    # Crear un diccionario en Python 
    payload = {
        "device_id": device_id,
        "timestamp": ahora,
        "cpu_usage": cpu,
        "network_latency_ms": latencia,
        "packet_loss_pct": perdida
    }

    # Convertir el diccionario de Python a un string con formato JSON
    return json.dumps(payload)


if __name__ == "__main__":
    print("Iniciando CloudTelemetry-Agent para Azure...")
    
    # Obtener la cadena de conexión de forma segura
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    if not conn_str:
        print("Error: No se encontró la variable en el archivo .env")
        exit(1)

    # Inicializar el cliente de Azure
    cliente = IoTHubDeviceClient.create_from_connection_string(conn_str)
    cliente.connect()
    print("Conectado a Azure IoT Hub")
    
    while True:
        datos_json = generar_telemetria("upiita-router-01")
        
        # Empaquetar y enviar a Azure
        mensaje = Message(datos_json)
        mensaje.content_encoding = "utf-8"
        mensaje.content_type = "application/json"
        
        cliente.send_message(mensaje)
        print(f"Enviado a Azure: {datos_json}")
        
        time.sleep(5)
