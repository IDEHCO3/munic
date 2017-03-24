#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'munic.settings'
#from  munic_2015.models import *
#from datetime import datetime
#p = Pesquisa(descricao='Munic 2015',data_referencia=datetime.today())
#p.save()
#from pyexcel_ods import get_data
#data = get_data("C:\desenv\dados\Base_MUNIC_2015_ods\Base_MUNIC_2015.ods")
#sheet_recursos_humanos = data.get('Recursos_humanos')

import psycopg2

try:
    conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
except:
    print ("I am unable to connect to the database")

cursor = conn.cursor()

# inserir na tabela pesquisa_munic.administracao_quadro_pessoal
cursor.execute("select * from pesquisa_munic.administracao_quadro_pessoal")
rows = cursor.fetchall()
if not rows: #inserir administracao_quadro_pessoal caso não haja linhas
    cursor.execute("insert into pesquisa_munic.administracao_quadro_pessoal(id_administracao_quadro_pessoal, descricao) values(1, 'Direta')")
    cursor.execute("insert into pesquisa_munic.administracao_quadro_pessoal(id_administracao_quadro_pessoal, descricao) values(2, 'Indireta')")
    cursor.execute("commit")

# fim pesquisa_munic.administracao_quadro_pessoal


cursor.execute("select * from  pesquisa_munic.tipo_item_pesquisa")
rows = cursor.fetchall()
if not rows: # inserir na tabela tipo_item_pesquisa caso não haja linhas
    cursor.execute("insert into  pesquisa_munic.tipo_item_pesquisa(pesquisa_munic.id_tipo_item_pesquisa, descricao) values(1, 'Recursos Humanos')")
    cursor.execute("insert into  pesquisa_munic.tipo_item_pesquisa(pesquisa_munic.id_tipo_item_pesquisa, descricao) values(2, 'Planejamento Urbano')")
    cursor.execute("insert into  pesquisa_munic.tipo_item_pesquisa(pesquisa_munic.id_tipo_item_pesquisa, descricao) values(3, 'Recursos para Gestão')")
    cursor.execute("insert into  pesquisa_munic.tipo_item_pesquisa(pesquisa_munic.id_tipo_item_pesquisa, descricao) values(4, 'Terceirização e Informatização')")
    cursor.execute("insert into  pesquisa_munic.tipo_item_pesquisa(pesquisa_munic.id_tipo_item_pesquisa, descricao) values(5, 'Gestão ambiental')")
    cursor.execute("insert into  pesquisa_munic.tipo_item_pesquisa(pesquisa_munic.id_tipo_item_pesquisa, descricao) values(6, 'Articulação Interinstituicional')")
    cursor.execute("insert into  pesquisa_munic.tipo_item_pesquisa(id_ pesquisa_munic.tipo_item_pesquisa, descricao) values(7, 'Variáveis Externas')")
    cursor.execute("commit")
# fim tipo_item_pesquisa
#Ajustar o path(file_name_with_path)
file_name_with_path = "C:\desenv\dados\Base_MUNIC_2015_ods\Base_MUNIC_2015.ods"
#abrir o arquivo ods que possui a munic
from pyexcel_ods import get_data
data = get_data(file_name_with_path)

cursor.execute("select * from  pesquisa_munic.item_composicao_quadro_pessoal where pesquisa_munic.id_tipo_item_pesquisa=1")
rows = cursor.fetchall()
if not rows: # inserir na tabela pesquisa_munic.item_composicao_quadro_pessoal caso não haja linhas, mas antes inserir na munic.esfera_municipal
   sheet_recursos_humanos = data.get('Recursos_humanos')
   id_esfera_municipal = 1
   for row in  sheet_recursos_humanos:
       if row[0] == 'A1':
           continue
       #insert into pesquisa_munic.esfera_municipal
       #cursor.execute("SELECT nextval('pesquisa_munic.s_esfera_municipal')")
       codigo_municipio = row[2]
       geocodigo = row[0]
       url_nome_municipio = 'http://idehco4.tk/instituicoes/ibge/bcim/municipios/'+ geocodigo + '/nome'
       url_geometry = 'http://idehco4.tk/instituicoes/ibge/bcim/municipios/'+ geocodigo + '/geom'
       sql = "insert into pesquisa_munic.esfera_municipal(id_esfera_municipal, codigo_municipio, geocodigo, url_nome_municipio, url_geometry)"
       values = "values(" + id_esfera_municipal + "," + str(codigo_municipio) + "," +  str(geocodigo) + "," + str(url_nome_municipio) + ","  + url_geometry + ")"
       sql = sql + values
       cursor.execute(sql)
       cursor.execute('commit')
       # fim insert into pesquisa_munic.esfera_municipal
       id_administracao_quadro_pessoal = 1
       total_func_adm_estatutario = row[4]
       total_func_adm_clt = row[5]
       total_func_adm_somente_comissionado =row[6]
       total_func_adm_estagiario = row[7]
       total_func_adm_sem_vinculo_permanente = row[8]

       id_tipo_item_pesquisa = 1
       sql = "insert into pesquisa_munic.item_composicao_quadro_pessoal(id_administracao_quadro_pessoal, total_func_adm_estatutario, total_func_adm_clt, total_func_adm_somente_comissionado, total_func_adm_estagiario, total_func_adm_sem_vinculo_permanente,id_tipo_item_pesquisa, id_esfera_municipal)"
       values = "values(" + str(id_administracao_quadro_pessoal) + "," +\
                str(total_func_adm_estatutario) + ", " + \
                str(total_func_adm_clt) + "," + \
                str(total_func_adm_somente_comissionado) + "," + \
                str(total_func_adm_estagiario) + "," + \
                str(total_func_adm_sem_vinculo_permanente) + "," + \
                id_tipo_item_pesquisa +\
                id_esfera_municipal +\
                ")"
       sql = sql + values
       cursor.execute(sql)
       cursor.execute('commit')
       #tem administração indireta
       if row[10] == 'Sim':
           total_func_adm_estatutario = row[9]
           total_func_adm_clt = row[10]
           total_func_adm_somente_comissionado =row[11]
           total_func_adm_estagiario = row[12]
           total_func_adm_sem_vinculo_permanente = row[13]
           id_administracao_quadro_pessoal = 2
           id_tipo_item_pesquisa = 1
           sql = "insert into pesquisa_munic.item_composicao_quadro_pessoal(id_administracao_quadro_pessoal, total_func_adm_estatutario, total_func_adm_clt, total_func_adm_somente_comissionado, total_func_adm_estagiario, total_func_adm_sem_vinculo_permanente, id_tipo_item_pesquisa, id_esfera_municipal)"
           values = "values(" + str(id_administracao_quadro_pessoal) + "," +\
                str(total_func_adm_estatutario) + ", " + \
                str(total_func_adm_clt) + "," + \
                str(total_func_adm_somente_comissionado) + "," + \
                str(total_func_adm_estagiario) + "," + \
                str(total_func_adm_sem_vinculo_permanente) + "," + \
                id_tipo_item_pesquisa +\
                id_esfera_municipal +\
                ")"
           sql = sql + values
           cursor.execute(sql)
           cursor.execute('commit')

       id_esfera_municipal = id_esfera_municipal + 1
# Fim Inserir Recursos Humanos




