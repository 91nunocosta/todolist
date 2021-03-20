FROM python

RUN pip install poetry

WORKDIR app

COPY poetry.lock pyproject.toml ./

RUN poetry install

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY ./todolist todolist

ENTRYPOINT ["poetry", "run", "python", "todolist/run.py"]
