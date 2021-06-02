from typing import NamedTuple, Set


GOODS_SEPARATOR_SYMBOL = ","
GOODS_EXCLUDE_SYMBOL = "-"


class IngredientComposition(NamedTuple):
    """
    Список желательных и нежелательных ингредиентов для коктейля
    """

    include_ingredients: Set[str]
    exclude_ingredients: Set[str]


def get_ingredients_from_str(goods_string: str) -> IngredientComposition:
    """
    Из строки получаем список желательных и нежелательных ингредиентов
    """
    include_ingredients = set()
    exclude_ingredients = set()

    for good in goods_string.split(GOODS_SEPARATOR_SYMBOL):
        good = good.strip().lower()
        if good.startswith(GOODS_EXCLUDE_SYMBOL):
            good = good.lstrip(GOODS_EXCLUDE_SYMBOL).lstrip()
            exclude_ingredients.add(good)
        else:
            include_ingredients.add(good)
    include_ingredients -= exclude_ingredients

    return IngredientComposition(include_ingredients, exclude_ingredients)
