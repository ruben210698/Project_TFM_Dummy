> Lanzar EC2 con Ubuntu
> grupo de seguridad: launch-wizard-2




scp -r -i servidor1Key.pem aa_proyecto_ec2 ubuntu@3.249.253.113:proyecto_python/



sudo apt update

sudo apt install python3-pip

-- Poner python como python3:
nano ~/.bashrc
Añadir abajo::    alias python='python3'
source ~/.bashrc


pip install flask; pip install flask_socketio; pip install spacy; pip install unidecode; pip install matplotlib; pip install networkx


sudo -i
pip3 install spacy
python -m spacy download es_dep_news_trf
python -m spacy download es_core_news_lg
python -m spacy download es_core_news_md
python -m spacy download es_core_news_sm

-----
Comprobar: >python3
import spacy
nlp = spacy.load("es_dep_news_trf")





export PYTHONPATH=/home/ubuntu/proyecto_python/aa_proyecto_ec2




sudo apt update
sudo apt install apache2
sudo scp -r /home/ubuntu/proyecto_python/aa_proyecto_ec2/npl_module/web_project/. /var/www/html/

cd /var/www/html/




















sudo apt install nginx

Configura NGINX para que actúe como proxy inverso y redirija las solicitudes a tu aplicación Python. Puedes editar el archivo de configuración de NGINX en /etc/nginx/sites-available/default y agregar la configuración necesaria. Por ejemplo:
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:puerto-de-tu-aplicacion-python;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}


scp -r -i servidor1Key.pem aa_proyecto_ec2 ubuntu@54.246.255.244:proyecto_python/




sudo apt install python3-pip

-- Poner python como python3:
nano ~/.bashrc
Añadir abajo::    alias python='python3'
source ~/.bashrc



pip install flask-cors
pip install flask
##pip install flask_socketio
pip install spacy
pip install unidecode
pip install matplotlib
pip install networkx

python -m spacy download es_dep_news_trf
python -m spacy download es_core_news_lg
python -m spacy download es_core_news_md
python -m spacy download es_core_news_sm
export PYTHONPATH=/home/ubuntu/proyecto_python/aa_proyecto_ec2


sudo apt update
sudo apt install apache2
sudo scp -r /home/ubuntu/proyecto_python/aa_proyecto_ec2/npl_module/web_project/. /var/www/html/

cd /var/www/html/


http://54.246.255.244/

¿Error?
sudo lsof -i :80
sudo service nginx stop
sudo service apache2 start
sudo service apache2 status

Acuerdate que la url de python en ec2 será http://127.0.0.1:5000



------------------------
Verifica la configuración del firewall: Asegúrate de que el puerto 5000 esté abierto en el firewall de tu instancia EC2. Puedes revisar la configuración de los grupos de seguridad en la consola de AWS y asegurarte de que se permita el tráfico en el puerto 5000 tanto para conexiones entrantes como salientes.
Selecciona el grupo de seguridad asociado a tu instancia EC2: En la lista de grupos de seguridad, encuentra y selecciona el grupo de seguridad asociado a tu instancia EC2 en la columna "Nombre del grupo de seguridad".

Verifica las reglas de entrada: En la pestaña "Reglas de entrada", verifica si ya existe una regla que permita el tráfico en el puerto 5000. Si ya existe una regla que permite el tráfico en el puerto 5000, puedes pasar al siguiente paso. De lo contrario, sigue los siguientes pasos para agregar una nueva regla.

Agrega una regla de entrada para el puerto 5000: Haz clic en el botón "Editar reglas de entrada" o "Agregar regla de entrada". Luego, agrega una nueva regla con la siguiente configuración:

Tipo: Personalizado TCP
Puerto de rango: 5000
Fuente: "0.0.0.0/0" (para permitir todas las direcciones IP) o una dirección IP específica desde la que deseas permitir el acceso.
Verifica las reglas de salida: En la pestaña "Reglas de salida", verifica si ya existe una regla que permita el tráfico saliente desde el puerto 5000. Si ya existe una regla que permite el tráfico saliente desde el puerto 5000, puedes pasar al siguiente paso. De lo contrario, sigue los siguientes pasos para agregar una nueva regla.

Agrega una regla de salida para el puerto 5000: Haz clic en el botón "Editar reglas de salida" o "Agregar regla de salida". Luego, agrega una nueva regla con la siguiente configuración:

Tipo: Personalizado TCP
Puerto de rango: 5000
Destino: "0.0.0.0/0" (para permitir todas las direcciones IP) o una dirección IP específica a la que deseas permitir el acceso.