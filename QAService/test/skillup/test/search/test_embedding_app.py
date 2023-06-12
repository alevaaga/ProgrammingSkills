import requests
from qaservice.common import TextInput, Embedding


def main():
    query = TextInput(text="Hello there.")
    response = requests.post(url="http://localhost:8081/embed", data=query.json())

    assert 200 == response.status_code, "Query failed"
    data = response.json()
    assert data is not None, "No results"
    embedding = Embedding(**data)

    assert len(embedding.embedding) == 768, "Wrong number of rows returned"

    print(embedding.embedding)
    print("Success")


if __name__ == '__main__':
    main()