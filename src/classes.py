import json


class Category:
    """Класс для категории"""
    category_name: str
    description: str
    products: list
    category_count = 0
    unique_products = 0

    def __init__(self, category_name, description, products):
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.category_name = category_name
        self.description = description
        self.products = products
        Category.category_count += 1
        Category.unique_products += len(products)


class Product:
    """Класс для продукта"""
    product_name: str
    description: str
    price: float
    quantity: int

    def __init__(self, product_name, description, price, quantity):
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.product_name = product_name
        self.description = description
        self.price = price
        self.quantity = quantity


def get_json_data(path):
    """Выгружает данные товаров из json файла"""
    with open(path, 'r', encoding='utf-8') as json_file:
        products_data = json.load(json_file)
    return products_data


def create_category_classes(products_data):
    """Создает классы категорий"""
    categories = []
    for category_data in products_data:
        category = Category(category_data.get('name'), category_data.get('description'), category_data.get('products'))
        categories.append(category)
    return categories


def create_product_classes(product_data):
    """Создает классы продуктов"""
    products_list = []
    for products in product_data:
        list_of_products = products.get('products')
        for product_info in list_of_products:
            product = Product(product_info.get('name'), product_info.get('description'), product_info.get('price'), product_info.get('quantity'))
            products_list.append(product)
    return products_list
