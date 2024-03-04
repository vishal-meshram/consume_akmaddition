from http import HTTPStatus
from pydantic import BaseModel, Field, ValidationError
from akmaddition.addition import Addition

from flask_openapi3 import OpenAPI

info = {"title": "sum API", "version": "0.0.1"}

app = OpenAPI(__name__, info=info)


class NumbersBody(BaseModel):
    num1: float = Field(description="Number 1")
    num2: float = Field(description="Number 2")


class SumResponse(BaseModel):
    num1: float = Field(description="Number 1")
    num2: float = Field(description="Number 2")
    sum: float = Field(description="Addtion result")


@app.post("/sum", responses={200: SumResponse})
def sum(body: NumbersBody):
    try:
        add_instance = Addition()
        result = add_instance.addition(body.num1, body.num2)
        response = SumResponse(num1=body.num1, num2=body.num2, sum=result)
        return response.model_dump_json(), HTTPStatus.OK
    except ValidationError as ve:
        return {"error": f"Validation Error: {ve}"}
    except Exception as e:
        return {"error": f"Error: {e}"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

