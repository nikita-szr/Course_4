import json
from abc import ABC, abstractmethod


class Mixin:
    """Миксин для вывода информации о созданном объекте"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f'Создан объект: {self}')

    def __repr__(self):
        attributes = [f'{key}: {value}' for key, value in self.__dict__.items()]
        return f"Создан объект {self.__class__.__name__} с атрибутами {', '.join(attributes)}"


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
        if not isinstance(product, Product):
            raise TypeError("Товар должен быть экземпляром класса Product")
        if product.quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.__products.append(product)
        Category.unique_products += 1

    @property
    def list_of_products(self):
        """Геттер для получения списка товаров в формате: 'Продукт, 80 руб. Остаток: 15 шт."""
        formatted_products = [
            f"{product.product_name}, {product._price} руб. Остаток: {product.quantity} шт."
            for product in self.__products
        ]
        return "\n".join(formatted_products)

    def __len__(self):
        """Метод для получения количества продуктов в категории."""
        return sum(product.quantity for product in self.__products)

    def __str__(self):
        """Строковое отображение категории."""
        return f"{self.category_name}, количество продуктов: {len(self)} шт."

    def average_products_price(self):
        """Метод для подсчета средней цены всех товаров в категории"""
        try:
            total_price = sum(product.price for product in self.__products)
            average_price = total_price / len(self.__products)
            return average_price
        except ZeroDivisionError:
            return 0


class Products(ABC):
    """Абстрактный класс для продуктов"""

    def __init__(self, product_name, description, price, quantity):
        self.product_name = product_name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @property
    @abstractmethod
    def product_price(self):
        pass

    @product_price.setter
    @abstractmethod
    def product_price(self, new_price):
        pass


class Product(Mixin, Products):
    """Класс для продукта"""
    product_name: str
    description: str
    price: float
    quantity: int

    def __init__(self, product_name, description, price, quantity):
        super().__init__(product_name, description, price, quantity)
        self._price = price

    @classmethod
    def new_product(cls, product_data: dict, products_list: list):
        """Метод класса для создания нового продукта. При наличии дубликата обновляет количество и цену"""
        product_name = product_data['product_name']
        description = product_data['description']
        price = product_data['price']
        quantity = product_data['quantity']

        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        for product in products_list:
            if product.product_name == product_name:
                product.quantity += quantity
                product._price = max(product._price, price)
                return product

        new_product = cls(product_name, description, price, quantity)
        products_list.append(new_product)
        return new_product

    @property
    def product_price(self):
        """Геттер для получения цены"""
        return self._price

    @product_price.setter
    def product_price(self, new_price):
        """Сеттер для установки цены с проверкой > 0"""
        if new_price > 0:
            if self._price > new_price:
                user_agreement = input('Понизить цену? "y" - если да, "n" - если нет :')
                if user_agreement.lower() == "y":
                    self._price = new_price
        else:
            print("Цена введена некорректно")

    def __str__(self):
        return f'{self.product_name}, {self.price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
        """Магический метод для сложения продуктов по правилу: цена * количество"""
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать продукты разных типов")
        return self._price * self.quantity + other._price * other.quantity


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
        """Возвращает следующий продукт в категории"""
        if self._index < len(self._category.__products):
            product = self._category.__products[self._index]
            self._index += 1
            return product
        else:
            raise StopIteration


class Smartphones(Product):
    """Класс для смартфонов"""

    def __init__(self, product_name, description, price, quantity, performance, model, storage, color):
        super().__init__(product_name, description, price, quantity)
        self.performance = performance
        self.model = model
        self.storage = storage
        self.color = color


class Lawngrass(Product):
    """Класс для газонной травы"""

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
            []
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
