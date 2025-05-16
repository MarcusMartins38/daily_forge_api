# Usa a imagem oficial do Python
FROM python:3.9

# Define o diretório de trabalho no container
WORKDIR /code

# Copia as dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Expõe a porta usada pelo Django
EXPOSE 3000

# Comando padrão (sobrescrito pelo docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
