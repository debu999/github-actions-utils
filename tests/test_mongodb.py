"""
This module contains test cases for the MongoDB functionalities provided by the
GraphQL API, including operations like create, get, list, update, and delete,
as well as querying actions data information.

"""
import pytest

from main import schema


@pytest.fixture(scope="module", name="shared_data")
def shared():
  """

  :return:
  """
  # Setup code
  data = {"m0": {}}
  print(data)
  yield data


# Test for synchronous query execution
@pytest.mark.asyncio
async def test_create_document(shared_data):
  """

  :return:
  """
  query = """
    mutation createItem {
      createItem(name: "debabrata", description: "github_actions_11") {
        description
        name
        id
        }
      }
    """

  # Act
  result = await schema.execute(query)

  # Assert
  assert result.errors is None
  assert result.data["createItem"]["description"] == "github_actions_11"
  print(result.data["createItem"])
  shared_data["github_actions_11"] = result.data["createItem"]


@pytest.mark.asyncio
async def test_get_document(shared_data):
  """

  :return:
  """
  doc = shared_data.get("github_actions_11")
  query = f"""
    query getItem {{
    getItem(id: "{doc.get("id")}") {{
      description
      id
      name
      }}
    }}
    """

  # Act
  result = await schema.execute(query)

  # Assert
  assert result.errors is None
  print(result.data["getItem"])
  assert result.data["getItem"]["description"] == "github_actions_11"


@pytest.mark.asyncio
async def test_list_document(shared_data):
  """

  :return:
  """
  query = """
    query listItems {
    listItems {
      description
      id
      name
      }
    }
    """

  # Act
  result = await schema.execute(query)

  # Assert
  assert result.errors is None
  doc = [r for r in result.data["listItems"] if
         r.get("id") == shared_data.get("github_actions_11").get("id")]
  print(doc)
  assert doc


@pytest.mark.asyncio
async def test_update_document(shared_data):
  """

  :return:
  """
  doc = shared_data.get("github_actions_11")
  query = f"""
    mutation updateItem {{
    updateItem(
        id: "{doc.get("id")}"
        name: "debabrata patnaik"
        description: "github_actions_13"
    ) {{
    description
    id
    name
    }}
    }}
    """

  # Act
  result = await schema.execute(query)

  # Assert
  assert result.errors is None
  print(result.data["updateItem"])
  assert result.data["updateItem"]["description"] == "github_actions_13"
  shared_data["github_actions_13"] = result.data["updateItem"]
  print(shared_data["github_actions_13"])


@pytest.mark.asyncio
async def test_delete_document(shared_data):
  """

  :return:
  """
  doc = shared_data.get("github_actions_13")
  query = f"""
    mutation deleteItem {{
      deleteItem(id: "{doc.get("id")}")
      }}
    """

  # Act
  result = await schema.execute(query)

  # Assert
  assert result.errors is None
  print(result.data["deleteItem"])
  assert result.data["deleteItem"]

  query = f"""
      query getItem {{
      getItem(id: "{doc.get("id")}") {{
        description
        id
        name
        }}
      }}
      """

  # Act
  result = await schema.execute(query)

  # Assert
  assert result.errors is None
  print(f"post delete data: {result.data["getItem"]}")
  assert not result.data["getItem"]
