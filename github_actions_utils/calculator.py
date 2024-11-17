"""
github_actions_utils.calculator
=============================

A utility package for integrating GitHub Actions with a GraphQL API, providing
calculator operations and book queries.

"""
from typing import List

import strawberry
from flask import Flask
from strawberry import Schema
from strawberry.flask.views import GraphQLView

app = Flask(__name__)

# pylint: disable=R0903
@strawberry.type
class Book:
  """A class representing a book with a title and an author."""
  title: str
  author: str

  def __init__(self, title: str, author: str):
    self.title = title
    self.author = author

  def __repr__(self):
    return f"Book(title={self.title!r}, author={self.author!r})"


def get_books():
  """A function that returns a list of books."""
  return [Book(title="The Great Gatsby", author="F. Scott Fitzgerald", ), ]


def resolve_add(a, b):
  """A function that adds two numbers."""
  return a + b


def resolve_subtract(a, b):
  """A function that subtracts two numbers."""
  return a - b


def resolve_multiply(a, b):
  """A function that multiplies two numbers."""
  return a * b


def resolve_divide(a, b):
  """A function that divides two numbers."""
  if b == 0:
    raise ValueError("Cannot divide by zero!")
  return a / b


# Query
@strawberry.type
class Query:
  """A class representing a query that returns a list of books."""
  books: List[Book] = strawberry.field(resolver=get_books)

  @strawberry.field
  def add(self, a: int, b: int) -> int:
    """A function that adds two numbers."""
    return a + b

  @strawberry.field
  def subtract(self, a: int, b: int) -> int:
    """A function that subtracts two numbers."""
    return a - b

  @strawberry.field
  def multiply(self, a: int, b: int) -> int:
    """A function that multiplies two numbers."""
    return a * b

  @strawberry.field
  def divide(self, a: int, b: int) -> float:
    """A function that divides two numbers."""
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
