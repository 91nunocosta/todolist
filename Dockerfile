FROM python

RUN pip install poetry

WORKDIR app

COPY poetry.lock pyproject.toml ./

RUN poetry install

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY ./todolist todolist

RUN poetry build

RUN poetry install

WORKDIR /app/todolist

ENTRYPOINT ["poetry", "run", "python", "run.py", "--host=0.0.0.0", "--port=5000"]
