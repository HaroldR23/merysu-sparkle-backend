# 1️⃣ Imagen base oficial de AWS Lambda para Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# 2️⃣ Variables de entorno para Python y Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# 3️⃣ Instalar Poetry
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

# 4️⃣ Definir directorio de trabajo dentro del contenedor
WORKDIR /var/task

# 5️⃣ Copiar solo archivos de dependencias (mejor cache)
COPY pyproject.toml poetry.lock ./

# 6️⃣ Instalar dependencias (sin dev)
RUN poetry install --no-root --only main

# 7️⃣ Copiar el resto del código de la aplicación
COPY . .

# 8️⃣ Comando que AWS Lambda ejecutará
CMD ["lambda_handler.handler"]
