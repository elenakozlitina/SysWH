# warehouse.py

class Warehouse:
    def __init__(self):
        self.inventory = {}

    def add_item(self, item_name, quantity):
        """Добавляет товар на склад."""
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity

    def remove_item(self, item_name, quantity):
        """Удаляет товар со склада."""
        if item_name in self.inventory:
            if self.inventory[item_name] >= quantity:
                self.inventory[item_name] -= quantity
                if self.inventory[item_name] == 0:
                    del self.inventory[item_name]
            else:
                raise ValueError("Недостаточно товара на складе")
        else:
            raise ValueError("Товар не найден на складе")

    def get_inventory(self):
        """Возвращает текущий инвентарь склада."""
        return self.inventory