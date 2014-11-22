# Web de la asociación python Mallorca

**Django estándar**, copiar el app.ini.template a app.ini, y configurándolo.

El propio sistema de configuración creará un sqlite para las pruebas.

Dispone de un sistema de actualización de entornos remotos basado en fabric.
Si tienes permisos en el entorno (clave ssh pública) para que se actualice es suficiente con hacer un:
**fab update**

