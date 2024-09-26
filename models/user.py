from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from . import engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'usuarios' # Nome da tabela
   
    # Dados da tabela
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40), nullable=False)
    genero = Column(String(1), nullable=False)
    datansc = Column(Date, nullable=False)
    cpf = Column(String(11), nullable=False)
    celular = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False)
    senha = Column(String(40), nullable=False)


    def __init__(self, nome:str, genero: str, datansc:Date, cpf:str, celular:str, email:str, senha:str):
        """
            Cria um novo usuário com os dados fornecidos.

            Arguments:
                nome: O nome completo do usuário.
                genero: O gênero do usuário.
                datansc: A data de nascimento do usuário.
                cpf: O CPF do usuário.
                celular: O número de celular do usuário.
                email: O endereço de email do usuário.
                senha: A senha do usuário.
        """
        self.nome = nome
        self.datansc = datansc  
        self.cpf = cpf
        self.celular = celular
        self.email = email
        self.senha = senha
        self.genero = genero

Base.metadata.create_all(engine)