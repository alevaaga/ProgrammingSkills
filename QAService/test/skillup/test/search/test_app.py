import requests
from pydantic import parse_obj_as
from skillup.test.search.schema import Query, SearchResult


def main():
    query = Query(partition_id=2, max_results=10, query="The fire extinguisher is showing red")
    response = requests.post(url="http://localhost:8080/answer", data=query.json())

    assert 200 == response.status_code, "Query failed"

    data = parse_obj_as(SearchResult, response.json())
    assert data is not None, "No results"
    assert len(data.answers) > 0, "Wrong number of rows returned"

    print("Success")
    for answer in data.answers:
        print(answer)


if __name__ == '__main__':
    main()
