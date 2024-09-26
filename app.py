from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify, request
from flask_cors import CORS
from datetime import date, datetime

from sqlalchemy.exc import IntegrityError

from models.user import User
from models import Session
from schemas.schemas import *

info = Info(title="User API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
user_tag = Tag(name="User", description="Adição, visualização, edição e remoção de usuários")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/user', tags=[user_tag],
        responses={"200": UserSchema, "409": ErrorSchema, "400": ErrorSchema})
#ADICIONAR USUARIO
def add_user(form: UserSchema):
    
    """Adiciona um novo Usuario à base de dados.
    
    Retorna uma representação dos dados do usuario novo.
    """
    session = Session()

    # Criando um objeto com os novos dados
    new_user = User(
        nome=form.nome,
        genero=form.genero,
        datansc=form.datansc,
        cpf=form.cpf,
        celular=form.celular,
        email=form.email,
        senha=form.senha
    )

    try:
        # Adiciona o novo usuário à sessão
        session.add(new_user)

        # Confirma a sessão para salvar as alterações no banco de dados
        session.commit()

        # Retorna uma mensagem de sucesso
        return {"message": "Usuario adicionado com sucesso!"}, 200
    
    except IntegrityError:
        # Se ocorrer um erro de integridade ex:o nome de usuário já existe, 
        # faz rollback da sessão e retorna uma mensagem de erro
        session.rollback()
        return {"message": "Ja existe um usuario com esse nome."}, 409

    except Exception as e:
        # Se ocorrer qualquer outro erro, faz rollback da sessão e retorna uma mensagem de erro
        session.rollback()
        return {"message": str(e)}, 400

    finally:
        # Fecha a sessão
        session.close()

#VER O USER POR ID
@app.get('/user/', tags=[user_tag],
        responses={"200": UserViewSchema, "404": ErrorSchema})
def get_user(query: UserBusca):
    """Busca um usuario, pelo id, que estiver no banco de dados.
    
    Retorna uma representação dos dados do id escolhido.
    """

    user_id = query.id
    
    try:   
        session = Session()
        
        # Consulta o usuário pelo ID
        user = session.query(User).filter(User.id == user_id).first()

        if user:
            # Se o usuário for encontrado, retorna os dados do usuário
            user_dict = apresenta_user(user)
            return jsonify(user_dict), 200 # transformando o dado para json
        else:
            # Se o usuário não for encontrado, retorna uma mensagem de erro
            return {"message": "Usuário não encontrado."}, 404
    except Exception as e:
        # Se ocorrer um erro, retorna uma mensagem de erro
        return {"message": "Usuário não encontrado."}, 400
    finally:
        # Fecha a sessão
        session.close()

#VER TODOS USUARIOS
@app.get('/users', tags=[user_tag],
        responses={"200": ListagemUsersSchema, "404": ErrorSchema})
def get_users():
    """Faz a busca por todos os Usuarios cadastrados

    Retorna uma representação da listagem de users.
    """

    session = Session()
    
    # fazendo a busca de todos os dados
    users = session.query(User).all()

    if not users:
        # se não há users cadastrados
        return {"users": []}, 200
    else:
        # retorna a a representação dos dados dos usuarios com o id
        #print(users)
        users_dict = apresenta_users(users)
        return jsonify(users_dict), 200

#EDITAR
@app.put('/user', tags=[user_tag],
        responses={"200": UserViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_user():
    """Faz a alteração dos dados do Usuario, pelo o id.

    Retorna uma representação dos novos dados.
    """
    form = request.form

    try:

        # Obtém o ID do usuário a ser atualizado
        user_id = int(form["id"])

        # Obtém os dados para atualização
        nome = form["nome"]
        genero = form["genero"]
        datansc = datetime.strptime(form["datansc"], "%Y-%m-%d").date()
        cpf = form["cpf"]
        celular = form["celular"]
        email = form["email"]
        senha = form["senha"]

        # Obtém o usuário pelo ID
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()
        
        if user:
            # Atualiza os campos do usuário com os novos valores
            user.nome = nome
            user.genero = genero
            user.datansc = datansc
            user.cpf = cpf
            user.celular = celular
            user.email = email
            user.senha = senha


            # Confirma a sessão para salvar as alterações no banco de dados
            session.commit()
            
            # Retorna os dados atualizados do usuário
            user_dict = apresenta_user(user)
            return jsonify(user_dict), 201
        else:
            # Se o usuário não for encontrado, retorna uma mensagem de erro
            return {"message": "Usuário não encontrado."}, 404
    except Exception as e:
        # Se ocorrer um erro, retorna uma mensagem do erro
        return {"message": str(e)}, 400
    finally:
        session.close()

#DELETAR
@app.delete('/users', tags=[user_tag],
            responses={"200": UserDelSchema, "404": ErrorSchema})
def del_produto(query: UsersBusca):
    """Deleta um usuario a partir do(s) id(s) informado(s).

    Retorna uma mensagem de confirmação da remoção.
    """

    # Recebendo uma string e transformando os dados em uma lista ao separarar-los por uma ",".
    user_ids = query.ids
    user_ids = [int(id_str) for id_str in user_ids.split(',')]

    deleted_users = []
    not_found_users = []

    try:
        # criando conexão com a base
        session = Session()

        # Com base a lista de ids, ele vai pegar cada linha e deletar do banco.
        for user_id in user_ids:
            user = session.query(User).filter(User.id == user_id).first()

            if user:
                deleted_users.append(user)
                session.delete(user)
            else:
                not_found_users.append(user_id)
        
        # Confirmar a sessão para salvar as alterações no banco de dados
        session.commit()
        
        if deleted_users:
            # Atualizar os IDs dos usuários restantes para seguir uma ordem sequencial
            users = session.query(User).order_by(User.id).all()
            for index, user in enumerate(users, start=1):
                user.id = index

            # Confirmar a sessão para salvar as alterações no banco de dados
            session.commit()
            
            # Retorna os usuario exlcuidos e os não encontrados caso a erros
            return {
                "deleted_user_ids": [user.id for user in deleted_users],
                "not_found_user_ids": not_found_users,
                "message": "Usuários excluídos com sucesso."
            }, 200
            
        else:
            return {"message": "Nenhum usuário encontrado."}, 404
    except Exception as e:
        session.rollback()
        return {"message": str(e)}, 500
    finally:
        session.close()
