from subprocess import Popen, PIPE

def get_all_files():
  ls_process = Popen(["ls","/home/filesystem_user/"], stdout=PIPE, stderr=PIPE)
  file_list = Popen(["awk",'-F',' ','{print $1}'], stdin=ls_process.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
  return filter(None,file_list)

def add_file(filename,content):
  contenido = "'"+content+"'"
  nombre = "/home/filesystem_user/"+filename+".txt"
  add_process = Popen(["echo",contenido,'>',nombre], stdout=PIPE, stderr=PIPE)
  add_process.wait()
  return True if filename in get_all_files() else False

def remove_file(filename):
   remove_process = Popen(["rm",'-r',"/home/filesystem_user/*.txt"], stdout=PIPE, stderr=PIPE)
   remove_process.wait()
