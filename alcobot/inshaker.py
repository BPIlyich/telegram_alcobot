import random
from typing import Dict, Optional, Set
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from utils import IngredientComposition, get_ingredients_from_str


MAIN_URL = "https://ru.inshaker.com"
INGREDIENTS_URI = "goods"


def get_ingredient_uri(
    good_name: str, ingredients_uri: str = INGREDIENTS_URI
) -> Optional[str]:
    """
    Возвращает uri ингредиента или None
    """
    soup = get_soup(ingredients_uri)
    for ingredient in soup.find_all("a", {"class": "common-good-icon"}):
        if ingredient.find(string=lambda x: x.lower().strip() == good_name):
            return ingredient.get("href")
    return None


def get_cocktails_recipes_uri_set(
    ingredient_uri: str,
    ingredient_composition: IngredientComposition,
) -> Set[str]:
    """
    Возвращает все подходящие uri коктейлей
    """
    soup = get_soup(ingredient_uri)
    cocktails_recipes_uri_set = set()

    while True:
        for cocktail_div in soup.find_all("div", {"class": "cocktail-item"}):
            ingredients_set = {
                ingredient_div.getText().strip().lower()
                for ingredient_div in cocktail_div.find_all(
                    "div", {"class": "cocktail-item-good-name"}
                )
            }

            if ingredient_composition.include_ingredients.issubset(
                ingredients_set
            ) and ingredient_composition.exclude_ingredients.isdisjoint(
                ingredients_set
            ):
                cocktail_uri = cocktail_div.find(
                    "a", {"class": "cocktail-item-preview"}
                )["href"]
                cocktails_recipes_uri_set.add(cocktail_uri)

        if next_uri := soup.find("a", {"class": ["common-more", "common-list-state"]}):
            soup = get_soup(next_uri["href"])
        else:
            break

    return cocktails_recipes_uri_set


def get_soup(
    uri: Optional[str] = None,
    base_url: str = MAIN_URL,
    url_params: Optional[Dict[str, str]] = {
        "pagination": "true",
        "respond_with": "body",
    },
) -> BeautifulSoup:
    """
    Вспомогательная функция для получения объекта BeautifulSoup
    """
    full_url = urljoin(base_url, uri)
    res = requests.get(full_url, url_params)
    html_doc = res.text
    return BeautifulSoup(html_doc, "html.parser")


def get_random_recipe_url(raw_string: str) -> str:
    """
    Отдает url случайного подходящего рецепта или сообщение о неудаче.
    """
    ingredient_composition = get_ingredients_from_str(raw_string)
    if ingredient_composition.include_ingredients:
        ingredient = ingredient_composition.include_ingredients.pop()
        if ingredient_uri := get_ingredient_uri(ingredient):
            cocktails_recipes_uri_set = get_cocktails_recipes_uri_set(
                ingredient_uri, ingredient_composition
            )
            random_recipe = random.sample(tuple(cocktails_recipes_uri_set), 1)[0]
            url = urljoin(MAIN_URL, random_recipe)
            return url
    text = (
        "Подходящий рецепт не найден."
        "Убедитесь что в запросе присутствует хотя бы 1 ингредиент со страницы"
        "https://ru.inshaker.com/goods"
    )
    return text
