#!/usr/bin/env python
import os, zipfile
from datetime import date

#os.system('export AZURE_DEVOPS_EXT_PAT=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
os.system('az artifacts universal download --only-show-errors --organization "XXXXXXXXXXXXXXXXXXX" --project "XXXXXXXXXXXXXXXXXXXX" --scope project --feed "offhire-frontend" --name "BRANCHE"  --version "*"   --path /var/www/html/xxxxxxxxxx')

dir_name = "/var/www/html/xxxxxxx"
extension = ".zip"

os.chdir(dir_name) # change directory from working dir to dir with files

for item in os.listdir(dir_name): # loop  items no diretorio
    if item.endswith(extension): # validar extensao
        file_name = os.path.abspath(item) # pegar o caminho dos arquivos
        zip_ref = zipfile.ZipFile(file_name)
        zip_ref.extractall(dir_name) # extraier os arq
        zip_ref.close() # fechar arq
        os.remove(file_name) # deletar o zip

exit(0);
