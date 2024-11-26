"""
Run with `uvicorn main:app --reload`

"""
import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from github_actions_utils.calculator import CalculatorQuery
from github_actions_utils.messaging_consumer import Subscription
from mongo_utils.db import MongoMutation, MongoQuery


@strawberry.type
class Query(MongoQuery, CalculatorQuery):
  """
  Main Query Class with all queries
  """


# Schema
schema = Schema(query=Query, subscription=Subscription, mutation=MongoMutation)
graphql_app = GraphQLRouter(schema)
origins = ["http://localhost", "http://localhost:8000", ]

app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )
