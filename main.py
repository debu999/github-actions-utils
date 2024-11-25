"""
Run with `uvicorn main:app --reload`

"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from github_actions_utils.calculator import schema

graphql_app = GraphQLRouter(schema)
origins = ["http://localhost", "http://localhost:8000", ]

app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )
