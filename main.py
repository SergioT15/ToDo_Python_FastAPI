from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from db import engine
from db import Base
from routes.to_do_route import router
import uvicorn

# Base.metadata.create_all(engine)
Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# python3 -m venv venv
# venv/bin/python -m pip install -r requirements.txt
# source venv/bin/activate
# uvicorn main:app --reload
# deactivate
