# SCILab

Sistema de Control de Ingreso a FabLab USM San Joaquín

### Inicializar sistema

Dirigirse a carpeta de proyecto:  
`cd ~/SCILab`  
Ejecutar comando:  
`python3 main.py`  

### Configuración SSH

Para ejecutar comandos y acceder a los archivos del Raspberry Pi, se recomienda realizarlo mediante [SSH](https://es.wikipedia.org/wiki/Secure_Shell), desde un terminal en cualquier sistema operativo (Windows, Linux, Mac, etc).  

Ejecutar comando desde otro equipo conectado a la misma red:  
`ssh fl_rpi2@[direccion IP]`  
E ingresar contraseña de usuario.  

Para esto también es necesario instalar [ZeroTier](https://www.zerotier.com/download/) en el dispositivo desde el cual se intenta acceder al RPi, y agregarlo a una red junto con el Raspberry Pi, con tal de contar con una IP estática a la que poder acceder de manera segura. 

### Configuración inicial

En caso de cambiar de RPi o formateo, conectarlo a una pantalla y teclado.  

Luego, instalar y añadir Raspberry Pi a una red en ZeroTier siguiendo [este tutorial](https://pimylifeup.com/raspberry-pi-zerotier/). De esta forma se podrá acceder a él mediante los pasos de la sección anterior, sin necesidad de una pantalla externa o teclado.  

Clonar repositorio de Github:  
`git clone https://github.com/josemqz/SCILab.git` (o el URL correspondiente, en caso de realizar un _fork_ del repositorio).  

Instalar pip en caso de ser necesario:  
```
sudo apt update  
sudo apt install python3-pip  
```  

Instalar dependencias:  
```
cd ~/SCILab  
pip3 install -R requirements.txt
```

### Subir código a repositorio Github
En caso de realizar modificaciones al código, se recomienda utilizar SSH para subirlo a Github (Ver [Agregar una nueva llave ssh a tu cuenta de Github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) y [Generar una nueva llave ssh y agregarla al agente ssh](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)).  
Ya sea a la rama _main_ o a un _fork_.

### Specs

Raspberry Pi 3B+ Rev 1.5  
RPi OS Lite 11 (bullseye) 32-bit

### Desarrollado por y para FabLab

Josué Venegas (Idea y gestión)  
José Quezada (Software e instalación electrónica)  
Javier González (Diseño 3D de protectores)  
Octavio Jaques (Instalación y apoyo en electrónica)  
Mateo Morales (Apoyo en electrónica)  
José Southerland (Apoyo en almacenamiento de datos en csv)  
