from django.contrib.gis.db import models

from django.contrib.gis.db import models


class AdministracaoQuadroPessoal(models.Model):
    id_administracao_quadro_pessoal = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'administracao_quadro_pessoal'


class EsferaMunicipal(models.Model):
    id_esfera_municipal = models.AutoField(primary_key=True)
    codigo_municipio = models.CharField(max_length=20, blank=True, null=True)
    url_nome_municipio = models.CharField(max_length=200, blank=True, null=True)
    geocodigo = models.CharField(max_length=20, blank=True, null=True)
    url_geometry = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'esfera_municipal'


class ItemComposicaoQuadroPessoal(models.Model):
    id_tem_composicao_quadro_pessoal = models.AutoField(primary_key=True)
    administracao_quadro_pessoal = models.ForeignKey(AdministracaoQuadroPessoal, db_column='id_administracao_quadro_pessoal', blank=True, null=True)
    total_func_adm_estatutario = models.IntegerField(blank=True, null=True)
    total_func_adm_clt = models.IntegerField(blank=True, null=True)
    total_func_adm_somente_comissionado = models.IntegerField(blank=True, null=True)
    total_func_adm_estagiario = models.IntegerField(blank=True, null=True)
    total_func_adm_sem_vinculo_permanente = models.IntegerField(blank=True, null=True)
    tipo_item_pesquisa = models.ForeignKey('TipoItemPesquisa', db_column='id_tipo_item_pesquisa', blank=True, null=True)
    esfera_municipal = models.ForeignKey('EsferaMunicipal', db_column='id_esfera_municipal', blank=True, null=True)
    pesquisa = models.ForeignKey('Pesquisa', db_column='id_pesquisa', blank=True, null=True)

    class Meta:
        db_table = 'item_composicao_quadro_pessoal'


class Pesquisa(models.Model):
    id_pesquisa = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=200)
    data_referencia = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'pesquisa'


class TipoItemPesquisa(models.Model):
    id_tipo_item_pesquisa = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'tipo_item_pesquisa'


class TipoPesquisa(models.Model):
    id_tipo_pesquisa = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tipo_pesquisa'



class TipoInstrumentoLegal(models.Model):
    descricao = models.CharField(max_length=100, blank=True, null=True)
    id_tipo_instrumento_legal = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'tipo_instrumento_legal'

class PlanoDiretor(models.Model):
    id_plano_diretor = models.AutoField(primary_key=True)
    ano_lei_criacao = models.IntegerField(blank=True, null=True)
    ano_ultima_atualizacao = models.IntegerField(blank=True, null=True)
    esta_em_elaboracao = models.NullBooleanField()
    esfera_municipal = models.ForeignKey('EsferaMunicipal', db_column='id_esfera_municipal', blank=True, null=True)

    class Meta:
        db_table = 'plano_diretor'

class CaracterizacaoPlanejamentoUrbano(models.Model):
    id_caracterizacao_planejamento_urbano = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'caracterizacao_planejamento_urbano'

class ItemPlanejamentoUrbano(models.Model):
    id_item_planejamento_urbano = models.AutoField(primary_key=True)
    escolaridade_gestor = models.CharField(max_length=50, blank=True, null=True)
    caracterizacao_planejamento_urbano = models.ForeignKey(CaracterizacaoPlanejamentoUrbano, db_column='id_caracterizacao_planejamento_urbano', blank=True, null=True)
    esfera_municipal = models.ForeignKey('EsferaMunicipal', db_column='id_esfera_municipal', blank=True, null=True)

    class Meta:
        db_table = 'item_planejamento_urbano'
