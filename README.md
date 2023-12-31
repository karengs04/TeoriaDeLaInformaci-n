# IoT
Repositorio para subir tareas de IoT


Estamos trabajando en una empresa de servicio de telecomunicaciones y se ha implementado un sistema de transmisión de archivos PDF a través de una red de datos. Los clientes utilizan este sistema para enviar documentos importantes como contratos o informes a través de la red de la empresa. 

El ruido en este escenario es causado por interferencias en la red de datos. Estas interferencias pueden ser el resultado de varios factores, como la congestión de la red, la pérdida temporal de paquetes de datos o la atenuación de la señal. La interferencia en la red causa errores en la transmisión de datos, lo que provoca que algunos bits se modifiquen en el camino.
Debido a la pérdida o corrupción ocasional de datos en la red, los archivos PDF transmitidos pueden verse afectados. Estos cambios en los bits de los archivos pueden llevar a una representación incorrecta de caracteres y formatos en los documentos recibidos, lo que resulta en documentos que no son idénticos a los originales.

Problema: 
Clientes informan problemas en la transmisión de archivos PDF a través de la red de datos.

Causa:
- Interferencias en la red de datos:
  * Congestión de la red.
  * Pérdida temporal de paquetes de datos.  
  * Atenuación de la señal.

Solución Propuesta :
 - Implementar un sistema de comunicación que simule el ruido en el canal de transmisión para probar y ajustar la calidad de la transmisión de archivos.


Componentes del Esquema de Comunicación:
 - Fuente de Información: Archivos PDF.
 - Transmisor: Codificación a binario.
 - Canal: Simulación de ruido en la red.
 - Receptor: Decodificación desde binario.
 - Destino de Información: Documentos PDF. 
