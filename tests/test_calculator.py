import pytest

from github_actions_utils.calculator import \
  schema  # Adjust the import based on your project structure


# Test for synchronous query execution
def test_query():
  # Arrange
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
  # Arrange
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
  query = """
        query {
            add(a: 2, b: 3)
        }
    """
  result = await schema.execute(query)
  assert result.data["add"] == 5


@pytest.mark.asyncio
async def test_subtract():
  query = """
        query {
            subtract(a: 5, b: 2)
        }
    """
  result = await schema.execute(query)
  assert result.data["subtract"] == 3


@pytest.mark.asyncio
async def test_multiply():
  query = """
        query {
            multiply(a: 4, b: 5)
        }
    """
  result = await schema.execute(query)
  assert result.data["multiply"] == 20


@pytest.mark.asyncio
async def test_divide():
  query = """
        query {
            divide(a: 10, b: 2)
        }
    """
  result = await schema.execute(query)
  assert result.data["divide"] == 5.0


@pytest.mark.asyncio
async def test_divide_by_zero():
  query = """
        query {
            divide(a: 10, b: 0)
        }
    """
  result = await schema.execute(query)
  assert result.errors[0].message == "Cannot divide by zero!"


@pytest.mark.asyncio
async def test_custom_input():
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
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald_old"}]
