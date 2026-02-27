from configparser import ConfigParser

import Grocy
import Mealie


if __name__ == '__main__':
    with open('config.ini') as config_file:
        config = ConfigParser()
        config.read_file(config_file)

    mealie = Mealie.Client(
        config['mealie']['url'],
        config['mealie']['token']
    )

    grocy = Grocy.Client(
        config['grocy']['url'],
        config['grocy']['key']
    )

    products_user_field = grocy.get_user_field(
        'mealieId',
        'products'
    )

    if products_user_field is None:
        grocy.create_mealie_field(
            'mealieId',
            'products'
        )

    recipes_user_field = grocy.get_user_field(
        'mealieId',
        'recipes'
    )

    if recipes_user_field is None:
        grocy.create_mealie_field(
            'mealieId',
            'recipes'
        )

    mealie_recipies = mealie.get_recipes()

    for mealie_recipe in mealie_recipies:
        grocy_recipe = grocy.get_recipe_by_mealie_id(mealie_recipe['id'])

        if grocy_recipe is None:
            continue

        mealie_recipe = mealie.get_recipe(mealie_recipe['id'])

        if mealie_recipe is None:
            continue

        print(mealie_recipe)