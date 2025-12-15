# src/data/base_texts.py

TEXTOS_LEGALES = {
    # --- INDICES ESPECIALES (Se mantienen vacíos porque usan tablas dinámicas en el código) ---
    "CARACTERÍSTICAS DE LA LICITACIÓN": "",
    "GARANTÍAS": "",
    "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS": "",

    # --- TUS TEXTOS OFICIALES CON VARIABLES ---
    
    "OBJETIVOS": (
        "Las presentes bases contienen las disposiciones administrativas por las cuales se regirán e interpretarán "
        "las relaciones de <b>{organismo}</b> con las empresas oferentes del servicio requerido, durante el proceso de "
        "llamado a Licitación, presentación de las ofertas, su apertura, adjudicación y todas las materias relacionadas "
        "con esta Licitación. Esta iniciativa busca contratar un servicio especializado para: <b>{descripcion}</b>."
    ),

    "DEFINICIONES": (
        "Para la correcta interpretación de las presentes Bases, de los documentos de la Propuesta y del contrato que se celebre, "
        "se convienen las siguientes abreviaciones y definiciones:<br><br>"
        "<b>Bases:</b> las presentes Bases Administrativas y Técnicas, que regulan los requisitos, condiciones y especificaciones, "
        "establecidos por <b>{organismo}</b>, describen los servicios a contratar y regulan el proceso de Propuesta y el contrato definitivo.<br><br>"
        "<b>Bases Administrativas:</b> cuerpo o apartado de las Bases que regula, de manera general y/o particular, la forma de presentación "
        "de las propuestas técnicas y económicas, las etapas, plazos, mecanismos de consulta y/o aclaraciones, criterios de evaluación, "
        "mecanismo de adjudicación, cláusulas y/o condiciones del contrato definitivo, y demás aspectos administrativos del proceso de Propuesta.<br><br>"
        "<b>Bases Técnicas:</b> cuerpo o apartado normativo de las Bases que contiene de manera general y/o particular las especificaciones, "
        "descripciones, requisitos y demás características del servicio a contratar.<br><br>"
        "<b>Proponente u Oferente:</b> proveedor que participa en el proceso de propuesta mediante la presentación de una propuesta, "
        "en la forma y condiciones establecidas en estas Bases.<br><br>"
        "<b>Adjudicatario:</b> oferente cuya propuesta, presentada dentro del marco del proceso de Propuesta, es seleccionada y aceptada "
        "para la suscripción del contrato.<br><br>"
        "<b>Contrato:</b> instrumento que regula las condiciones de la prestación del servicio objeto de la presente licitación, suscrito "
        "entre el organismo y el proponente."
    ),

    "ORDEN DE PRECEDENCIA DE LOS DOCUMENTOS": (
        "La Propuesta y contrato respectivo a que pudiere dar lugar, se regirán por los siguientes documentos, cuyo orden de precedencia, "
        "en caso de existir discrepancia entre ellos, será el que a continuación se indica:<br>"
        "a) Las presentes Bases Administrativas y Técnicas.<br>"
        "b) El contrato respectivo.<br>"
        "c) La Propuesta, con todos sus documentos anexos."
    ),

    "CONTENIDO DE LAS BASES": (
        "Estas bases se encuentran conformadas por los siguientes cuerpos normativos:<br>"
        "I. Bases Administrativas.<br>"
        "II. Bases Técnicas.<br>"
        "III. Anexos (Calendario, Formularios, etc.)."
    ),

    "PLAZOS": (
        "La presente Propuesta se desarrollará conforme a los plazos que, para sus diversas etapas, se establecen en el Anexo N°1 “Calendario de la Propuesta”."
    ),

    "REQUISITOS DE LOS OFERENTES": (
        "Podrán participar en esta propuesta privada, las personas jurídicas que hayan sido invitadas formalmente al proceso y que cumplan con "
        "todas las exigencias establecidas en las presentes Bases. Para los efectos de esta Propuesta, los oferentes fijan domicilio en la "
        "comuna de Santiago, Región Metropolitana, y se someten a la jurisdicción de sus Tribunales de Justicia."
    ),

    "DURACIÓN Y FORMALIZACIÓN DE LA COMPRA": (
        "<b>{organismo}</b> comunicará por escrito la adjudicación del servicio al proponente seleccionado. El acuerdo entre las partes quedará "
        "formalizado mediante la firma de un contrato de prestación de servicios, en el cual se establecerán los derechos y obligaciones de ambos, "
        "según lo estipulado en las presentes bases y en la propuesta adjudicada. El plazo de duración será de <b>{duracion_contrato}</b>, "
        "contados desde la adjudicación de la presente licitación."
    ),

    "NOTIFICACIONES": (
        "Todas las notificaciones que hayan de efectuarse por parte de <b>{organismo}</b> con ocasión de la presente licitación serán enviadas por correo electrónico."
    ),

    "LLAMADO A PROPUESTA Y ENTREGA DE BASES": (
        "Se estimará, por el solo hecho de participar en este proceso, que el oferente conoce, acepta y está conforme con las presentes Bases y con todas "
        "las condiciones y exigencias en ellas establecidas y que, ante una eventual discrepancia entre su oferta y las Bases y sus aclaraciones complementarias, "
        "prevalecerán estas últimas, las que serán íntegramente respetadas."
    ),

    "CONSULTAS, ACLARACIONES Y MODIFICACIONES": (
        "Los proponentes podrán formular consultas o solicitar aclaraciones respecto de las presentes Bases, las que deberán ser realizadas únicamente a través "
        "del correo electrónico dentro del plazo establecido en el Anexo Nº1 “Calendario de la Propuesta”. <b>{organismo}</b> enviará a todos los oferentes las "
        "respuestas y aclaraciones solicitadas, a través de correo electrónico.<br>"
        "<b>{organismo}</b> podrá modificar, con a lo menos 24 horas de anticipación, los requerimientos de la licitación, informando por correo electrónico de ello "
        "a todas las personas invitadas a participar. Estas modificaciones formarán parte integrante de las bases originales."
    ),

    "PRESENTACIÓN DE LAS PROPUESTAS": (
        "Cada proponente podrá presentar una o más propuestas de acuerdo a lo indicado en el punto 6 letra c. La entrega de las propuestas, esto es, de la "
        "documentación correspondiente a las letras a), b) y c) del punto 6, deberá efectuarse a la apertura de las ofertas indicada en el Anexo 1 “Calendario de Propuesta”."
    ),

    "ENTREGA DE LAS PROPUESTAS": (
        "Las ofertas se dividirán en Oferta Técnica y Oferta Económica. Ambas se entregarán en forma física. Por otra parte, el oferente entregará el documento de "
        "garantía de seriedad de la oferta señalada en el punto 20, de manera física en la misma oportunidad, en sobre cerrado identificando claramente su contenido "
        "y al oferente al que pertenece. Las propuestas deberán ser entregadas en Profesora Amanda Labarca N°70, piso 5, Santiago."
    ),

    "APERTURA DE LAS PROPUESTAS": (
        "Inmediatamente después de haber recibido todas las propuestas, se revisará detalladamente si cada oferente cumple con los requisitos indicados en el punto 6 "
        "de las presentes bases. Esta operación comprende el análisis de fondo y forma de las garantías, poderes, y si los documentos respectivos están debidamente firmados."
    ),

    "ADMISIBILIDAD DE LA PROPUESTA": (
        "Podrán ser estimadas como causales de exclusión o eliminación de las propuestas las siguientes:<br>"
        "<ul>"
        "<li>Que la propuesta no haya sido entregada conforme a lo exigido en el punto 14 de las presentes bases.</li>"
        "<li>Que la propuesta no comprenda toda la documentación exigida en el punto 13 de las presentes bases.</li>"
        "</ul>"
        "<b>{organismo}</b> se reserva la facultad de admitir aquellas propuestas que presenten omisiones o defectos de forma o errores menores evidentes o que obedezcan "
        "a una justa causa de error, siempre que la información defectuosa o errónea no sea de fondo, no se refiera a aspectos esenciales, no altere el tratamiento "
        "igualitario de todos los proponentes y no impida la correcta evaluación de las propuestas."
    ),

    "ACLARACIONES": (
        "Durante el proceso de evaluación, <b>{organismo}</b> podrá solicitar a los oferentes las aclaraciones a sus propuestas que estime necesarias para una correcta "
        "evaluación de las mismas, las que deberán ser canalizadas e informadas al resto de los oferentes a través de correo electrónico. Con excepción de las situaciones "
        "precedentemente descritas, durante el período de evaluación los oferentes no podrán mantener contacto alguno con el organismo."
    ),

    "VALIDEZ DE LA PROPUESTA": (
        "Las ofertas, técnica y económica, tendrán una validez de 30 días contados desde la fecha de apertura de la propuesta. Si dentro de ese plazo no se puede efectuar "
        "la adjudicación, <b>{organismo}</b> podrá solicitar a los proponentes, antes de su expiración, la prórroga de las propuestas."
    ),

    "COMISIÓN DE EVALUACIÓN DE LAS OFERTAS": (
        "El análisis y evaluación de las propuestas estará a cargo de una Comisión de Evaluación integrada por la Subgerencia de Administración y Finanzas y Fiscalía de "
        "<b>{organismo}</b>. Corresponderá a la Comisión verificar la admisibilidad, realizar el proceso de evaluación y elaborar el Informe de Evaluación. La propuesta será "
        "resuelta por el Gerente General."
    ),

    "ACEPTACIÓN DE OFERTAS": (
        "<b>{organismo}</b> se reserva el derecho de aceptar cualquiera de las ofertas recibidas, sean éstas de una o más empresas oferentes o rechazarlas todas. En todos "
        "estos casos no requerirá dar expresión de causa de lo resuelto en uso de estas atribuciones, ni estará obligada al pago de indemnización alguna de eventuales "
        "perjuicios que produzcan estas decisiones."
    ),

    "ADJUDICACIÓN": (
        "La adjudicación de las ofertas se realizará dentro de los plazos y en las condiciones establecidas en el Anexo N°1, comunicando la decisión por correo electrónico "
        "a la empresa seleccionada y a los demás participantes."
    ),

    "SUSCRIPCIÓN DEL CONTRATO": (
        "El contrato respectivo deberá suscribirse dentro del plazo máximo de 05 días hábiles contado desde la fecha en que se notifique la adjudicación al oferente. "
        "Si el adjudicado no concurre a suscribir el convenio dentro del plazo señalado, se entenderá ipso facto que aquél no acepta la adjudicación y se procederá a ejecutar la garantía."
    ),

    "DOMICILIO": (
        "Para todos los efectos del contrato, las partes fijarán su domicilio en la ciudad de Santiago."
    ),

    "TERMINACIÓN ANTICIPADA DEL CONTRATO": (
        "<b>{organismo}</b> podrá poner término anticipado al contrato que se suscriba sin existir compensación económica asociada a este evento y en cualquiera de las situaciones "
        "que se señalan a continuación:<br>"
        "a) Si el adjudicatario se encuentra en estado de notoria insolvencia.<br>"
        "b) Si la calidad en la ejecución del servicio o en sus entregables finales no satisface las exigencias mínimas.<br>"
        "c) La condena del adjudicatario por cuasidelitos o delitos relacionados con responsabilidad.<br>"
        "d) Si así lo exigiera el interés público o la seguridad nacional.<br>"
        "e) Si las partes de común acuerdo convienen en dar término anticipado al convenio.<br>"
        "f) Por incumplimiento grave de las obligaciones que le impone el contrato."
    ),

    "SOLUCIÓN DE LAS CONTROVERSIAS": (
        "Durante la ejecución del convenio cualquier desacuerdo entre las partes será sometido a consideración del Gerente General de <b>{organismo}</b> y Gerente General de "
        "la Adjudicataria, o las personas que éstos designen, previo informe técnico y/o legal según corresponda, sin perjuicio de que las partes se someterán a la jurisdicción "
        "de los tribunales de justicia competentes de la ciudad de Santiago."
    ),

    "LUGAR Y UNIDAD DE TIEMPO EN QUE SE PRESTAN LOS SERVICIOS": (
        "[ESTA SECCIÓN DEBE SER PERSONALIZADA SEGÚN EL SERVICIO (EJ: PRESENCIAL/REMOTO, HORARIOS, PLAZOS DE ENTREGA)]."
    ),

    "SANCIONES POR INCUMPLIMIENTO": (
        "En caso de que el adjudicatario incurra en incumplimiento de las obligaciones contractuales, la Isapre podrá aplicar las siguientes sanciones:<br>"
        "<ul>"
        "<li><b>Multas por Atraso en la Entrega o Servicio:</b> Se aplicará una multa diaria [DEFINIR MONTO, EJ: 3 UF o 0,5%] por cada día de atraso.</li>"
        "<li><b>Multas por Incumplimiento de Especificaciones Técnicas:</b> Se aplicará una multa de [DEFINIR MONTO, EJ: 10 UF o 10%] por cada evento de incumplimiento.</li>"
        "<li><b>Multa por Incumplimiento de Confidencialidad o Interrupción del Servicio:</b> Considerada falta grave.</li>"
        "<li><b>Ejecución de la Garantía de Fiel Cumplimiento:</b> Por incumplimiento grave o acumulación de multas.</li>"
        "</ul>"
    ),

    "OBLIGACIÓN DE RESERVA Y USO DE INFORMACIÓN": (
        "La empresa adjudicataria queda obligada a mantener reserva de la información relativa al servicio, no difundir ni reproducir la información técnica o de beneficiarios, "
        "y mantener confidencialidad estricta con la información referida a los usuarios/afiliados de <b>{organismo}</b>. Especialmente, el cumplimiento de la Ley N° 19.628 sobre "
        "Protección de la Vida Privada."
    ),

    "FORMA DE PAGO / CONDICIONES DE PAGO Y FACTURACIÓN": (
        "[SELECCIONAR LA OPCIÓN QUE CORRESPONDA AL SERVICIO]:<br><br>"
        "<b>Opción A (Servicios Continuos):</b> El pago de cada factura se realizará dentro de los 30 días corridos siguientes a su correcta recepción por parte de la Isapre.<br><br>"
        "<b>Opción B (Por Hitos):</b> El valor total del servicio se pagará en cuotas, de acuerdo al detalle establecido en las bases (ej: 50% anticipo y 50% saldo)."
    ),

    "RESPONSABILIDAD": (
        "Serán de cargo y cuenta del proponente la contratación del personal necesario para la ejecución de las funciones que conlleve la labor y objeto de la presente licitación "
        "y, por lo tanto, será de su exclusiva responsabilidad el pago de remuneraciones y leyes sociales, no existiendo vínculo laboral ni contractual entre el personal del adjudicatario "
        "y <b>{organismo}</b>."
    )
}