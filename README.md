### Parcial 1
Universidad ICESI  
Curso: Sistemas Operativos  
Estudiante: Juan Pablo Medina Mora 
Código: 11112010

Link: https://github.com/hansTra77/parcial1SO/

### Creación del usuario filesystem_user, instalación de flask y creación del ambiente virtual

Con el fin de desarrollar el parcial el primer paso consistió en la creación de un nuevo usuario, para tal fin se siguió el siguiente procedimiento

```
# adduser filesystem_user
# passwd password
```

Con el nuevo usuario creado se procedió a crear el ambiente virtual que el usuario utilizaría

```
# su filesystem_user
$ cd ~/
$ mkdir envs
$ cd envs
$ virtualenv flask_env
```

Se activó el ambiente virtual creado

```
$ cd ~/envs
$ . flask_env/bin/activate
```

Después se procedió a instalar Flask en el nuevo ambiente virtual

```
$ pip install Flask
```

Con lo anterior se terminó con el proceso necesario previo al desarrollo del parcial

### Creación de los archivos files.py y file_commands.py

El enunciado del examen presentaba la siguiente información, que debía servir de guía para la implementación de los scripts que levantarían los servicios web.

Descripción de las URIs

|   |POST   |GET   |PUT   |DELETE   |
|---|---|---|---|---|
| /files  | Crear archivo  | Obtener listado de archivos  | No aplica | Elimina todos los archivos  |
| /files/recently_created  | No aplica  | Retorna los archivos que se crearon recientemente  | No aplica | No aplica  |

Descripción de los formatos de envío de las solicitudes

|   |POST   |GET   |PUT   |DELETE   |
|---|---|---|---|---|
| /files  | JSON  | No aplica  | No aplica  | No aplica  |
| /files/recently_created  | No aplica  | No aplica  | No aplica  | No aplica  |

Descripción de los formatos de respuesta de las solicitudes

|   |POST   |GET   |PUT   |DELETE   |
|---|---|---|---|---|
| /files  | HTTP 201 CREATED | JSON | HTTP 404 NOT FOUND | HTTP 200 OK |
| /files/recently_created  | HTTP 404 NOT FOUND | JSON  | HTTP 404 NOT FOUND | HTTP 404 NOT FOUND |

Descripción del formato de intercambio de datos (JSON)  

```json
{
  "filename": "carta",
  "content": "this is the file content"
}
```

```json
{
  "files": [
    "carta",
    "listado",
    "tareas",
    "recordatorio"
  ]
}
```

Se creó el archivo files.py

```python
from flask import Flask, abort, request
import json

from file_commands import get_all_files, add_file, remove_file

app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/files',methods=['POST'])
def create_file():
  content = request.get_json(silent=True)
  filename = content['filename']
  contenido = content['content']
  if not filename:
    return "El archivo no tiene nombre", 400
  if filename in get_all_files():
    return "El archivo ya existe", 400
  if add_file(filename,contenido):
    return "Archivo creado", 201
  else:
    return "Error al crear el archivo", 400

@app.route(api_url+'/files',methods=['GET'])
def list_files():
  list = {}
  list["files"] = get_all_files()
  return json.dumps(list), 200

@app.route(api_url+'/files',methods=['DELETE'])
def delete_files():
  remove_file()
  return 'Todos los archivos se han eliminado correctamente', 200

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=9090,debug='True')
```

Se creó el archivo file_commands.py

```python
from subprocess import Popen, PIPE

def get_all_files():
  ls_process = Popen(["ls","/home/filesystem_user/"], stdout=PIPE, stderr=PIPE)
  file_list = Popen(["awk",'-F',' ','{print $1}'], stdin=ls_process.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
  return filter(None,file_list)

def add_file(filename,content):
  contenido = "'"+content+"'"
  nombre = "/home/filesystem_user/"+filename+".txt"
  add_process = Popen(["touch",nombre], stdout=PIPE, stderr=PIPE)
  add_process.wait()
  with open(filename,"W") as fo:
    fo.Write(content)
  return True if filename in get_all_files() else False

def remove_file(filename):
   remove_process = Popen(["rm",'-r',"/home/filesystem_user/*.txt"], stdout=PIPE, stderr=PIPE)
   remove_process.wait()
```
Y se crearon los archivos file_res_commands.py y files_recently.py

```python
from subprocess import Popen, PIPE

def get_recent_files():
  ls_process = Popen(["ls","/home/filesystem_user/"], stdout=PIPE, stderr=PIPE)
  file_list = Popen(["head",'-5'], stdin=ls_process.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
  return filter(None,file_list)
```

```python
from flask import Flask, abort, request
import json

from file_res_commands import get_recent_files

app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/files/recently_created',methods=['GET'])
def recent_created():
  list = {}
  list["recently created"] = get_recent_files()
  return json.dumps(list), 200
  
if __name__ == "__main__":
  app.run(host='0.0.0.0',port=9191,debug='True')
```

Con los archivos creados se procedió a habilitar el puerto 9090 y el 9191en el archivo iptables.

```
# cat /etc/sysconfig/iptables
# service iptables restart
```

#### Prueba del servicio para la URI /files

Primero se levanta el servicio

```
$ (flask_env) python files.py
```
Con el servicio subido se procedió a utilizar la extensión Postman para verificar los resultados del servicio.

A continuación se muestran las pruebas al servicio web empleando la extensión postman.

Prueba de la URI con GET

![][1]

Prueba de la URI con POST

![][2]

Prueba de la URI con DELETE

![][3]

#### Prueba del servicio para la URI /files/recently_created

Primero se levanta el servicio

```
$ (flask_env) python files_recently.py
```
Prueba de la URI con GET

![][4]

Con esto realizado se procedió a desactivar el ambiente.

```
$ deactivate
```
Con lo anterior se dio por finalizado el parcial.

[1]: images/get1.JPG
[2]: images/post.JPG
[3]: images/delete.JPG
[4]: images/get2.JPG
