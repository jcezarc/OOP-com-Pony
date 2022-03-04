from fastapi import FastAPI
import uvicorn
from pony.orm import db_session, commit, select, sql_debug
from models import Cliente, Email, Telefone, Contato
from pydantic import BaseModel

app = FastAPI()


class DadosCliente(BaseModel):
    nome: str
    emails: str  # lista de emails separados por vírgula
    telefones: str  # lista de telefones separados por vírgula


@app.post("/cliente")
@db_session
def novo_cliente(dados: DadosCliente):
    contatos = Email.lista(dados.emails) + Telefone.lista(dados.telefones)
    if not contatos:
        return 'Dados inválidos'
    cliente = Cliente(
        nome=dados.nome,
        contatos=contatos
    )
    commit()

@app.get("/cliente/email/{email}")
@db_session
def busca_cliente_por_email(email: str):
    query = select(
        (e.cliente.nome, e.conteudo)
        for e in Email
        if email in e.conteudo
    )
    return list(query)

uvicorn.run(app)
