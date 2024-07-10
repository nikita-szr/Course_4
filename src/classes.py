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
        self.__products = products
        Category.category_count += 1
        Category.unique_products += len(products)

    def add_product(self, product):
        """Метод для добавления товара в категорию."""
        self.__products.append(product)
        Category.unique_products += 1

    @property
    def list_of_products(self):
        """Геттер для получения списка товаров в формате: 'Продукт, 80 руб. Остаток: 15 шт."""
        formatted_products = [
            f"{Product.product_name}, {Product.price} руб. Остаток: {Product.quantity} шт."
            for product in self.__products
        ]
        return "\n".join(formatted_products)

    def __len__(self):
        """Метод для получения количества продуктов в категории."""
        return sum(product.quantity for product in self.__products)

    def __str__(self):
        """Строковое отображение категории."""
        return f"{self.category_name}, количество продуктов: {len(self)} шт."


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
        self._price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict, products_list: list):
        """Метод класса для создания нового продукта. При наличии дубликата обновляет количество и цену"""
        product_name = product_data['product_name']
        description = product_data['description']
        price = product_data['price']
        quantity = product_data['quantity']

        for product in products_list:
            if product.product_name == product_name:
                product.quantity += quantity
                product.price = max(product.price, price)
                return product

        new_product = cls(product_name, description, price, quantity)
        products_list.append(new_product)
        return new_product

    @property
    def product_price(self):
        """Геттер для получения цены"""
        return self.price

    @product_price.setter
    def product_price(self, new_price):
        """Сеттер для установки цены с проверкой > 0"""
        if new_price > 0:
            if self.price > new_price:
                user_agreement = input('Понизить цену? "y" - если да, "n" - если нет :')
                if user_agreement.lower() == "y":
                    self._price = new_price
        else:
            print("Цена введена некорректная")

    def __str__(self):
        return f'{self.product_name}, {self.price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
        """Магический метод для сложения продуктов по правилу: цена * количество"""
        return (self._price * self.quantity) + (other.price * other.quantity)


class CategoryIterator:
    """Класс для итерации по товарам в категории"""

    def __init__(self, category):
        """Инициализация итератора с категорией"""
        self._category = category
        self._index = 0

    def __iter__(self):
        """Возвращает итератор"""
        return self

    def __next__(self):
        pass


class Smartphones(Product):
    def __init__(self, product_name, description, price, quantity, performance, model, storage, color):
        super().__init__(product_name, description, price, quantity)
        self.perfomance = performance
        self.model = model
        self.storage = storage
        self.color = color


class Lawngrass(Product):
    def __init__(self, product_name, description, price, quantity, country, germination, color):
        super().__init__(product_name, description, price, quantity)
        self.country = country
        self.germination = germination
        self.color = color


def get_json_data(path):
    """Выгружает данные товаров из json файла"""
    with open(path, "r", encoding="utf-8") as json_file:
        products_data = json.load(json_file)
    return products_data


def create_category_classes(products_data):
    """Создает классы категорий"""
    categories = []
    for category_data in products_data:
        category = Category(
            category_data.get("name"),
            category_data.get("description"),
            category_data.get("products"),
        )
        categories.append(category)
    return categories


def create_product_classes(product_data):
    """Создает классы продуктов"""
    products_list = []
    for products in product_data:
        list_of_products = products.get("products")
        for product_info in list_of_products:
            product = Product(
                product_info.get("name"),
                product_info.get("description"),
                product_info.get("price"),
                product_info.get("quantity"),
            )
            products_list.append(product)
    return products_list
