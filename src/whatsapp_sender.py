import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def enviar_mensaje_whatsapp(cuerpo_mensaje):
    
    try:
        print("Preparando envío de reporte por WhatsApp...")
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_whatsapp_number = os.getenv('TWILIO_WHATSAPP_FROM') 
        to_whatsapp_number = os.getenv('TO_WHATSAPP_NUMBER')    

        if not all([account_sid, auth_token, from_whatsapp_number, to_whatsapp_number]):
            raise ValueError("Faltan credenciales de Twilio en el archivo .env")

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=cuerpo_mensaje,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )

        print(f"✅ Reporte enviado exitosamente. Message SID: {message.sid}")

    except Exception as e:
        print(f"❌ Error al enviar el mensaje por WhatsApp: {e}")