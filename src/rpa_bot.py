import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

from whatsapp_sender import enviar_mensaje_whatsapp

class RPAAnalisisVentas:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.df_ventas = None
        self.df_vehiculos = None
        self.df_completo = None
        self.metricas = {}
        
        if not os.path.exists('reports'):
            os.makedirs('reports')

    def extraer_datos(self):
        try:
            print("Iniciando extracción de datos...")
            self.df_ventas = pd.read_excel(self.ruta_archivo, sheet_name='VENTAS')
            self.df_vehiculos = pd.read_excel(self.ruta_archivo, sheet_name='VEHICULOS')
            
            self.df_completo = pd.merge(
                self.df_ventas, 
                self.df_vehiculos, 
                left_on='ID_Vehículo', 
                right_on='ID_Vehiculo', 
                how='left'
            )
            print("Datos extraídos y unificados correctamente.")
        except Exception as e:
            print(f"Error al leer el archivo Excel: {e}")
            raise

    def calcular_metricas(self):
        try:
            print("Calculando métricas...")
            df = self.df_completo
            
            ventas_por_sede = df.groupby('Sede')['Precio Venta sin IGV'].sum()
            top_modelos = df['MODELO'].value_counts().head(5)
            ventas_por_canal = df['Canal'].value_counts()
            segmento_clientes = df.groupby('Segmento')['Precio Venta sin IGV'].sum()
            
            clientes_unicos = df['Cliente'].nunique()
            cantidad_ventas = len(df)
            total_sin_igv = df['Precio Venta sin IGV'].sum()
            total_con_igv = df['Precio Venta Real'].sum()

            self.metricas = {
                'ventas_por_sede': ventas_por_sede,
                'top_modelos': top_modelos,
                'ventas_por_canal': ventas_por_canal,
                'segmento_clientes': segmento_clientes,
                'clientes_unicos': clientes_unicos,
                'cantidad_ventas': cantidad_ventas,
                'total_sin_igv': total_sin_igv,
                'total_con_igv': total_con_igv
            }
            print("Métricas calculadas.")
        except Exception as e:
            print(f"Error en los cálculos: {e}")
            raise

    def generar_visualizaciones(self):
        try:
            print("Generando gráficos...")
            m = self.metricas
            
            plt.figure(figsize=(10, 6))
            m['ventas_por_sede'].plot(kind='bar', color='skyblue')
            plt.title('Ventas sin IGV por Sede')
            plt.ylabel('Monto ($)')
            plt.tight_layout()
            plt.savefig('reports/ventas_por_sede.png')
            plt.close()

            plt.figure(figsize=(10, 6))
            m['top_modelos'].plot(kind='barh', color='lightgreen')
            plt.title('Top 5 Modelos Más Vendidos')
            plt.xlabel('Cantidad')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig('reports/top_5_modelos.png')
            plt.close()

            plt.figure(figsize=(10, 6))
            m['ventas_por_canal'].plot(kind='bar', color='coral')
            plt.title('Ventas por Canal')
            plt.ylabel('Cantidad de Ventas')
            plt.tight_layout()
            plt.savefig('reports/ventas_por_canal.png')
            plt.close()

            plt.figure(figsize=(8, 8))
            m['segmento_clientes'].plot(kind='pie', autopct='%1.1f%%', startangle=90)
            plt.title('Ventas sin IGV por Segmento de Cliente')
            plt.ylabel('')
            plt.tight_layout()
            plt.savefig('reports/segmento_clientes.png')
            plt.close()

            print("Gráficos guardados en la carpeta 'reports/'.")
        except Exception as e:
            print(f"Error al generar visualizaciones: {e}")
            raise

    def generar_dashboard(self):
        try:
            print("Generando Dashboard consolidado...")
            m = self.metricas
            
            fig, axes = plt.subplots(2, 2, figsize=(16, 10))
            fig.suptitle('DASHBOARD RESUMEN DE VENTAS', fontsize=20, fontweight='bold', color='#333333')

            m['ventas_por_sede'].plot(kind='bar', color='skyblue', ax=axes[0, 0])
            axes[0, 0].set_title('Ventas sin IGV por Sede')
            axes[0, 0].set_ylabel('Monto ($)')
            axes[0, 0].tick_params(axis='x', rotation=45)

            m['top_modelos'].plot(kind='barh', color='lightgreen', ax=axes[0, 1])
            axes[0, 1].set_title('Top 5 Modelos Más Vendidos')
            axes[0, 1].set_xlabel('Cantidad')
            axes[0, 1].invert_yaxis()

            m['ventas_por_canal'].plot(kind='bar', color='coral', ax=axes[1, 0])
            axes[1, 0].set_title('Ventas por Canal')
            axes[1, 0].set_ylabel('Cantidad')
            axes[1, 0].tick_params(axis='x', rotation=45)

            m['segmento_clientes'].plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=axes[1, 1])
            axes[1, 1].set_title('Ventas por Segmento')
            axes[1, 1].set_ylabel('')

            plt.tight_layout()
            fig.subplots_adjust(top=0.90) 
            
            plt.savefig('reports/DASHBOARD_RESUMEN.png')
            plt.close()
            
            print("✅ Dashboard guardado como 'DASHBOARD_RESUMEN.png'.")
        except Exception as e:
            print(f"Error al generar el dashboard: {e}")
            raise


    def preparar_y_enviar_reporte(self):
        try:
            m = self.metricas
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            
            top_modelos_str = "\n".join([f"• {modelo}: {cant} unds." for modelo, cant in m['top_modelos'].items()])
            top_canales_str = "\n".join([f"• {canal}: {cant} ventas" for canal, cant in m['ventas_por_canal'].items()])
            sedes_str = "\n".join([f"• {sede}: ${monto:,.2f}" for sede, monto in m['ventas_por_sede'].sort_values(ascending=False).items()])
            
            mensaje_reporte = (
                f"📊 *REPORTE COMPLETO DE VENTAS* 📊\n"
                f"Fecha: {fecha_actual}\n\n"
                f"📈 *MÉTRICAS CLAVE (Totalizadores)*\n"
                f"• Transacciones: {m['cantidad_ventas']}\n"
                f"• Clientes Únicos: {m['clientes_unicos']}\n"
                f"• Total Ventas (Sin IGV): ${m['total_sin_igv']:,.2f}\n"
                f"• Total Ventas (Con IGV): ${m['total_con_igv']:,.2f}\n\n"
                f"🚗 *TOP 5 MODELOS MÁS VENDIDOS*\n"
                f"{top_modelos_str}\n\n"
                f"📺 *VENTAS POR CANAL*\n"
                f"{top_canales_str}\n\n"
                f"📍 *VENTAS POR SEDE (Sin IGV)*\n"
                f"{sedes_str}\n\n"
                f"📁 _Nota: Los 4 gráficos de análisis visual han sido generados y guardados exitosamente en la carpeta local 'reports/'_"
            )
            
            enviar_mensaje_whatsapp(mensaje_reporte)
        except Exception as e:
            print(f"Error al preparar el reporte: {e}")
            raise

if __name__ == "__main__":
    ruta_excel = 'data/Ventas - Fundamentos.xlsx'
    
    bot = RPAAnalisisVentas(ruta_excel)
    bot.extraer_datos()
    bot.calcular_metricas()
    bot.generar_visualizaciones()
    bot.generar_dashboard()
    bot.preparar_y_enviar_reporte()