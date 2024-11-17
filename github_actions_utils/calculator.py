from typing import List

import strawberry
from flask import Flask
from strawberry import Schema
from strawberry.flask.views import GraphQLView

app = Flask(__name__)


@strawberry.type
class Book:
  title: str
  author: str


@strawberry.type
class Query:
  books: List[Book]


def get_books():
  return [Book(title="The Great Gatsby", author="F. Scott Fitzgerald", ), ]


def resolve_add(a, b):
  return a + b


def resolve_subtract(a, b):
  return a - b


def resolve_multiply(a, b):
  return a * b


def resolve_divide(a, b):
  if b == 0:
    raise ValueError("Cannot divide by zero!")
  return a / b


# Query
@strawberry.type
class Query:
  books: List[Book] = strawberry.field(resolver=get_books)

  @strawberry.field
  def add(self, a: int, b: int) -> int:
    return a + b

  @strawberry.field
  def subtract(self, a: int, b: int) -> int:
    return a - b

  @strawberry.field
  def multiply(self, a: int, b: int) -> int:
    return a * b

  @strawberry.field
  def divide(self, a: int, b: int) -> float:
    if b == 0:
      raise ValueError("Cannot divide by zero!")
    return a / b


# Schema
schema = Schema(query=Query)

# GraphQL View
app.add_url_rule('/graphql',
                 view_func=GraphQLView.as_view('graphql', schema=schema,
                                               graphiql=True))

if __name__ == '__main__':
  app.run(debug=True)
