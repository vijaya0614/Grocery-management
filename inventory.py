import sys
import json
import os
from PyQt5.QtWidgets import (
QApplication, QWidget, QVBoxLayout, QHBoxLayout,
QLabel, QLineEdit, QPushButton, QTableWidget,
QTableWidgetItem, QMessageBox, QAbstractItemView, QSizePolicy
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QHBoxLayout

class InventoryWindow(QWidget):

    def __init__(self, username):
        super().__init__()        
        self.is_updating = False
        self.update_row_index = None
        self.setWindowIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\41965FDAB3CB2BD0FDC4536D321AD4FC\WhatsApp Image 2025-05-20 at 12.04.02_78b18849.jpg"))
        self.username = username  # 👈 Store the current user's name
        self.inventory_file = f"inventory_{self.username}.json"  # 👈 Unique file per user
        self.shopping_list_file = f"shoppinglist_{self.username}.json"
        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 1000, 600)
        self.setMinimumSize(1000, 600)
        self.showMaximized()

        self.setup_ui()
        self.load_inventory()

    def go_back_home(self):
        from home import HomePageWindow
        self.home = HomePageWindow(self.username)  # 👈 Pass username back if needed
        self.home.showMaximized()
        self.close()

    def setup_ui(self):
        self.setStyleSheet("background-color: white;")

        heading = QLabel("Inventory Management")
        heading.setStyleSheet("font-size: 60px; font-weight: bold; color: #53AAB8;")
        heading.setAlignment(Qt.AlignCenter)

        input_style = """
        QLineEdit {
            background-color: white;
            border: 2px solid #53AAB8;
            border-radius: 30px;
            padding: 10px 10px;
            min-height: 50px;
            font-size: 20px;
        }
        """

        self.name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.category_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.expiry_date = QLineEdit()

        for field in [self.name_input, self.quantity_input, self.category_input, self.amount_input, self.expiry_date]:
            field.setStyleSheet(input_style)

        form_layout = QVBoxLayout()

        def add_form_row(label_text, widget):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 20px;")
            form_layout.addWidget(label)
            form_layout.addWidget(widget)

        add_form_row("Item Name", self.name_input)
        add_form_row("Quantity", self.quantity_input)
        add_form_row("Category", self.category_input)
        add_form_row("Amount", self.amount_input)
        add_form_row("Expiry Date (dd-mm-yyyy)", self.expiry_date)

        button_layout = QHBoxLayout()
        button_names = [("Add", self.add_item), ("Update", self.update_item),
                        ("Delete", self.delete_item), ("Check Expiry", self.check_expiry)]

        for name, handler in button_names:
            btn = QPushButton(name)
            btn.clicked.connect(handler)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #53AAB8;
                    color: white;
                    font-size: 18px;
                    border-radius: 20px;
                    padding: 10px 20px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #3B8A98;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button_layout.addWidget(btn)

        # Back Button Layout
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(30, 10, 30, 20)
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\3152E3B1E52E2CB123363787D5F76C95\WhatsApp Image 2025-05-20 at 12.15.55_66d143d4.jpg"))
        self.back_button.setIconSize(QSize(36, 36))
        self.back_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: white;
            }
        """)
        self.back_button.clicked.connect(self.go_back_home)
        bottom_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Left Panel
        left_panel = QVBoxLayout()
        content_layout = QVBoxLayout()
        content_layout.addWidget(heading)
        content_layout.addSpacing(40)
        content_layout.addLayout(form_layout)
        content_layout.addSpacing(20)
        content_layout.addLayout(button_layout)
        content_layout.addSpacing(40)

        left_panel.addStretch()
        left_panel.addLayout(content_layout)
        left_panel.addStretch()

        left_widget = QWidget()
        left_widget.setLayout(left_panel)

        # Right Panel - Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Quantity", "Category", "Amount", "Expiry Date"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #53AAB8;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #3B8A98;
                padding: 5px;
            }
        """)
        self.table.setFrameShape(QTableWidget.NoFrame)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #53AAB8;
                border-radius: 10px;
                background-color: #F9F9F9;
                gridline-color: #CCCCCC;
            }
            QHeaderView::section {
                background-color: #53AAB8;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 8px;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
                font-size: 14px;
            }
        """)

        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setWordWrap(True)
        self.table.setSortingEnabled(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultSectionSize(170)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(30, 20, 40, 40)
        right_layout.setSpacing(0)
        right_layout.addWidget(self.table)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # Main Horizontal Layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(40, 20, 20, 20)
        main_layout.setSpacing(0)
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 1)

        # Final Layout
        outer_layout = QVBoxLayout()
        outer_layout.addLayout(main_layout)
        #outer_layout.addStretch()
        outer_layout.addLayout(bottom_layout)
        self.setLayout(outer_layout)


    def get_item_data(self):
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        category = self.category_input.text().strip()
        amount = self.amount_input.text().strip()
        expiry_date = self.expiry_date.text().strip()

        if not name or not quantity or not category or not amount or not expiry_date:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return None

        return {
            "name": name,
            "quantity": quantity,
            "category": category,
            "amount": amount,
            "expiry_date": expiry_date
        }

    def clear_inputs(self):
        self.name_input.clear()
        self.quantity_input.clear()
        self.category_input.clear()
        self.amount_input.clear()
        self.expiry_date.clear()

    def add_item(self):
        item = self.get_item_data()
        if item:
            self.save_to_file(item, mode='add')
            self.load_inventory()
            self.clear_inputs()

    def update_item(self):
        if not self.is_updating:
            # Step 1: Populate fields from selected row
            row = self.table.currentRow()
            if row == -1:
                QMessageBox.warning(self, "No Selection", "Please select a row to update.")
                return

            self.update_row_index = row
            self.is_updating = True

            # Fill input fields from selected row
            self.name_input.setText(self.table.item(row, 0).text())
            self.quantity_input.setText(self.table.item(row, 1).text())
            self.category_input.setText(self.table.item(row, 2).text())
            self.amount_input.setText(self.table.item(row, 3).text())
            self.expiry_date.setText(self.table.item(row, 4).text())

            QMessageBox.information(self, "Edit Mode", "Now modify the fields and click 'Update' again to save changes.")
        else:
            # Step 2: Save changes to selected row
            updated_item = self.get_item_data()
            if updated_item is None:
                return

            inventory = self.load_from_file()
            if 0 <= self.update_row_index < len(inventory):
                inventory[self.update_row_index] = updated_item
                self.save_to_file(inventory, mode='overwrite')
                self.load_inventory()
                self.clear_inputs()
                self.is_updating = False
                self.update_row_index = None
                QMessageBox.information(self, "Success", "Item updated successfully.")
            else:
                QMessageBox.warning(self, "Error", "Invalid row index selected.")




    def delete_item(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return

        inventory = self.load_from_file()
        deleted_item = inventory.pop(row)

        # Add to shopping list
        self.add_to_shopping_list(deleted_item)

        self.save_to_file(inventory, mode='overwrite')
        self.load_inventory()


    def check_expiry(self):
        inventory = self.load_from_file()
        today = QDate.currentDate()
        alerts = []
        for item in inventory:
            try:
                expiry = QDate.fromString(item['expiry_date'], "dd-MM-yyyy")
                if expiry < today:
                    alerts.append(f"{item['name']} has expired!")
                    self.add_to_shopping_list(item)
                else:
                    days_left = today.daysTo(expiry)
                    if 0 <= days_left <= 3:
                        alerts.append(f"{item['name']} expires in {days_left} day(s)")
            except:
                continue

        if alerts:
            QMessageBox.warning(self, "Expiry Alert", "\n".join(alerts))
        else:
            QMessageBox.information(self, "All Good", "No items expiring soon!")

    def load_inventory(self):
        self.auto_check_expiry()
        inventory = self.load_from_file()
        self.table.setRowCount(0)
        for item in inventory:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.table.setItem(row, 1, QTableWidgetItem(item['quantity']))
            self.table.setItem(row, 2, QTableWidgetItem(item['category']))
            self.table.setItem(row, 3, QTableWidgetItem(item['amount']))
            self.table.setItem(row, 4, QTableWidgetItem(item['expiry_date']))

    def load_from_file(self):
        try:
            with open(self.inventory_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_to_file(self, data, mode='add'):
        inventory = self.load_from_file() if mode == 'add' else []
        if mode == 'add':
            inventory.append(data)
        else:
            inventory = data
        with open(self.inventory_file, 'w') as f:
            json.dump(inventory, f, indent=4)
    def add_to_shopping_list(self, item):
        try:
            if os.path.exists(self.shopping_list_file):
                with open(self.shopping_list_file, 'r') as f:
                    data = json.load(f)
            else:
                data = []
            # Check for duplicate by item name
            existing_item_names = [i['name'] for i in data]
            if item['name'] not in existing_item_names:
                data.append(item)
                with open(self.shopping_list_file, 'w') as f:
                    json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error adding to shopping list: {e}")

    def auto_check_expiry(self):
        inventory = self.load_from_file()
        today = QDate.currentDate()
        expired_items = []

        for item in inventory:
            try:
                expiry = QDate.fromString(item['expiry_date'], "dd-mm-yyyy")
                if expiry.isValid() and expiry < today:
                    expired_items.append(item)
            except:
                continue

        if expired_items:
            shopping_list_file = f"shoppinglist_{self.username}.json"
            existing_items = []
            try:
                with open(shopping_list_file, 'r') as f:
                    existing_items = json.load(f)
            except:
                pass

            # Avoid duplicates
            existing_item_names = [item['name'] for item in existing_items]
            for item in expired_items:
                if item['name'] not in existing_item_names:
                    existing_items.append(item)

            with open(shopping_list_file, 'w') as f:
                json.dump(existing_items, f, indent=4)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InventoryWindow("[testuser@example.com](mailto:testuser@example.com)")  # Replace with actual username
    window.show()
    sys.exit(app.exec())