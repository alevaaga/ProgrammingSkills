import requests
from pydantic import parse_obj_as

from skillup.schema.schema import EPQuery, EPSearchResult


def main():
    query = EPQuery(prg_typ_id=2, max_results=100, query="The fire extinguisher is showing red")
    response = requests.post(url="http://localhost:8080/find_ep", data=query.json())

    assert 200 == response.status_code, "Query failed"

    data = parse_obj_as(EPSearchResult, response.json())
    assert data is not None, "No results"
    assert len(data.eps) > 0, "Wrong number of rows returned"


if __name__ == '__main__':
    main()