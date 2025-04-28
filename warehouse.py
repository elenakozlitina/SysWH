from typing import List, Dict

class WarehouseErrorMessages:
    """Класс для хранения сообщений об ошибках склада."""
    NOT_ENOUGH = "Недостаточно товара на складе"
    NOT_FOUND = "Товар не найден на складе"
    NEGATIVE_QUANTITY = "Количество не может быть отрицательным"

class Notifications:
    """Класс для управления уведомлениями."""
    def __init__(self) -> None:
        self._messages: List[str] = []

    def add_notification(self, message: str) -> None:
        self._messages.append(message)

    def get_notifications(self) -> List[str]:
        return self._messages.copy()

    def clear_notifications(self) -> None:
        self._messages.clear()

class Warehouse:
    def __init__(self) -> None:
        self._inventory: Dict[str, int] = {}
        self.notifications = Notifications()  # подключаем уведомления

    def add_item(self, item_name: str, quantity: int) -> None:
        self._validate_quantity(quantity)
        self._inventory[item_name] = self._inventory.get(item_name, 0) + quantity
        self.notifications.add_notification(f"Добавлено {quantity} ед. товара '{item_name}' на склад.")

    def remove_item(self, item_name: str, quantity: int) -> None:
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

    def get_inventory(self) -> Dict[str, int]:
        return self._inventory.copy()

    def _validate_quantity(self, quantity: int) -> None:
        if quantity < 0:
            self.notifications.add_notification(WarehouseErrorMessages.NEGATIVE_QUANTITY)
            raise ValueError(WarehouseErrorMessages.NEGATIVE_QUANTITY)
