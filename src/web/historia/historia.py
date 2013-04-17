from base64 import urlsafe_b64decode

__author__ = 'lucas.shen'

from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from core.tirinha.model import Usuario
from zen import router

def form(write_tmpl):
    values={"save_url":router.to_path(salvar)}
    write_tmpl("/historia/templates/")

def salvar(handler, titulo_tirinha, img_tirinha, legenda, avalicao, id=None):
    #SE O ID NÃO EXISTIR ELE CRIA UM NOVO ID E REGISTRO
    if id:
        tirinha = Usuario(id=long(id), titulo_tirinha=titulo_tirinha, img_tirinha=img_tirinha, legenda=legenda, avalicao=long(avalicao))
    #SE ELE POSSUIR UM ID, ELE REALIZA UM UPDATE DO RESGISTRO
    else:
        tirinha = Usuario(titulo_tirinha=titulo_tirinha, img_tirinha=img_tirinha, legenda=legenda, avalicao=long(avalicao))
    #SALVA AS ALTERAÇÕES
    tirinha.put();
    #REDIRECIONA PARA O LISTAR
    handler.redirect(router.to_path(listar))

def listar(write_tmpl):
    #REALIZA A CONSULTA PELOS ID MAIORES QUE 0 E ORDENA POR ID
    query = Usuario.query(Usuario.get_by_id>0).order(Usuario.get_by_id)
    #TRAZ SOMENTE 10 LINHAS DA CONSULTA
    tirinha =  query.fetch(10)
    #VALORES QUE SERÃO PASSADOS NA URL
    values = {"tirinha":tirinha,
              "apagar_url":router.to_path(apagar),
              "editar_url":router.to_path(editar)}
    #MONTA A PAGINA
    write_tmpl()

def apagar(handler, id):
    #RECEBE O OBJETO MAIS O ID DELE
    key = ndb.Key(Usuario,long(id))
    #DELETA O REGISTRO
    key.delete()
    #REDIRECIONA PARA A PAGINA LISTAR
    handler.redirect(router.to_path(listar))

def editar(write_tmpl,urlsafe):
    #
    key =  ndb.Key(urlsafe=urlsafe)
    #PEGA A CHAVE PRIMARIA E ARMAZENA NA HISTORIA
    tirinha = key.get()
    #CARREGA O VALORES DA PK E MANDA PARA O SALVAR
    values = {"save_url":router.to_path(salvar),
              "tirinha":tirinha}
    write_tmpl()