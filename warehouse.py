from typing import List, Dict
from werkzeug.security import generate_password_hash, check_password_hash

# Класс для хранения сообщений об ошибках склада
class WarehouseErrorMessages:
    NOT_ENOUGH = "Недостаточно товара на складе"
    NOT_FOUND = "Товар не найден на складе"
    NEGATIVE_QUANTITY = "Количество не может быть отрицательным"

# Класс для управления уведомлениями
class Notifications:
    def __init__(self) -> None:
        self._messages: List[str] = []

    def add_notification(self, message: str) -> None:
        self._messages.append(message)

    def get_notifications(self) -> List[str]:
        return self._messages.copy()

    def clear_notifications(self) -> None:
        self._messages.clear()

# Класс для представления пользователя
class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password_hash = generate_password_hash(password)  # Хешируем пароль

    def check_password(self, password: str) -> bool:
        """Проверяем, совпадает ли введенный пароль с хешом"""
        return check_password_hash(self.password_hash, password)

# Основной класс склада
class Warehouse:
    def __init__(self) -> None:
        self._inventory: Dict[str, int] = {}
        self.notifications = Notifications()  # подключаем уведомления
        self.users = {}  # Пользователи
        self.logged_in_user = None  # Текущий авторизованный пользователь

    # Метод для регистрации нового пользователя
    def register_user(self, username: str, password: str) -> None:
        """Регистрация нового пользователя с хешированием пароля"""
        new_user = User(username, password)
        self.users[username] = new_user
        print(f"Пользователь {username} зарегистрирован")

    # Метод для входа пользователя в систему
    def login_user(self, username: str, password: str) -> bool:
        """Аутентификация пользователя"""
        user = self.users.get(username)
        if user and user.check_password(password):
            self.logged_in_user = user
            print(f"Пользователь {username} успешно вошел")
            return True
        print("Неверный логин или пароль")
        return False

    # Метод для выхода из системы
    def logout_user(self) -> None:
        """Выход из системы"""
        self.logged_in_user = None
        print("Пользователь вышел из системы.")

    # Проверка наличия авторизации перед выполнением операций
    def _check_authorization(self) -> bool:
        if self.logged_in_user is None:
            print("Ошибка: доступ запрещен. Пожалуйста, войдите в систему.")
            return False
        return True

    # Добавление товара на склад
    def add_item(self, item_name: str, quantity: int) -> None:
        if not self._check_authorization():
            return
        self._validate_quantity(quantity)
        self._inventory[item_name] = self._inventory.get(item_name, 0) + quantity
        self.notifications.add_notification(f"Добавлено {quantity} ед. товара '{item_name}' на склад.")

    # Удаление товара со склада
    def remove_item(self, item_name: str, quantity: int) -> None:
        if not self._check_authorization():
            return
        self._validate_quantity(quantity)

        if item_name not in self._inventory:
            self.notifications.add_notification(WarehouseErrorMessages.NOT_FOUND)
            raise ValueError(WarehouseErrorMessages.NOT_FOUND)

        if self._inventory[item_name] < quantity:
            self.notifications.add_notification(WarehouseErrorMessages.NOT_ENOUGH)
            raise ValueError(WarehouseErrorMessages.NOT_ENOUGH)

        self._inventory[item_name] -= quantity
        self.notifications.add_notification(f"Удалено {quantity} ед. товара '{item_name}' со склада.")

        if self._inventory[item_name] == 0:
            del self._inventory[item_name]
            self.notifications.add_notification(f"Товар '{item_name}' полностью удален со склада.")

    # Получение текущего состояния склада
    def get_inventory(self) -> Dict[str, int]:
        if not self._check_authorization():
            return {}
        return self._inventory.copy()

    # Валидация количества товара
    def _validate_quantity(self, quantity: int) -> None:
        if quantity < 0:
            self.notifications.add_notification(WarehouseErrorMessages.NEGATIVE_QUANTITY)
            raise ValueError(WarehouseErrorMessages.NEGATIVE_QUANTITY)
