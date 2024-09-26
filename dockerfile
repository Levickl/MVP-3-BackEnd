# Usar uma imagem oficial do Python como base
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de requisitos e o código da aplicação
COPY requisitos.txt ./ 
COPY . .

# Instalar as dependências
RUN pip install -r requisitos.txt

# Definir a variável de ambiente FLASK_APP
ENV FLASK_APP=app.py

# Expor a porta 5000
EXPOSE 5000

# Definir o comando para rodar a aplicação Flask
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
