import unittest
import sys
import os

# Добавляем корневую директорию в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from warehouse import Warehouse

class TestWarehouse(unittest.TestCase):
    def setUp(self):
        """Инициализация объекта Warehouse перед каждым тестом."""
        self.warehouse = Warehouse()

    def test_add_item(self):
        """Тест добавления товара на склад."""
        self.warehouse.add_item("apple", 10)
        self.assertEqual(self.warehouse.get_inventory(), {"apple": 10})

    def test_add_existing_item(self):
        """Тест добавления товара, который уже есть на складе."""
        self.warehouse.add_item("apple", 10)
        self.warehouse.add_item("apple", 5)
        self.assertEqual(self.warehouse.get_inventory(), {"apple": 15})

    def test_remove_item(self):
        """Тест удаления товара со склада."""
        self.warehouse.add_item("apple", 10)
        self.warehouse.remove_item("apple", 5)
        self.assertEqual(self.warehouse.get_inventory(), {"apple": 5})

    def test_remove_item_not_found(self):
        """Тест удаления несуществующего товара."""
        with self.assertRaises(ValueError):
            self.warehouse.remove_item("banana", 5)

    def test_remove_insufficient_quantity(self):
        """Тест удаления большего количества товара, чем есть на складе."""
        self.warehouse.add_item("apple", 10)
        with self.assertRaises(ValueError):
            self.warehouse.remove_item("apple", 15)

if __name__ == "__main__":
    unittest.main()
