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


scp -r -i servidor1Key.pem aa_proyecto_ec2 ubuntu@54.78.241.159:proyecto_python/



sudo apt install python3-pip
pip install flask-cors
pip install flask
##pip install flask_socketio