import requests
from skillup.test.search.schema import Query, SearchResult


def main():
    query = Query(partition_id=1, max_results=10, query="Who wrote the Harry Potter series")
    response = requests.post(url="http://localhost:8080/answer", data=query.json())

    assert 200 == response.status_code, "Query failed"
    data = response.json()
    assert data is not None, "No results"
    answers = SearchResult(**data)

    assert len(answers.answers) == 10, "Wrong number of rows returned"

    for i, ans in enumerate(answers.answers):
        print(f"{i}) - {ans.answer_tx}")

    print("Success")


if __name__ == '__main__':
    main()