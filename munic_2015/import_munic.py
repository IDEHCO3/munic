# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'munic.settings'

from  munic_2015.models import AdministracaoQuadroPessoal, TipoItemPesquisa, Pesquisa, TipoPesquisa, ItemComposicaoQuadroPessoal, EsferaMunicipal, CaracterizacaoPlanejamentoUrbano, ItemPlanejamentoUrbano, TipoInstrumentoLegal, \
    PlanoDiretor
from datetime import datetime
from pyexcel_ods3 import get_data
from pyexcel_ods3.ods import *

#Common to all sheets
def get_sheet(file_name_with_path, sheet_name):
    #Ajustar o path(file_name_with_path) para o seu caso
    #abrir o arquivo ods que possui a munic
    data = get_data(file_name_with_path)
    return data.get(sheet_name)

# init Migrate Recursos Humanos
def populate_pesquisa_if_need():
    Pesquisa.objects.get_or_create(descricao='Munic 2015')

def populate_AdministracaoQuadroPessoal_if_need():
    array_aqp = AdministracaoQuadroPessoal.objects.all()
    if not array_aqp:
        aqp =  AdministracaoQuadroPessoal(pk=1, descricao='Direta')
        aqp.save()
        aqp =  AdministracaoQuadroPessoal(pk=2, descricao='Indireta')
        aqp.save()

def populate_TipoItemPesquisa_if_need():
    array_tip =  TipoItemPesquisa.objects.all()
    if not array_tip:
        tip = TipoItemPesquisa(pk=1, descricao='Recursos Humanos')
        tip.save()
        tip = TipoItemPesquisa(pk=2, descricao='Planejamento Urbano')
        tip.save()
        tip = TipoItemPesquisa(pk=3, descricao='Recursos para Gestão')
        tip.save()
        tip = TipoItemPesquisa(pk=4, descricao='Terceirização e Informatização')
        tip.save()
        tip = TipoItemPesquisa(pk=5, descricao='Gestão ambiental')
        tip.save()
        tip = TipoItemPesquisa(pk=6, descricao='Articulação Interinstitucional')
        tip.save()
        tip = TipoItemPesquisa(pk=7, descricao='Variáveis Externas')
        tip.save()

#aponta para aba Recursos humanos da planilha

def save_sheet_recursos_humanos(sheet_recursos_humanos):
    #objetos relacionados como objetos EsferaMunicipal ItemComposicaoQuadroPessoal
    tip_rh = TipoItemPesquisa.objects.get(descricao='Recursos Humanos')
    aqp_d =  AdministracaoQuadroPessoal.objects.get(descricao='Direta')
    aqp_i =  AdministracaoQuadroPessoal.objects.get(descricao='Indireta')
    pes_munic = Pesquisa.objects.get(descricao='Munic 2015')

    for row in  sheet_recursos_humanos:
        if row[0] == 'A1': #ignora o cabeçalho
           continue
        #Cria objeto EsferaMunicipal
        codigo_municipio = str(row[2])
        geo_codigo = str(row[0])
        url_nome_municipio = 'http://idehco4.tk/instituicoes/ibge/bcim/municipios/'+ geo_codigo + '/nome'
        url_geometry = 'http://idehco4.tk/instituicoes/ibge/bcim/municipios/'+ geo_codigo + '/geom'
        em = EsferaMunicipal(codigo_municipio=codigo_municipio, geocodigo=geo_codigo,url_nome_municipio=url_nome_municipio, url_geometry=url_geometry)
        em.save()
        #Cria objeto ItemComposicaoQuadroPessoal
        icqp = ItemComposicaoQuadroPessoal(total_func_adm_estatutario=int(row[4]), total_func_adm_clt=int(row[5]), total_func_adm_somente_comissionado=int(row[6]),total_func_adm_estagiario=int(row[7]),total_func_adm_sem_vinculo_permanente=int(row[8]))
        icqp.esfera_municipal=em
        icqp.administracao_quadro_pessoal=aqp_d
        icqp.tipo_item_pesquisa=tip_rh
        icqp.pesquisa=pes_munic
        icqp.save()

        #tem administração indireta
        if row[10] == 'Sim':
            icqp = ItemComposicaoQuadroPessoal(total_func_adm_estatutario=int(row[12]), total_func_adm_clt=int(row[13]), total_func_adm_somente_comissionado=int(row[14]),total_func_adm_estagiario=int(row[15]),total_func_adm_sem_vinculo_permanente=int(row[16]))
            icqp.esfera_municipal=em
            icqp.administracao_quadro_pessoal=aqp_i
            icqp.tipo_item_pesquisa=tip_rh
            icqp.pesquisa=pes_munic
            icqp.save()


def execute_migration_recursos_humanos(file_name_with_path ="/home/aluizio/munic/Base_MUNIC_2015.ods", sheet_name="Recursos_humanos"):
    populate_pesquisa_if_need()
    populate_TipoItemPesquisa_if_need()
    populate_AdministracaoQuadroPessoal_if_need()
    sheet_recursos_humanos = get_sheet(file_name_with_path, sheet_name)
    save_sheet_recursos_humanos(sheet_recursos_humanos)
    # init Migrate Recursos Humanos
# End Migrate Recursos Humanos

# init Migrate Planejamento Urbano
def populate_tipo_instrumento_legal_if_need(): #domínio
    array_tip =  TipoInstrumentoLegal.objects.all()
    if not array_tip:
        arr = [ 'Legislação sobre área e/ou zona especial de interesse social- existência',
                'Legislação sobre zona e/ou área de especial interesse - existência',
                'Lei de perímetro urbano - existência',
                'Legislação sobre parcelamento do solo - existência',
                'Legislação sobre zoneamento ou uso e ocupação do solo - existência',
                'Legislação sobre solo criado ou outorga onerosa do direito de construir - existência',
                'Legislação sobre contribuição de melhoria - existência',
                'Legislação sobre operação urbana consorciada - existência',
                'Legislação sobre estudo de impacto de vizinhança - existência',
                'Código de obras - existência',
                'Legislação sobre zoneamento ambiental ou zoneamento ecológico-econômico',
                'Legislação sobre servidão administrativa',
                'Legislação sobre tombamento',
                'Legislação sobre unidade de conservação',
                'Legislação sobre concessão de uso especial para fins de moradia',
                'Legislação sobre usucapião especial de imóvel urbano',
                'Legislação sobre direito de superfície',
                'Legislação sobre regularização fundiária',
                'Legislação sobre a legitimação de posse',
                'Legislação sobre estudo prévio de impacto ambiental']
        for desc in arr:
          tip = TipoInstrumentoLegal(descricao=desc)
          tip.save() #



def create_plano_diretor(ano_lei_criacao, ano_ultima_atualizacao, esta_em_elaboracao, esfera_municipal):

    try:
        ano_criacao = int(ano_lei_criacao)
    except ValueError:
        ano_criacao = None
    try:
        ano_atualizacao = int(ano_ultima_atualizacao)
    except ValueError:
        ano_atualizacao = None

    try:
        if esta_em_elaboracao == 'Sim':
            em_elaboracao = True
        elif esta_em_elaboracao == 'Não':
            em_elaboracao = False
        else:
            em_elaboracao = None
    except ValueError:
        em_elaboracao = None

    pla_diretor = PlanoDiretor(ano_criacao, ano_ultima_atualizacao= ano_atualizacao, esta_em_elaboracao= em_elaboracao )
    pla_diretor.esfera_municipal = esfera_municipal
    pla_diretor.save()

def save_sheet_planejamento_urbano(sheet_planejamento_urbano):
    for row in  sheet_planejamento_urbano:
        carac_planej_urb = CaracterizacaoPlanejamentoUrbano.objects.get_or_create(descricao=row[4])
        esfera_municipal = EsferaMunicipal.objects.get(geocodigo=row[0])
        create_plano_diretor(row[7], row[8], row[9], esfera_municipal)
        item_planej_urb.esfera_municipal = esfera_municipal
        item_planej_urb = ItemPlanejamentoUrbano(escolaridade_gestor=row[5])
        item_planej_urb.caracterizacao_planejamento_urbano= carac_planej_urb
        instrum_legal = InstrumentoLegal

def execute_migration_planejamento_urbano(file_name_with_path ="C:\desenv\dados\Base_MUNIC_2015_ods\Base_MUNIC_2015.ods", sheet_name="Planejamento_urbano"):
    populate_pesquisa_if_need()
    populate_AdministracaoQuadroPessoal_if_need()
    sheet_planejamento_urbano = get_sheet(file_name_with_path, sheet_name)
    save_sheet_planejamento_urbano(sheet_planejamento_urbano)
# end Migrate Planejamento Urbano
