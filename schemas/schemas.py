from typing import List
from pydantic import BaseModel, Field
from datetime import date
from models.user import User

class UserSchema(BaseModel):
    nome: str
    genero: str
    datansc: date
    cpf: str
    celular: str
    email: str
    senha: str 

class UsersBusca(BaseModel):
    ids: str
    
class UserBusca(BaseModel):
    id: int

class UserViewSchema(BaseModel):
    id: int = Field(..., description="ID único do usuário")
    nome: str = Field(..., description="Nome do usuário")
    genero: str = Field(..., description="Genero do Usuario")
    datansc: date = Field(..., description="Data de nascimento do usuário")
    cpf: str = Field(..., description="CPF do usuário")
    celular: str = Field(..., description="Número de celular do usuário")
    email: str = Field(..., description="Email do usuário")
    senha: str = Field(..., description="Senha do usuario")

    class Config:
        from_attributes = True 


class ErrorSchema(BaseModel):
    message: str


def apresenta_user(user: User):
    """ Retorna uma representação do user seguindo o schema definido em
        UserViewSchema.
    """
    return {
        "id": user.id,
        "nome": user.nome,
        "genero": user.genero,
        "datansc": user.datansc.strftime("%Y-%m-%d"),
        "cpf": user.cpf,
        "celular": user.celular,
        "email": user.email,
        "senha": user.senha,
    }

def apresenta_users(users: List[User]):
    """ Retorna uma representação do user seguindo o schema definido em
        UserViewSchema.
    """
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "nome": user.nome,
            "genero": user.genero,
            "datansc": user.datansc.strftime("%Y-%m-%d"),
            "cpf": user.cpf,
            "celular": user.celular,
            "email": user.email,
            "senha": user.senha,
        })

    return {"Users": result}

class ListagemUsersSchema(BaseModel):
    """ Define como uma listagem de usuarios será retornada.
    """
    users:List[UserSchema]

class UserDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    deleted_user_ids: List[int]
    not_found_user_ids: List[int]
    menssage: str