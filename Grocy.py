import uuid

import httpx
from typing import TypedDict


class Client:
    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.Client(
            base_url=base_url,
            headers={"GROCY-API-KEY": api_key}
        )

    def get_user_field(self, name: str, entity_type: str) -> UserField:
        data: list[UserField] = self.client.get('/api/objects/userfields', params={
            'query[]': [f"name={name}", f"entity={entity_type}"]
        }).json()
        return next(iter(data), None)

    def create_mealie_field(self, name: str, entity_type: str):
        self.client.post('/api/objects/userfields', json={
            'name': name,
            'entity': entity_type,
            'caption': 'Mealie ID',
            'type': 'text-single-line',
            'showInTable': 0,
            'required': 0,
        })

    def get_recipe_by_mealie_id(self, mealie_id: str):
        data: list[Recipe] = self.client.get('/api/objects/recipes').json()
        for recipe in data:
            if recipe.get('userfields', {}).get('mealieId') == str(mealie_id):
                return recipe
        return None

class Recipe(TypedDict):
     id: int
     name: str
     userfields: dict

class UserField(TypedDict):
    id: int
    name: str
    entity: str

class UserFieldQuery(TypedDict):
    name: str
    entity: str
