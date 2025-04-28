from typing import Dict

class WarehouseErrorMessages:     """Класс для хранения сообщений об ошибках склада."""
    NOT_ENOUGH = "Недостаточно товара на складе"
    NOT_FOUND = "Товар не найден на складе"
    NEGATIVE_QUANTITY = "Количество не может быть отрицательным"

class Warehouse:
    def __init__(self) -> None:
        self._inventory: Dict[str, int] = {}

    def add_item(self, item_name: str, quantity: int) -> None:
        self._validate_quantity(quantity)
        self._inventory[item_name] = self._inventory.get(item_name, 0) + quantity

    def remove_item(self, item_name: str, quantity: int) -> None:
        self._validate_quantity(quantity)
        
        if item_name not in self._inventory:
            raise ValueError(WarehouseErrorMessages.NOT_FOUND)
            
        if self._inventory[item_name] < quantity:
            raise ValueError(WarehouseErrorMessages.NOT_ENOUGH)
            
        self._inventory[item_name] -= quantity
        
        if self._inventory[item_name] == 0:
            del self._inventory[item_name]

    def get_inventory(self) -> Dict[str, int]:
        return self._inventory.copy()

    def _validate_quantity(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError(WarehouseErrorMessages.NEGATIVE_QUANTITY)