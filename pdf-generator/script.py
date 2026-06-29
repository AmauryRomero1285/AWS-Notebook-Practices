"""
Genera un reporte PDF para el Laboratorio 3.6
con el estilo visual del Lab 3.1, e inserta las capturas de pantalla proporcionadas.
Incluye nombre del estudiante y matrícula en la portada.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage

# ------------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS (¡CAMBIA AQUÍ LA RUTA DE TUS IMÁGENES!)
# ------------------------------------------------------------

IMAGES_FOLDER = "C:/Users/Amaury/Downloads/cuper/Labs - AWS/Lab - 06"  # Cambia por tu ruta

# Lista de imágenes en el orden deseado (según el orden de las figuras en el PDF de ejemplo)
image_files = [
    "Captura de pantalla 2026-06-28 225800.png",
    "Captura de pantalla 2026-06-28 225823.png",
    "Captura de pantalla 2026-06-28 225842.png",
    "Captura de pantalla 2026-06-28 230317.png",
    "Captura de pantalla 2026-06-28 230457.png",
    "Captura de pantalla 2026-06-28 230350.png",
    "Captura de pantalla 2026-06-28 230423.png",
    "Captura de pantalla 2026-06-28 230457.png",
    "Captura de pantalla 2026-06-28 230603.png",
    "Captura de pantalla 2026-06-28 230630.png",
    "Captura de pantalla 2026-06-28 230700.png",
    "Captura de pantalla 2026-06-28 230737.png",
    "Captura de pantalla 2026-06-28 230813.png",
    "Captura de pantalla 2026-06-28 230836.png",
    "Captura de pantalla 2026-06-28 231019.png",
    "Captura de pantalla 2026-06-28 231556.png",
    "Captura de pantalla 2026-06-28 231613.png",
]

# Ruta completa de cada imagen
image_paths = [os.path.join(IMAGES_FOLDER, f) for f in image_files]

# ------------------------------------------------------------
# 2. DATOS DEL ESTUDIANTE Y FECHA
# ------------------------------------------------------------

titulo = "Guided Lab 3.6"
subtitulo = "AMAZON SAGEMAKER - GENERATING MODEL PERFORMANCE METRICS"
fecha = "28/06/2026"
nombre_estudiante = "Yared Amaury Romero Martínez"
matricula = "230190"

# ------------------------------------------------------------
# 3. CONTENIDO DEL REPORTE (extraído del PDF de ejemplo y adaptado)
# ------------------------------------------------------------

indice = [
    "Iniciar laboratorio",
    "Abrir la Consola de AWS",
    "Tarea 1: Acceder a una instancia de notebook en Amazon SageMaker",
    "Seguir las instrucciones del notebook",
    "Finalizar el laboratorio"
]

secciones = [
    {
        "titulo": "Iniciar laboratorio",
        "parrafos": [
            "<b>Iniciar laboratorio</b>",
            "Selecciona la opción Start Lab para iniciar el entorno del laboratorio.",
            "IMAGEN",  # Figura 1
            "<b>Estado de la sesión: en creación</b>",
            "El panel Start Lab se abre mientras se prepara el entorno.",
            "IMAGEN",  # Figura 2
            "<b>Esperar estado: listo</b>",
            "El estado del laboratorio cambia a 'ready' cuando está disponible.",
            "IMAGEN",  # Figura 3
        ]
    },
    {
        "titulo": "Abrir la Consola de AWS",
        "parrafos": [
            "<b>Abrir la Consola de AWS</b>",
            "Accede a la Consola de Administración de AWS mediante el botón AWS.",
            "IMAGEN",  # Figura 4
            "<b>Organizar pestañas del navegador</b>",
            "Organiza las pestañas lado a lado para seguir las instrucciones.",
            "IMAGEN",  # Figura 5
        ]
    },
    {
        "titulo": "Tarea 1: Acceder a una instancia de notebook en Amazon SageMaker",
        "parrafos": [
            "<b>Abrir Amazon SageMaker AI</b>",
            "En la Consola de AWS, en el menú Services, elige Amazon SageMaker AI.",
            "IMAGEN",  # Figura 6
            "<b>Navegar a Notebooks</b>",
            "En el menú de navegación izquierdo, expande Applications and IDEs y elige Notebooks.",
            "IMAGEN",  # Figura 7
            "<b>Abrir JupyterLab</b>",
            "Busca la instancia MyNotebook y abre JupyterLab.",
            "IMAGEN",  # Figura 8
            "<b>Localizar el archivo del notebook</b>",
            "En JupyterLab, localiza el archivo 3_6-machinelearning.ipynb.",
            "IMAGEN",  # Figura 9
            "<b>Abrir el notebook</b>",
            "Abre el notebook en JupyterLab para comenzar.",
            "IMAGEN",  # Figura 10
        ]
    },
    {
        "titulo": "Seguir las instrucciones del notebook",
        "parrafos": [
            "<b>Ejecutar las celdas del notebook</b>",
            "Sigue las instrucciones dentro del notebook para completar las tareas de métricas de rendimiento del modelo.",
            "IMAGEN",  # Figura 11
            "Continúa ejecutando las celdas para calcular las métricas.",
            "IMAGEN",  # Figura 12
            "Observa los resultados de las métricas del modelo.",
            "IMAGEN",  # Figura 13
            "Analiza los resultados generados.",
            "IMAGEN",  # Figura 14
            "Completa el análisis del rendimiento del modelo.",
            "IMAGEN",  # Figura 15
            "Visualiza las métricas de rendimiento.",
            "IMAGEN",  # Figura 16
            "Genera el reporte de métricas.",
            "IMAGEN",  # Figura 17
            "Resultados finales del notebook.",
            "IMAGEN",  # Figura 18
            "Métricas de rendimiento generadas exitosamente.",
            "IMAGEN",  # Figura 19
        ]
    },
    {
        "titulo": "Finalizar el laboratorio",
        "parrafos": [
            "<b>Confirmar finalización</b>",
            "Para finalizar el laboratorio, elige End Lab y luego Yes.",
            "IMAGEN",  # Figura 20
            "<b>Mensaje de eliminación</b>",
            "Aparece el mensaje: DELETE has been initiated...",
            "IMAGEN",  # Figura 21
            "<b>Cerrar el panel</b>",
            "Cierra el panel haciendo clic en la X en la esquina superior derecha.",
            "IMAGEN",  # Figura 22
            "Panel cerrado — laboratorio finalizado.",
            "IMAGEN",  # Figura 23
        ]
    }
]

# ------------------------------------------------------------
# 4. FUNCIÓN PARA CREAR EL PDF CON ESTILO MEJORADO
# ------------------------------------------------------------

def generar_pdf(nombre_archivo, secciones, image_paths):
    """Genera el PDF con el estilo visual del Lab 3.1."""

    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)

    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        'Titulo',
        parent=styles['Title'],
        fontSize=26,
        leading=30,
        textColor=colors.HexColor('#1A5276'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Times-Roman'
    )

    estilo_subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=styles['Heading2'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#2E86C1'),
        alignment=TA_CENTER,
        spaceAfter=18,
        fontName='Times-Roman'
    )

    estilo_datos = ParagraphStyle(
        'Datos',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Times-Roman'
    )

    estilo_seccion = ParagraphStyle(
        'Seccion',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1A5276'),
        spaceAfter=12,
        spaceBefore=18,
        fontName='Times-Roman'
    )

    estilo_normal = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        fontName='Times-Roman'
    )

    estilo_figura = ParagraphStyle(
        'Figura',
        parent=estilo_normal,
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=12,
        spaceBefore=6,
        fontName='Times-Roman'
    )

    estilo_indice = ParagraphStyle(
        'Indice',
        parent=estilo_normal,
        fontSize=12,
        leading=16,
        spaceAfter=4,
        leftIndent=20,
        fontName='Times-Roman'
    )

    elementos = []

    # --- PORTADA ---
    elementos.append(Paragraph(titulo, estilo_titulo))
    elementos.append(Paragraph(subtitulo, estilo_subtitulo))
    elementos.append(Spacer(1, 0.3*inch))
    elementos.append(Paragraph(f"Fecha: {fecha}", estilo_datos))
    elementos.append(Paragraph(f"Nombre: {nombre_estudiante}", estilo_datos))
    elementos.append(Paragraph(f"Matrícula: {matricula}", estilo_datos))
    elementos.append(Spacer(1, 0.5*inch))
    elementos.append(Paragraph("<hr/>", estilo_normal))
    elementos.append(Spacer(1, 0.3*inch))

    # --- ÍNDICE ---
    elementos.append(Paragraph("ÍNDICE", estilo_seccion))
    for i, item in enumerate(indice, start=1):
        elementos.append(Paragraph(f"{i}. {item}", estilo_indice))
    elementos.append(PageBreak())

    # --- CONTENIDO ---
    contador_imagenes = 0
    contador_figuras = 1

    MAX_WIDTH = 5.2 * inch
    MAX_HEIGHT = 5.5 * inch

    for sec in secciones:
        elementos.append(Paragraph(sec["titulo"], estilo_seccion))

        for parrafo in sec["parrafos"]:
            if parrafo == "IMAGEN":
                if contador_imagenes < len(image_paths):
                    ruta_img = image_paths[contador_imagenes]
                    if os.path.exists(ruta_img):
                        try:
                            with PILImage.open(ruta_img) as img_pil:
                                w, h = img_pil.size

                            escala_w = MAX_WIDTH / w
                            escala_h = MAX_HEIGHT / h
                            escala = min(escala_w, escala_h, 1.0)

                            nuevo_ancho = w * escala
                            nuevo_alto = h * escala

                            img = Image(ruta_img, width=nuevo_ancho, height=nuevo_alto)
                            img.hAlign = 'CENTER'
                            elementos.append(Spacer(1, 0.05*inch))
                            elementos.append(img)
                            elementos.append(Paragraph(f"<b>Figura {contador_figuras}</b>", estilo_figura))
                            contador_figuras += 1

                        except Exception as e:
                            elementos.append(Paragraph(f"<i>Error al cargar la imagen: {e}</i>", estilo_normal))
                    else:
                        elementos.append(Paragraph(f"<i>Imagen no encontrada: {os.path.basename(ruta_img)}</i>", estilo_normal))
                    contador_imagenes += 1
                else:
                    elementos.append(Paragraph("<i>[Imagen faltante]</i>", estilo_normal))
            else:
                elementos.append(Paragraph(parrafo, estilo_normal))

        elementos.append(Spacer(1, 0.2*inch))

    doc.build(elementos)
    print(f"✅ PDF generado: {nombre_archivo}")

# ------------------------------------------------------------
# 5. EJECUTAR
# ------------------------------------------------------------

if __name__ == "__main__":
    output_pdf = "Reporte_Lab_3.6_Yared_Romero_230190.pdf"
    generar_pdf(output_pdf, secciones, image_paths)