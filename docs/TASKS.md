# Tareas

Lista unificada de tareas pendientes del proyecto `skeleton_qt`.

## Convenciones

- **ID**: identificador estable `Txx`.
- **Prioridad**: Alta, Media o Baja.
- Las tareas están divididas en unidades pequeñas para poder implementarlas y verificarlas de forma independiente.
- Cuando una tarea tenga dependencia explícita, debe abordarse después de la tarea indicada.

---

## Refactoring

| Status | ID  | Priority | Description |
|:------:|:---:|:--------:|:------------|
| ✅ | T00 | **Prioridad:** Alta | Corregir `TextBinder.bind()` para sources no-callable. Revisar el contrato de `TextBinder.bind()` para aceptar correctamente sources `Callable` y valores de texto directos, evitando llamadas como `source()` cuando el source no es callable.|
| ✅ | T01 | **Prioridad:** Alta | Adaptar `MainWindow.bind_text()` al contrato de `TextBinder`. Actualizar `MainWindow.bind_text()` para utilizar correctamente el contrato corregido de `TextBinder`.|
| ✅ | T02 | **Prioridad:** Alta | Adaptar `BaseView.bind_text()` al contrato de `TextBinder`. Actualizar `BaseView.bind_text()` para utilizar correctamente el contrato corregido de `TextBinder`.|
| ✅ | T03 | **Prioridad:** Alta | Añadir pruebas para `TextBinder` con callable y texto directo. Cubrir con tests los casos válidos de source callable, texto directo, setter explícito y setter por defecto.|
| ⏳ | T04 | **Prioridad:** Alta | Añadir desplegable de categorías en `LogsView`. Crear un desplegable seleccionable, utilizando el custom widget `CheckableComboBox`, para que el usuario pueda elegir qué categorías de logging se muestran en el panel de logs de la vista de logs.|
| ⏳ | T05 | **Prioridad:** Alta | Homogeneizar convención de nombres para componentes MVC. Alinear naming de Model, View y Controller con patrón consistente (`X_Model`, `X_View`, `X_Controller`) sin variaciones entre features.|
| ⏳ | T06 | **Prioridad:** Alta | Establecer guías de estilo para docstrings en Python. Definir formato estándar para parámetros, tipos de retorno, descripciones y casos especiales (exceptions, side effects).|
| ⏳ | T07 | **Prioridad:** Alta | Revisar README contra implementación actual. Actualizar descripción de arquitectura, estructura y componentes para reflejar fielmente el código existente.|
| ⏳ | T08 | **Prioridad:** Alta | Documentar flujos de error comunes y su manejo. Crear documentación interna sobre errores esperados en HTTP clients, providers externos y operaciones asíncronas.|
| ⏳ | T09 | **Prioridad:** Alta | Corregir docstrings desactualizados. Revisar los docstrings identificados durante la auditoría y corregir parámetros, tipos, retornos y descripciones que ya no representan el código actual.|
| ⏳ | T10 | **Prioridad:** Alta | Simplificar `Application._setup_menus()`. Revisar la estructura actual de definiciones, creación y registro de acciones para eliminar complejidad innecesaria sin introducir una abstracción excesiva.|
| ⏳ | T11 | **Prioridad:** Media | Integrar la revisión de temas dinámicos en `_setup_menus()`. Adaptar la simplificación de `_setup_menus()` para que pueda construir posteriormente el menú de temas de forma dinámica.|
| ⏳ | T12 | **Prioridad:** Media | Revisar el manejo de excepciones de `TextBinder.refresh()`. Determinar si el `RuntimeError` capturado corresponde realmente al caso de widgets Qt destruidos y evitar ocultar errores producidos por setters.|
| ⏳ | T13 | **Prioridad:** Media | Revisar el contrato de `LogsView.append_log()`. Determinar qué parámetros necesita realmente `LogsView.append_log()` y eliminar parámetros innecesarios o justificar los que formen parte de un contrato común.|
| ⏳ | T14 | **Prioridad:** Media | Revisar el flujo de `clear` de `LogsView`. Analizar la señal `clear_requested` y el flujo entre `LogsView`, `Controller` y `LogsModel` para mantener una separación clara de responsabilidades.|
| ⏳ | T15 | **Prioridad:** Media | Refactorizar `SpeedometerProgress`: API. Revisar métodos, parámetros, tipos y responsabilidades del widget antes de integrarlo en `VideoUploader`.|
| ⏳ | T16 | **Prioridad:** Media | Refactorizar `SpeedometerProgress`: estilo y configuración. Adaptar colores, fuentes, configuración y documentación del widget a las convenciones del proyecto.|
| ⏳ | T17 | **Prioridad:** Media | Diseñar la API de `HttpClient`. Definir responsabilidades, configuración, errores, timeouts y contrato público del cliente HTTP antes de implementar proveedores.|
| ⏳ | T18 | **Prioridad:** Media | Implementar la base de `HttpClient`. Implementar el cliente HTTP genérico definido en T17, manteniéndolo independiente de YouTube, Instagram y TikTok.|
| ⏳ | T19 | **Prioridad:** Media | Revisar acciones placeholder de Edit. Determinar el comportamiento correcto de `Cut`, `Copy` y `Paste`: implementación, deshabilitación o mantenimiento como acciones educativas.|
| ⏳ | T20 | **Prioridad:** Baja | Revisar modelos vacíos y logging compartido. Determinar si los modelos vacíos actuales necesitan una estructura común para logging o si deben mantenerse como puntos de extensión mínimos.|
| ⏳ | T21 | **Prioridad:** Baja | Revisar naming de handlers `_action_X_button`. Evaluar y normalizar la nomenclatura de los handlers de botones sin modificarla si no aporta una mejora real.|
| ⏳ | T22 | **Prioridad:** Baja | Corregir comparación de strings en `BaseView.setup_ui()`. Sustituir comparaciones `is not` aplicadas a strings por `!=` para eliminar la dependencia accidental de interning.|
| ⏳ | T23 | **Prioridad:** Alta | Separar configuración de logging por salida. Definir el estado configurable de las salidas `Console`, `File` y `GUI`, sustituyendo el modelo actual que trata la salida GUI de forma independiente.|
| ⏳ | T24 | **Prioridad:** Alta | Añadir checkbox de salida Console en Settings. Añadir el control visual para activar/desactivar la salida de consola.|
| ⏳ | T25 | **Prioridad:** Alta | Añadir checkbox de salida File en Settings. Añadir el control visual para activar/desactivar la salida a fichero.|
| ⏳ | T26 | **Prioridad:** Alta | Añadir checkbox de salida GUI en Settings. Sustituir el actual `Enable logging` por el selector específico de salida GUI.|
| ⏳ | T27 | **Prioridad:** Alta | Conectar Settings con `LoggingManager` para las tres salidas. Propagar correctamente los cambios de Console/File/GUI hasta `LoggingManager`.|
| ⏳ | T28 | **Prioridad:** Media | Añadir configuración de plataformas. Completar en Settings los checkboxes de plataformas pendientes.|
| ⏳ | T29 | **Prioridad:** Media | Añadir opción de vaciado del fichero al salir. Implementar el comportamiento de la opción `Clear log file on exit`.|
| ⏳ | T30 | **Prioridad:** Media | Diseñar persistencia de configuración en INI. Definir qué opciones se persisten, dónde se almacena el fichero y cómo se cargan valores por defecto.|
| ⏳ | T31 | **Prioridad:** Media | Implementar lectura de configuración INI. Cargar la configuración persistida durante el arranque de la aplicación.|
| ⏳ | T32 | **Prioridad:** Media | Implementar escritura de configuración INI. Persistir los cambios realizados desde Settings.|
| ⏳ | T33 | **Prioridad:** Media | Conectar Settings con la persistencia. Hacer que los controles de Settings actualicen y recuperen la configuración persistida.|
| ✅ | T34 | **Prioridad:** Media | Mover selector de categorías a `LogsView`. Trasladar el selector de categorías desde Settings al panel global de Logs.|
| ⏳ | T35 | **Prioridad:** Media | Añadir selector de niveles en `LogsView`. Permitir seleccionar los niveles de logging que se desean visualizar.|
| ⏳ | T36 | **Prioridad:** Media | Implementar filtrado real de categorías. Aplicar la selección de categorías al contenido mostrado en LogsView.|
| ⏳ | T37 | **Prioridad:** Media | Implementar filtrado real de niveles. Aplicar la selección de niveles al contenido mostrado en LogsView.|
| ⏳ | T38 | **Prioridad:** Media | Refrescar historial y filtrado al cambiar criterios. Asegurar que cambiar filtros actualiza correctamente los registros ya almacenados y los nuevos mensajes.|
| ⏳ | T39 | **Prioridad:** Baja | Documentar acciones educativas de Edit. Explicar en README el propósito de `Cut`, `Copy` y `Paste` si permanecen como acciones educativas.|
| ⏳ | T40 | **Prioridad:** Baja | Documentar acciones educativas de Help. Explicar en README el propósito provisional/educativo de las acciones de Help.|
| ⏳ | T41 | **Prioridad:** Baja | Añadir comentarios aclaratorios donde aporten valor. Documentar decisiones arquitectónicas no evidentes sin llenar el código de comentarios redundantes.|
| ⏳ | T42 | **Prioridad:** Media | Integrar `SpeedometerProgress` en `VideoUploaderView`. Integrar el widget después de completar T14 y T15.|
| ⏳ | T43 | **Prioridad:** Media | Conectar progreso real del proceso de subida. Conectar el progreso del uploader con `SpeedometerProgress` cuando exista el flujo de subida correspondiente.|
| ⏳ | T44 | **Prioridad:** Media | Definir infraestructura común para providers. Determinar cómo consumirán `HttpClient` los distintos providers sin introducir dependencias innecesarias.|
| ⏳ | T45 | **Prioridad:** Media | Implementar provider YouTube. Implementar la integración REST de YouTube utilizando el cliente HTTP común.|
| ⏳ | T46 | **Prioridad:** Media | Implementar provider Instagram. Implementar la integración REST de Instagram utilizando el cliente HTTP común.|
| ⏳ | T47 | **Prioridad:** Media | Implementar provider TikTok. Implementar la integración REST de TikTok utilizando el cliente HTTP común.|
| ⏳ | T48 | **Prioridad:** Media | Integrar providers con `VideoUploaderModel`. Conectar los providers con la lógica del modelo manteniendo la View independiente de las APIs externas.|
| ⏳ | T49 | **Prioridad:** Media | Añadir gestión de errores de providers. Normalizar errores HTTP/API y su comunicación hacia la aplicación.|
| ⏳ | T50 | **Prioridad:** Media | Diseñar responsabilidades de `RouteDesignerModel`. Definir qué lógica de cálculo/datos debe pertenecer al modelo.|
| ⏳ | T51 | **Prioridad:** Media | Diseñar interfaz de `RouteDesignerView`. Definir los controles necesarios respetando la arquitectura MVC existente.|
| ⏳ | T52 | **Prioridad:** Media | Implementar `RouteDesignerModel`. Implementar la lógica definida en T50.|
| ⏳ | T53 | **Prioridad:** Media | Implementar `RouteDesignerView`. Implementar la interfaz definida en T51.|
| ⏳ | T54 | **Prioridad:** Media | Conectar Route Designer con Controller. Integrar la funcionalidad completa sin introducir un controller específico para la feature.|
| ⏳ | T55 | **Prioridad:** Alta | Mantener tests de regresión del refactoring. Actualizar y ampliar los tests afectados por T00–T22.|
| ⏳ | T56 | **Prioridad:** Media | Añadir tests de configuración. Cubrir configuración de logging, plataformas y persistencia INI.|
| ⏳ | T57 | **Prioridad:** Media | Añadir tests de filtrado de logs. Cubrir categorías, niveles y actualización de la vista.|
| ⏳ | T58 | **Prioridad:** Media | Añadir tests de `SpeedometerProgress`. Cubrir API pública y casos límite relevantes.|
| ⏳ | T59 | **Prioridad:** Media | Añadir tests de `HttpClient`. Cubrir requests, errores, timeouts y comportamiento común.|
| ⏳ | T60 | **Prioridad:** Media | Añadir tests de providers. Cubrir la integración de YouTube, Instagram y TikTok mediante mocks/control de respuestas.|
| ⏳ | T61 | **Prioridad:** Media | Revisar suite completa de tests. Ejecutar y revisar la suite completa después de cada bloque funcional importante.|
| ⏳ | T62 | **Prioridad:** Alta | Incluir `resources/` recursivamente en PyInstaller. **Dependencia:** T62 debe completarse antes de T64–T66. Sustituir las listas manuales de recursos de `skeleton_qt.spec` por una inclusión genérica y recursiva de toda la carpeta `resources/`.|
| ⏳ | T63 | **Prioridad:** Alta | Verificar empaquetado de recursos en Windows y Linux. **Dependencia:** T62 debe completarse antes de T64–T66. Comprobar que traducciones, estilos y assets se encuentran correctamente en el binario empaquetado.|
| ⏳ | T64 | **Prioridad:** Alta | Descubrir temas disponibles desde `resources/styles/`. **Dependencia:** T62 debe completarse antes de T64–T66. Implementar el descubrimiento dinámico de ficheros `.qss` en lugar de mantener `light` y `dark` cableados.|
| ⏳ | T65 | **Prioridad:** Alta | Validar identificadores y nombres de temas descubiertos. **Dependencia:** T62 debe completarse antes de T64–T66. Definir cómo se obtiene el identificador del tema a partir del nombre del fichero y cómo se manejan nombres inválidos.|
| ⏳ | T66 | **Prioridad:** Alta | Generar dinámicamente el menú de Temas. **Dependencia:** T62 debe completarse antes de T64–T66. Crear las acciones del menú Options a partir de los temas descubiertos en `resources/styles/`.|
| ⏳ | T67 | **Prioridad:** Alta | Integrar temas dinámicos con traducción y selección exclusiva. Mantener el comportamiento de traducción, `QActionGroup` y estado seleccionado con el nuevo sistema dinámico.|
| ⏳ | T68 | **Prioridad:** Alta | Verificar temas dinámicos en desarrollo y binario. Comprobar que un tema nuevo añadido a `resources/styles/` aparece tanto en ejecución normal como en la aplicación empaquetada.|
| ⏳ | T69 | **Prioridad:** Media | Completar configuración de Settings. Integrar de forma coherente las opciones de plataformas, salidas de logging y persistencia.|
| ⏳ | T70 | **Prioridad:** Media | Completar sistema de logging. Integrar categorías, niveles, salidas y filtros en un flujo coherente.|
| ⏳ | T71 | **Prioridad:** Media | Completar VideoUploader. Finalizar la interfaz y progreso después de completar las tareas precedentes.|
| ⏳ | T72 | **Prioridad:** Media | Completar providers. Finalizar YouTube, Instagram y TikTok después de `HttpClient`.|
| ⏳ | T73 | **Prioridad:** Media | Completar Route Designer. Finalizar la feature después de disponer de la infraestructura HTTP y del orden funcional establecido.|
| ⏳ | T74 | **Prioridad:** Baja | Revisión final de arquitectura. Revisar que las funcionalidades añadidas mantienen MVC, el Controller único, la separación View/Model y la simplicidad del skeleton.|
| ⏳ | T75 | **Prioridad:** Baja | Revisión final de documentación. Actualizar README, estructura del proyecto y documentación de configuración/empaquetado.|
| ⏳ | T76 | **Prioridad:** Baja | Revisión final de empaquetado. Realizar una verificación final de los builds y recursos incluidos en las plataformas soportadas.|
