"""Inventory management system with logging and input validation:)"""
import json
import logging
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# Global variable
stock_data = {}


def add_item(item=None, qty=0, logs=None):
    """
    Add an item to stock inventory.

    Args:
        item: Item name (str)
        qty: Quantity to add (int)
        logs: Optional list to store log messages
    """
    if logs is None:
        logs = []

    # Input validation
    if not item or not isinstance(item, str):
        logger.warning("Invalid item name provided")
        return

    if not isinstance(qty, int):
        logger.warning("Invalid quantity type for %s: expected int, got %s",
                       item, type(qty).__name__)
        return

    if qty < 0:
        logger.warning("Cannot add negative quantity for %s", item)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    logger.info(log_message)


def remove_item(item, qty):
    """
    Remove an item from stock inventory.

    Args:
        item: Item name (str)
        qty: Quantity to remove (int)
    """
    # Input validation
    if not isinstance(item, str):
        logger.error("Invalid item type: expected str, got %s",
                     type(item).__name__)
        return

    if not isinstance(qty, (int, float)) or qty < 0:
        logger.error("Invalid quantity: %s", qty)
        return

    try:
        if item not in stock_data:
            raise KeyError(f"Item '{item}' not found in inventory")

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
        logger.info("Removed %s of %s", qty, item)
    except KeyError as e:
        logger.error("Error removing item: %s", e)


def get_qty(item):
    """
    Get quantity of an item in stock.

    Args:
        item: Item name (str)

    Returns:
        int: Quantity of item, or 0 if not found
    """
    if not isinstance(item, str):
        logger.error("Invalid item type: expected str, got %s",
                     type(item).__name__)
        return 0

    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from JSON file.

    Args:
        file: Path to JSON file
    """
    global stock_data  # pylint: disable=global-statement
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logger.info("Data loaded from %s", file)
    except FileNotFoundError:
        logger.warning("File %s not found, starting with empty inventory", file)
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in %s: %s", file, e)


def save_data(file="inventory.json"):
    """
    Save inventory data to JSON file.

    Args:
        file: Path to JSON file
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
        logger.info("Data saved to %s", file)
    except IOError as e:
        logger.error("Error saving data: %s", e)


def print_data():
    """Print inventory report."""
    print("Items Report")
    print("-" * 30)
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """
    Check for items below threshold.

    Args:
        threshold: Minimum quantity threshold (int)

    Returns:
        list: Items below threshold
    """
    if not isinstance(threshold, (int, float)) or threshold < 0:
        logger.warning("Invalid threshold: %s, using default 5", threshold)
        threshold = 5

    result = []
    for item, qty in stock_data.items():
        if qty < threshold:
            result.append(item)
    return result


def main():
    """Main execution function."""
    logger.info("Starting inventory system")

    add_item("apple", 10)
    add_item("banana", 5)
    # These will be rejected with warnings
    add_item(123, "ten")  # invalid types
    add_item("orange", -2)  # negative quantity

    remove_item("apple", 3)
    remove_item("orange", 1)  # will log error - item not found

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    save_data()
    load_data()
    print_data()

    # Removed eval() call
    logger.info("Inventory system completed successfully")


if __name__ == "__main__":
    main()
