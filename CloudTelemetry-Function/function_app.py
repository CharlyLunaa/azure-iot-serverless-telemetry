import azure.functions as func
import logging
import json
import uuid

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="mensajes-iot", connection="IoTHubConnection")
@app.cosmos_db_output(arg_name="outputDocument", database_name="TelemetriaDB", container_name="Escribe Mensajes", connection="CosmosDBConnection")
def ProcesarTelemetria(azeventhub: func.EventHubEvent, outputDocument: func.Out[func.Document]):
    logging.info('Azure Function procesó un evento de telemetría.')
    
    cuerpo_mensaje = azeventhub.get_body().decode('utf-8')
    
    try:
        datos = json.loads(cuerpo_mensaje)
        logging.info(f"Datos recibidos: {datos}")
        
        # 1. Crear un ID único (Cosmos DB requiere estrictamente un campo "id" en formato texto)
        datos["id"] = str(uuid.uuid4())
        
        # 2. Lógica básica: Detectar latencia alta
        latencia = datos.get("network_latency_ms", 0)
        if latencia > 100:
            logging.warning(f"¡ALERTA! Alta latencia detectada en {datos.get('device_id')}: {latencia}ms")
            
        # 3. Guardar en Cosmos DB usando el Output Binding
        outputDocument.set(func.Document.from_dict(datos))
        logging.info("Dato guardado exitosamente en Cosmos DB.")
            
    except ValueError:
        logging.error("Error: El mensaje recibido no es un JSON válido.")

        #func start