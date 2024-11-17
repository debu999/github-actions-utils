"""
This module contains test cases for the calculator functionalities provided by the
GraphQL API, including operations like addition, subtraction, multiplication, and division,
as well as querying book information.
"""
import pytest

from github_actions_utils.calculator import \
  schema  # Adjust the import based on your project structure


# Test for synchronous query execution
def test_query():
  """
  Test for synchronous query execution.

  This test case verifies that querying the schema for book information using the
  `execute_sync` method returns the expected response, i.e., a list of dictionaries
  containing the book title and its author.

  The test case also checks that no errors are present in the result.
  """
  query = """
        query TestQuery {
            books {
                title
                author
            }
        }
    """

  # Act
  result = schema.execute_sync(query)

  # Assert
  assert result.errors is None
  assert result.data["books"] == [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", }]


# Test for asynchronous query execution
@pytest.mark.asyncio
async def test_query_async():
  """
  Test for asynchronous query execution.

  This test case verifies that querying the schema for book information using the
  `execute` method returns the expected response, i.e., a list of dictionaries
  containing the book title and its author.

  The test case also checks that no errors are present in the result.
  """
  query = """
        query TestQuery {
            books {
                title
                author
            }
        }
    """

  # Act
  resp = await schema.execute(query)

  # Assert
  assert resp.errors is None
  assert resp.data["books"] == [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", }]
  query = """
        query TestQuery {
            books {
                title
                author
            }
        }
    """

  # Act
  resp = await schema.execute(query)

  # Assert
  assert resp.errors is None
  assert resp.data["books"] == [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", }]


# Test cases
@pytest.mark.asyncio
async def test_add():
  """
      Test case for asynchronous query execution to add two numbers.

      This test case verifies that querying the schema for adding two numbers
      using the `execute` method returns the expected response, i.e., the result of
      the addition.

      The test case also checks that no errors are present in the result.
      """
  query = """
        query {
            add(a: 2, b: 3)
        }
    """
  result = await schema.execute(query)
  assert result.data["add"] == 5


@pytest.mark.asyncio
async def test_subtract():
  """
      Test case for asynchronous query execution to subtract two numbers.

      This test case verifies that querying the schema for subtracting two numbers
      using the `execute` method returns the expected response, i.e., the result of
      the subtraction.

      The test case also checks that no errors are present in the result.
      """
  query = """
        query {
            subtract(a: 5, b: 2)
        }
    """
  result = await schema.execute(query)
  assert result.data["subtract"] == 3


@pytest.mark.asyncio
async def test_multiply():
  """
    Test case for asynchronous query execution to multiply two numbers.

    This test case verifies that querying the schema for multiplying two numbers
    using the `execute` method returns the expected response, i.e., the result of
    the multiplication.

    The test case also checks that no errors are present in the result.
    """
  query = """
        query {
            multiply(a: 4, b: 5)
        }
    """
  result = await schema.execute(query)
  assert result.data["multiply"] == 20


@pytest.mark.asyncio
async def test_divide():
  """
    Test case for asynchronous query execution to divide two numbers.

    This test case verifies that querying the schema for dividing two numbers
    using the `execute` method returns the expected response, i.e., the result of
    the division.

    The test case also checks that no errors are present in the result.
    """
  query = """
        query {
            divide(a: 10, b: 2)
        }
    """
  result = await schema.execute(query)
  assert result.data["divide"] == 5.0


@pytest.mark.asyncio
async def test_divide_by_zero():
  """
    Test case for handling division by zero in asynchronous query execution.

    This test case verifies that querying the schema for dividing a number by zero
    using the `execute` method raises an error with the expected message, "Cannot divide by zero!".
    """
  query = """
        query {
            divide(a: 10, b: 0)
        }
    """
  result = await schema.execute(query)
  assert result.errors[0].message == "Cannot divide by zero!"


@pytest.mark.asyncio
async def test_custom_input():
  """
    Test case for asynchronous query execution with custom input.

    This test case verifies that querying the schema with custom input using the
    `execute` method returns the expected response, i.e., the result of the
    addition and the queried books.

    The test case also checks that no errors are present in the result.
    """
  query = """
        query {
          books{
            title
            author
          }
          add(a:3, b: 4)
        }
    """
  result = await schema.execute(query)
  assert result.data["add"] == 7
  assert result.data["books"] == [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}]
