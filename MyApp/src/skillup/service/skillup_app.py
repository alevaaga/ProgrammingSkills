import uvicorn
from fastapi import FastAPI
from skillup.bizlogic.searchlogic import EPSearchLogic
from skillup.schema import EPSearchResult, EPQuery

app = FastAPI()


@app.post(path="/find_ep", response_model=EPSearchResult)
def find_ep(query: EPQuery) -> EPSearchResult:
    searchlogic = EPSearchLogic()
    result_list = searchlogic.find(query)
    result = EPSearchResult(eps=result_list)
    return result


if __name__ == '__main__':
    uvicorn.run("skillup.service.skillup_app:app", host="0.0.0.0", port=8080, reload=True)
