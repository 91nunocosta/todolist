FROM python

RUN pip install poetry

WORKDIR /app

# builds the python lib
COPY poetry.lock pyproject.toml ./
COPY ./todolist todolist
RUN poetry build --format wheel

RUN pip install dist/todolist-0.1.0-py3-none-any.whl

ENTRYPOINT ["todolist"]
