# EOII_2425_T1
*Trabajo evaluable de las prácticas 1 a 4*

## Módulos de Python desarrollados

### ```styles.py```
En este fichero se definen los colores y las fuentes que se utilizarán para los elementos generados con el módulo ```tkinter```.

### ```udp_client_class.py```
Implementación de la clase cliente UDP para usar con la ventana del cliente UDP.

### ```udp_client_window.py```
Implementación de la ventana del cliente UDP con ```tkinter```. A través de esta ventana el usuari@ puede enviar mensajes a una dirección de servidor determinada por una IP y un puerto. Esta aplicación proporciona protección de errores, como datos incorrectos, un uso en orden diferente al que se ha establecido o un cierre abrupto de la aplicación. Se realiza un cierre de las ventanas y una finalización correcta de los hilos existentes.

### ```udp_server_class.py```
Implementación de la clase servidor UDP para usar con la ventana del servidor UDP.

### ```udp_server_window.py```
Implementación de la ventana del servidor UDP con ```tkinter```. A través de esta ventana el usuari@ puede establecer en que puerto local se recibirán los mensajes del cliente UDP. Esta aplicación proporciona protección de errores, como datos incorrectos o un cierre abrupto de la aplicación. Se realiza un cierre de las ventanas y una finalización correcta de los hilos existentes.

## Ejecución de las aplicaciones

Para poner en funcionamiento las aplicaciones, tienen que estar en ejecución los módulos ```udp_client_window.py``` y ```udp_server_window.py```.

Estando dentro de la carpeta del proyecto, abrir una terminal y ejecutar los siguientes comandos para que se inicien las aplicaciones en segundo plano (funciona en linux):

```bash
python3 udp_client_window.py &
python3 udp_server_window.py &
```