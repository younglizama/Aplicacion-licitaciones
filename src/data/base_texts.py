# src/data/base_texts.py

TEXTOS_LEGALES = {
    # --- INDICES ESPECIALES (Tablas Dinámicas) ---
    "CARACTERÍSTICAS DE LA LICITACIÓN": "",
    "GARANTÍAS": "",
    "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS": "",

    # --- TEXTOS ADMINISTRATIVOS ---
    "OBJETIVOS": (
        "Las presentes bases contienen las disposiciones administrativas por las cuales se regirán e interpretarán "
        "las relaciones de <b>{organismo}</b> con las empresas oferentes del servicio requerido... "
        "Esta iniciativa busca contratar un servicio especializado para: <b>{descripcion}</b>."
    ),

    "DEFINICIONES": (
        "Para la correcta interpretación de las presentes Bases... se convienen las siguientes abreviaciones:<br><br>"
        "<b>Bases:</b> las presentes Bases Administrativas y Técnicas...<br>"
        "<b>Contrato:</b> instrumento que regula las condiciones suscrito entre <b>{organismo}</b> y el proponente."
    ),

    "ORDEN DE PRECEDENCIA DE LOS DOCUMENTOS": (
        "La Propuesta y contrato respectivo... se regirán por:<br>"
        "a) Las presentes Bases Administrativas y Técnicas.<br>"
        "b) El contrato respectivo.<br>"
        "c) La Propuesta, con todos sus documentos anexos."
    ),

    "CONTENIDO DE LAS BASES": (
        "Estas bases se encuentran conformadas por:<br>"
        "I. Bases Administrativas.<br>II. Bases Técnicas.<br>III. Anexos."
    ),

    "PLAZOS": "La presente Propuesta se desarrollará conforme a los plazos establecidos en el Anexo N°1 “Calendario”.",

    "REQUISITOS DE LOS OFERENTES": (
        "Podrán participar en esta propuesta privada las personas jurídicas invitadas que cumplan con las exigencias... "
        "Fijan domicilio en la comuna de Santiago."
    ),

    "DURACIÓN Y FORMALIZACIÓN DE LA COMPRA": (
        "<b>{organismo}</b> comunicará por escrito la adjudicación... El plazo de duración será de <b>{duracion_contrato}</b>, "
        "contados desde la adjudicación."
    ),

    "NOTIFICACIONES": "Todas las notificaciones serán enviadas por correo electrónico.",

    "LLAMADO A PROPUESTA Y ENTREGA DE BASES": "Se estimará que el oferente conoce y acepta las presentes Bases...",

    "CONSULTAS, ACLARACIONES Y MODIFICACIONES": (
        "Los proponentes podrán formular consultas vía correo electrónico según el Calendario... "
        "<b>{organismo}</b> podrá modificar los requerimientos con 24 horas de anticipación."
    ),

    "PRESENTACIÓN DE LAS PROPUESTAS": "Cada proponente podrá presentar una o más propuestas...",

    "ENTREGA DE LAS PROPUESTAS": (
        "Las ofertas Técnica y Económica se entregarán en forma física, junto con la garantía de seriedad, "
        "en Profesora Amanda Labarca N°70, piso 5, Santiago."
    ),

    "APERTURA DE LAS PROPUESTAS": "Se revisará detalladamente si cada oferente cumple con los requisitos...",

    "ADMISIBILIDAD DE LA PROPUESTA": (
        "Causales de exclusión:<br>"
        "<ul><li>Propuesta no entregada conforme al punto 14.</li><li>Falta de documentación exigida.</li></ul>"
        "<b>{organismo}</b> podrá admitir errores menores que no alteren el tratamiento igualitario."
    ),

    "ACLARACIONES": "Durante la evaluación, <b>{organismo}</b> podrá solicitar aclaraciones a las propuestas...",

    "VALIDEZ DE LA PROPUESTA": "Las ofertas tendrán una validez de 30 días contados desde la apertura.",

    "COMISIÓN DE EVALUACIÓN DE LAS OFERTAS": (
        "El análisis estará a cargo de una Comisión integrada por la Subgerencia de Administración y Finanzas y Fiscalía de <b>{organismo}</b>."
    ),

    "ACEPTACIÓN DE OFERTAS": "<b>{organismo}</b> se reserva el derecho de aceptar o rechazar cualquiera de las ofertas.",

    "ADJUDICACIÓN": "La adjudicación se realizará dentro de los plazos del Anexo N°1...",

    "SUSCRIPCIÓN DEL CONTRATO": "El contrato deberá suscribirse dentro del plazo máximo de 05 días hábiles...",

    "DOMICILIO": "Las partes fijarán su domicilio en la ciudad de Santiago.",

    "TERMINACIÓN ANTICIPADA DEL CONTRATO": (
        "<b>{organismo}</b> podrá poner término anticipado sin compensación si:<br>"
        "a) Insolvencia del adjudicatario.<br>b) Calidad deficiente.<br>c) Condena por delitos.<br>"
        "d) Interés público.<br>e) Mutuo acuerdo.<br>f) Incumplimiento grave."
    ),

    "SOLUCIÓN DE LAS CONTROVERSIAS": "Cualquier desacuerdo será sometido a consideración de los Gerentes Generales...",

    "LUGAR Y UNIDAD DE TIEMPO EN QUE SE PRESTAN LOS SERVICIOS": "[SECCIÓN A PERSONALIZAR SEGÚN SERVICIO]",

    "SANCIONES POR INCUMPLIMIENTO": (
        "Sanciones aplicables:<br>"
        "<ul><li><b>Multas por Atraso:</b> 3 UF o 0,5% diario.</li>"
        "<li><b>Multas por Incumplimiento Técnico:</b> 10 UF o 10% por evento.</li>"
        "<li><b>Confidencialidad:</b> Falta grave.</li></ul>"
    ),

    "OBLIGACIÓN DE RESERVA Y USO DE INFORMACIÓN": (
        "La empresa debe mantener estricta confidencialidad sobre la información de <b>{organismo}</b> y sus beneficiarios (Ley 19.628)."
    ),

    "FORMA DE PAGO / CONDICIONES DE PAGO Y FACTURACIÓN": (
        "<b>Opción A (Continuos):</b> Pago a 30 días contra recepción conforme.<br>"
        "<b>Opción B (Hitos):</b> Pago en cuotas según avance."
    ),

    "RESPONSABILIDAD": "El proponente es el único responsable de la contratación y pago de su personal.",

    # --- NUEVA SECCIÓN: BASES TÉCNICAS (TEXTO BASE) ---
    "BASES TÉCNICAS": (
        "<b>1. ANTECEDENTES GENERALES</b><br>"
        "<b>{organismo}</b> requiere contratar los servicios de una empresa especializada para [DESCRIBIR NECESIDAD]. "
        "El presente documento detalla las especificaciones técnicas y estándares de calidad exigidos.<br><br>"
        
        "<b>2. OBJETIVOS DEL SERVICIO</b><br>"
        "<b>Objetivo General:</b> Contratar un servicio experto para [OPTIMIZAR/MANTENER] la [OBJETO LICITACIÓN], "
        "garantizando la continuidad operativa.<br>"
        "<b>Objetivos Específicos:</b><br>"
        "<ul><li>Asegurar la calidad y disponibilidad del servicio.</li>"
        "<li>Cumplir con los plazos de respuesta.</li>"
        "<li>Proveer información clara mediante informes de gestión.</li></ul><br>"
        
        "<b>3. ALCANCE DEL SERVICIO</b><br>"
        "<b>3.1. Descripción:</b> El proveedor deberá realizar [DETALLAR ACCIONES] acorde a estas bases.<br>"
        "<b>3.2. Especificaciones Técnicas:</b> El servicio debe cumplir con:<br>"
        "<ul><li>[CARACTERÍSTICA 1]</li><li>[CARACTERÍSTICA 2]</li><li>[CARACTERÍSTICA 3]</li></ul><br>"
        
        "<b>4. METODOLOGÍA DE TRABAJO</b><br>"
        "El oferente deberá presentar un plan que incluya: forma de operación (horarios, logística), protocolos de contingencia y cronograma.<br><br>"
        
        "<b>5. ENTREGABLES E INFORMES</b><br>"
        "<ul><li><b>Informes de Avance:</b> Detalle de tareas y mediciones del periodo.</li>"
        "<li><b>Acta de Recepción:</b> Validación de conformidad del servicio.</li>"
        "<li><b>Informe Final:</b> Consolidado del servicio prestado.</li></ul><br>"
        
        "<b>6. NIVELES DE SERVICIO (SLA)</b><br>"
        "<ul><li><b>Atención Normal:</b> Plazo máximo [INDICAR TIEMPO].</li>"
        "<li><b>Urgencias:</b> Plazo máximo [INDICAR HORAS].</li>"
        "<li><b>Continuidad:</b> La interrupción se considera falta grave.</li></ul><br>"
        
        "<b>7. PERSONAL</b><br>"
        "El equipo debe contar con experiencia y certificaciones. El proveedor debe asegurar la disponibilidad del jefe de proyecto.<br><br>"
        
        "<b>8. GARANTÍA Y CALIDAD</b><br>"
        "Se debe cumplir con la normativa vigente y presentar protocolos de aseguramiento de calidad."
    )
}