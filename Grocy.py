from dataclasses import dataclass
from typing import TypedDict

import httpx


class Product(TypedDict):
    id: int
    name: str
    userfields: dict

class RecipeIngredient(TypedDict):
    product_id: int
    recipe_id: int

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

    def get_user_field(self, name: str, entity_type: str) -> UserField | None:
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

    def get_recipe_by_mealie_id(self, mealie_id: str) -> Recipe | None:
        data: list[Recipe] = self.client.get('/api/objects/recipes').raise_for_status().json()
        for recipe in data:
            if recipe.get('userfields', {}).get('mealieId') == str(mealie_id):
                return recipe
        return None

    def get_product_by_mealie_id(self, mealie_id: str) -> Product | None:
        data: list[Product] = self.client.get('/api/objects/products').raise_for_status().json()
        for product in data:
            if product.get('userfields', {}).get('mealieId') == str(mealie_id):
                return product
        return None

    def get_recipe_ingredient(self, recipe_id: int, product_id: int) -> RecipeIngredient | None:
        data: list[RecipeIngredient] = self.client.get('/api/objects/recipes_pos', params={
            'query[]': [f"recipe_id={recipe_id}", f"product_id={product_id}"]
        }).raise_for_status().json()

        for ingredient in data:
            if ingredient['recipe_id'] == recipe_id and ingredient['product_id'] == product_id:
                return ingredient

        return None
