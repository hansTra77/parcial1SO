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
