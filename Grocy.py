from dataclasses import dataclass
from typing import TypedDict

import httpx


@dataclass
class Client:
    base_url: str
    api_key: str

    def __enter__(self):
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={"GROCY-API-KEY": self.api_key}
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_user_field(self, name: str, entity_type: str) -> UserField:
        data: list[UserField] = self.client.get('/api/objects/userfields', params={
            'query[]': [f"name={name}", f"entity={entity_type}"]
        }).raise_for_status().json()
        return next(iter(data), None)

    def create_mealie_field(self, name: str, entity_type: str):
        self.client.post('/api/objects/userfields', json={
            'name': name,
            'entity': entity_type,
            'caption': 'Mealie ID',
            'type': 'text-single-line',
            'showInTable': 0,
            'required': 0,
        }).raise_for_status()

    def get_recipe_by_mealie_id(self, mealie_id: str):
        data: list[Recipe] = self.client.get('/api/objects/recipes').raise_for_status().json()
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
