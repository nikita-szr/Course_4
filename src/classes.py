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
