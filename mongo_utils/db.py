# pylint: disable=too-few-public-methods,redefined-builtin
"""
A utility package for integrating MongoDB with a GraphQL API

"""
from dataclasses import dataclass, asdict
from typing import Optional, List

import strawberry
from bson import ObjectId
from mongojet import create_client, Client
from mongojet._types import DeleteResult

from configuration import get_config

CONFIG = get_config()


class ItemNotFoundException(Exception):
  """Raised when an item is not found"""


# Connect to MongoDB
async def get_client() -> Client:
  """
  Connect to MongoDB

  :param cfg:
  :return:
  """
  client: Client = await create_client(CONFIG.mongodb_uri)
  return client


async def get_db(db_name: str):
  """
  :param db_name:
  :return:
  """
  client: Client = await get_client()
  return client.get_database(db_name)


async def get_collection(db_name: str, collection_name: str):
  """

  :param db_name:
  :param collection_name:
  :return:
  """
  db = await get_db(db_name)
  return db.get_collection(collection_name)


# Define a MongoJet document model
@dataclass
class Item:
  """

  :param name:
  :param description:
  """

  def __init__(self, name, description):
    self.name = name
    self.description = description

  name: str
  description: Optional[str] = None


# GraphQL type
@strawberry.type
class ItemType:
  """
    Strawberry output ItemType
  """
  id: str
  name: str
  description: Optional[str] = None


# GraphQL mutations
@strawberry.type
class MongoMutation:
  """
    Strawberry mutation
  """

  @strawberry.mutation
  async def create_item(self, name: str,
      description: Optional[str] = None) -> ItemType:
    """

    :param name:
    :param description:
    :return:
    """
    item = Item(name, description)
    collection = await get_collection("github_actions", "items")

    i = asdict(item)
    await collection.insert_one(i)  # Save the item to the database
    return ItemType(id=str(i.get("_id")), name=i.get("name"),
                    description=i.get("description"))

  @strawberry.mutation
  async def update_item(self, id: str, name: str,
      description: Optional[str] = None) -> ItemType:
    """

    :param id:
    :param name:
    :param description:
    :return:
    """
    collection = await get_collection("github_actions", "items")
    item = await collection.find_one({"_id": ObjectId(id)})
    if item:
      item["name"] = name
      item["description"] = description
      await collection.replace_one({"_id": ObjectId(id)}, item)
      # Update the item in the database
      return ItemType(id=str(item.get("_id")), name=item.get("name"),
                      description=item.get("description"))
    raise ItemNotFoundException("Item not found")

  @strawberry.mutation
  async def delete_item(self, id: str) -> bool:
    """

    :param id:
    :return:
    """
    collection = await get_collection("github_actions", "items")
    result: DeleteResult = await collection.delete_one({"_id": ObjectId(id)})
    return result["deleted_count"]


# GraphQL queries
@strawberry.type
class MongoQuery:
  """
    Strawberry query
  """

  @strawberry.field
  async def get_item(self, id: str) -> Optional[ItemType]:
    """

    :param id:
    :return:
    """
    collection = await get_collection("github_actions", "items")
    item = await collection.find_one({"_id": ObjectId(id)})
    if item:
      return ItemType(id=str(item.get("_id")), name=item.get("name"),
                      description=item.get("description"))
    return None

  @strawberry.field
  async def list_items(self) -> List[ItemType]:
    """

    :return:
    """
    collection = await get_collection("github_actions", "items")
    items = await collection.find_many()
    return [ItemType(id=str(item.get("_id")), name=item.get("name"),
                     description=item.get("description")) for item in items]
