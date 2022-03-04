from pony.orm import Database, PrimaryKey, Required, Set, Optional


db = Database()
db.bind(provider='sqlite', filename='agenda.db', create_db=True)


class Cliente(db.Entity):
    id = PrimaryKey(int, auto=True)
    nome = Required(str)
    contatos = Set('Contato')


class Contato(db.Entity):
    id = PrimaryKey(int, auto=True)
    cliente = Optional('Cliente')
    conteudo = Required(str)
    @classmethod
    def lista(cls, expr: str):
        return [
            cls(conteudo=item) for item in expr.split(',')
            if cls.valida(item)
        ]


class Email(Contato):
    @classmethod
    def valida(cls, email: str):
        return '@' in email


class Telefone(Contato):
    @classmethod
    def valida(cls, telefone: str):
        return all(c.isdigit() or c in '()- ' for c in telefone)


db.generate_mapping(create_tables=True)
