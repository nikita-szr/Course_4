import pytest

from src.classes import Category, Product


@pytest.fixture()
def category_pasta():
    return Category("Паста", "Разные макаронные изделия", ["спагетти", "перья"])


@pytest.fixture()
def category_gaming_consoles():
    return Category("Консоли", "Игровые приставки", ["Playstation", "Nintendo Switch"])


def test_category_init(category_pasta, category_gaming_consoles):
    assert category_pasta.category_name == "Паста"
    assert category_pasta.description == "Разные макаронные изделия"
    assert category_pasta.unique_products == 4
    assert category_pasta.category_count == 2

    assert category_gaming_consoles.category_name == "Консоли"
    assert category_gaming_consoles.description == "Игровые приставки"
    assert category_gaming_consoles.unique_products == 4
    assert category_gaming_consoles.category_count == 2


@pytest.fixture()
def product_smartphone():
    return Product(
        "Samsung Galaxy C23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )


@pytest.fixture()
def product_tv():
    return Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)


def test_product_init(product_smartphone, product_tv):
    assert product_smartphone.product_name == "Samsung Galaxy C23 Ultra"
    assert product_smartphone.description == "256GB, Серый цвет, 200MP камера"
    assert product_smartphone._price == 180000.0
    assert product_smartphone.quantity == 5

    assert product_tv.product_name == '55" QLED 4K'
    assert product_tv.description == "Фоновая подсветка"
    assert product_tv._price == 123000.0
    assert product_tv.quantity == 7


def test_product_addition():
    product1 = Product("Phone1", "Smartphone", 1000, 10)
    product2 = Product("Phone2", "Smartphone", 2000, 5)
    result = product1 + product2
    assert result == 20000


def test_list_of_products():
    product1 = Product("Iphone", "Smartphone", 100000, 10)
    category = Category("Electronics", "Various electronic products", [product1])
    expected_output = "Iphone, 100000 руб. Остаток: 10 шт."
    assert category.list_of_products == expected_output


def test_add_non_product_to_category():
    product1 = Product("Iphone", "Smartphone", 100000, 10)
    category = Category("Electronics", "Various electronic products", [product1])

    with pytest.raises(TypeError):
        category.add_product("not a product")
