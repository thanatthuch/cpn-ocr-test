from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from model import my_ocr

app = FastAPI()

class Body(BaseModel):
    image64: str


@app.post("/slip-detect")
def slip_detect(body: Body):
    # CALL SERVICE
    try:
        return {"status": 200,"message":"success", "data" : my_ocr.detect(body.image64)}
    except:
        return {"status": 500, "message": "error" , "data" : {}}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info")