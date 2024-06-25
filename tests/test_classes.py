import pytest
import json
from src.classes import Category, Product


@pytest.fixture()
def category_pasta():
    return Category("Паста", "Разные макаронные изделия", ['спагетти', 'перья'])
@pytest.fixture()
def category_gaming_consoles():
    return Category("Консоли", "Игровые приставки", ['Playstation', 'Nintendo Switch'])


def test_category_init(category_pasta, category_gaming_consoles):
    assert category_pasta.category_name == "Паста"
    assert category_pasta.description == "Разные макаронные изделия"
    assert category_pasta.products == ['спагетти', 'перья']
    assert category_pasta.unique_products == 4
    assert category_pasta.category_count == 2

    assert category_gaming_consoles.category_name == "Консоли"
    assert category_gaming_consoles.description == "Игровые приставки"
    assert category_gaming_consoles.products == ['Playstation', 'Nintendo Switch']
    assert category_gaming_consoles.unique_products == 4
    assert category_gaming_consoles.category_count == 2






