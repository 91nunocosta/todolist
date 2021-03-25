import json

from todolist.app import app

DOC_FILE = "open-api-spec.json"


def get_open_api_spec():
    client = app.test_client()

    response = client.get("/api-docs")

    spec = response.json

    return spec


def write_spec(spec):
    dump = json.dumps(spec, indent=4)
    with open(DOC_FILE, "w") as spec_file:
        spec_file.write(dump)


if __name__ == "__main__":
    spec = get_open_api_spec()
    write_spec(spec)
