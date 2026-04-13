# RPA para Análisis de Ventas y Notificación vía WhatsApp

Automatización en Python para el procesamiento, análisis y reporte de datos de ventas de una concesionaria. El bot realiza ETL desde Excel, genera métricas y visualizaciones, y envía resúmenes por WhatsApp mediante Twilio.

## Funcionalidades
- **ETL Automatizado:** Lee archivos Excel (múltiples hojas) y combina registros para obtener una base de datos consistente.
- **Análisis financiero:** Calcula métricas clave: ventas totales (con/sin IGV), ticket promedio y clientes únicos.
- **Visualizaciones:** Genera gráficos (barras, horizontales, circulares) y un dashboard consolidado en PNG.
- **Notificaciones:** Envía reportes ejecutivos por WhatsApp usando la API de Twilio.

## Tecnologías
- **Lenguaje:** Python 3.13+
- **Data:** pandas, numpy
- **Excel:** openpyxl
- **Visualización:** matplotlib
- **Mensajería:** Twilio (API WhatsApp)
- **Configuración:** python-dotenv

## Estructura del proyecto

```
rpa-analisis-ventas/
├── data/                # Datos de entrada (Excel)
├── reports/             # Salida: gráficos y dashboard (.png)
├── src/
│   ├── __init__.py
│   ├── rpa_bot.py       # Motor principal
│   └── whatsapp_sender.py # Integración con Twilio
├── .env                 # Variables de entorno (no versionar)
├── requirements.txt
└── README.md
```

## Requisitos
- Python 3.13 o superior
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Instalación y ejecución

1. Clonar el repositorio y crear un entorno virtual:

```bash
git clone <url-del-repositorio>
cd rpa-analisis-ventas
python -m venv venv
```

2. Activar el entorno (Windows):

```powershell
venv\\Scripts\\Activate.ps1
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear el archivo `.env` en la raíz con las credenciales necesarias:

```env
TWILIO_ACCOUNT_SID=tu_sid_aqui
TWILIO_AUTH_TOKEN=tu_token_aqui
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TO_WHATSAPP_NUMBER=whatsapp:+58412XXXXXXX
```

5. Ejecutar el bot (asegúrate de tener el archivo Excel en `data/`):

```bash
python src/rpa_bot.py
```

## Qué produce
- Archivos de imagen con gráficos y un dashboard en la carpeta `reports/`.
- Resumen ejecutivo enviado por WhatsApp (si `.env` está configurado).

## Métricas y análisis incluidos
- Top 5 modelos por volumen de ventas
- Rendimiento por sede (ingresos brutos)
- Análisis por canal de captación
- Segmentación de ventas por tipo de cliente

---

