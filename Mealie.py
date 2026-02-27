from dataclasses import dataclass
from typing import TypedDict, NotRequired

import httpx

@dataclass
class Client:
    base_url: str
    token: str

    def __enter__(self):
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.token}"}
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_shopping_lists(self) -> list[ShoppingList]:
        data: Response[ShoppingList] = self.client.get(
            '/api/households/shopping/lists',
            params={ "perPage": -1 }
        ).raise_for_status().json()
        return data['items']

    def get_foods(self) -> list[Food]:
        data: Response[Food] = self.client.get(
            '/api/foods',
            params={ "perPage": -1 }
        ).raise_for_status().json()
        return data["items"]

    def get_recipes(self) -> list[Recipe]:
        data: Response[Recipe] = self.client.get(
            '/api/recipes',
            params={ "perPage": -1 }
        ).raise_for_status().json()
        return data['items']

    def get_recipe(self, mealie_id: str) -> Recipe:
        data: Recipe = self.client.get(
            f'/api/recipes/{mealie_id}'
        ).raise_for_status().json()
        return data


class Response[T](TypedDict):
    items: list[T]

class Unit:
    id: str
    name: str

class Ingredient(TypedDict):
    quantity: float
    unit: Unit
    food: Food

class Recipe(TypedDict):
    id: str
    name: str
    recipeIngredient: NotRequired[list[Ingredient]]

class ShoppingList(TypedDict):
    name: str

class Food(TypedDict):
    id: str
    name: str
