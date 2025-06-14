import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox,
    QHBoxLayout, QLineEdit, QFileDialog, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from home import HomePageWindow
from fpdf import FPDF
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QHBoxLayout

class ShoppingListWindow(QWidget):
    def __init__(self, user_email):
        super().__init__()
        self.setWindowIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\1FC8C3D03B0021478A8C9EBDCD457C67\WhatsApp Image 2025-05-20 at 12.04.02_964ba44c.jpg"))
        self.user_email = user_email
        self.shopping_file = f"shoppinglist_{self.user_email}.json"
        self.setWindowTitle("Shopping List Manager")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: white;")
        self.setup_ui()
        self.load_shopping_list()

    
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        heading = QLabel("Shopping List Manager")
        heading.setFont(QFont("Arial", 28, QFont.Bold))
        heading.setStyleSheet("color: #53AAB8;")
        heading.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(heading)

        # Split left and right
        center_layout = QHBoxLayout()
        center_layout.setSpacing(30)

        # LEFT PANEL
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("""
            QTextEdit {
                font-size: 25px;
                padding: 10px;
                border: 2px solid #53AAB8;
                border-radius: 15px;
                background-color: #f9f9f9;
            }
        """)
        center_layout.addWidget(self.output_area, 1)

        # RIGHT PANEL
        # RIGHT PANEL
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # --- Container to center these widgets vertically ---
        center_container = QWidget()
        center_vbox = QVBoxLayout(center_container)
        center_vbox.setSpacing(10)  # Minimal space between widgets
        center_vbox.setAlignment(Qt.AlignCenter)

        # Input Field
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("Enter item name...")
        self.item_input.setFixedHeight(65)
        self.item_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 8px;
                border: 2px solid #53AAB8;
                border-radius: 16px;
            }
        """)
        self.item_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        center_vbox.addWidget(self.item_input)

        # Add and Delete buttons (side-by-side)
        buttons_row = QHBoxLayout()
        add_btn = QPushButton("Add")
        delete_btn = QPushButton("Delete")

        for btn in (add_btn, delete_btn):
            btn.setFont(QFont("Arial", 12))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #53AAB8;
                    color: white;
                    border-radius: 18px;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #3B8A98;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setFixedHeight(65)

        buttons_row.addWidget(add_btn)
        buttons_row.addSpacing(10)
        buttons_row.addWidget(delete_btn)
        center_vbox.addLayout(buttons_row)

        # Generate PDF button
        generate_btn = QPushButton("Generate PDF")
        generate_btn.setFont(QFont("Arial", 12))
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #53AAB8;
                color: white;
                border-radius: 15px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #3B8A98;
            }
        """)
        generate_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        generate_btn.setFixedHeight(65)
        center_vbox.addWidget(generate_btn)

        # Center the container vertically in right panel
        right_layout.addStretch()
        right_layout.addWidget(center_container)
        right_layout.addStretch()


        center_layout.addWidget(right_panel, 1)
        main_layout.addLayout(center_layout)

        # Back Button at bottom
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\3152E3B1E52E2CB123363787D5F76C95\WhatsApp Image 2025-05-20 at 12.15.55_c63eff09.jpg"))  # Your arrow image
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
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Add this bottom layout to your main layout (at the end)
        main_layout.addLayout(bottom_layout)

        # Button connections
        add_btn.clicked.connect(self.add_item)
        delete_btn.clicked.connect(self.delete_item)
        generate_btn.clicked.connect(self.generate_pdf)
        self.back_button.clicked.connect(self.go_back_home)

        self.setLayout(main_layout)
        

    def load_shopping_list(self):
        if not os.path.exists(self.shopping_file):
            self.shopping_items = []
        else:
            try:
                with open(self.shopping_file, 'r') as f:
                    self.shopping_items = json.load(f)
            except:
                self.shopping_items = []
        self.display_shopping_items()

    def display_shopping_items(self):
        if not self.shopping_items:
            self.output_area.setText("Your shopping list is empty.")
        else:
            names = [item['name'] for item in self.shopping_items]
            self.output_area.setText("\n".join(names))

    def save_shopping_list(self):
        with open(self.shopping_file, 'w') as f:
            json.dump(self.shopping_items, f, indent=4)

    def add_item(self):
        item_name = self.item_input.text().strip()
        if item_name:
            if any(item['name'].lower() == item_name.lower() for item in self.shopping_items):
                QMessageBox.information(self, "Duplicate Item", "This item is already in the shopping list.")
            else:
                self.shopping_items.append({"name": item_name})
                self.save_shopping_list()
                self.display_shopping_items()
                self.item_input.clear()


    def delete_item(self):
        item_name = self.item_input.text().strip()
        if item_name:
            original_len = len(self.shopping_items)
            # Filter out items where the name matches case-insensitively
            self.shopping_items = [item for item in self.shopping_items if item['name'].lower() != item_name.lower()]
            if len(self.shopping_items) != original_len:
                self.save_shopping_list()
                self.display_shopping_items()
                self.item_input.clear()
            else:
                QMessageBox.information(self, "Info", "Item not found in the list.")

    def generate_pdf(self):
        if not self.shopping_items:
            QMessageBox.information(self, "Info", "Shopping list is empty.")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", f"shopping_list_{self.user_email}.pdf", "PDF Files (*.pdf)")
        if not save_path:
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.set_text_color(40, 70, 90)
        pdf.cell(200, 10, txt="Shopping List", ln=True, align='C')
        pdf.ln(10)

        for i, item in enumerate(self.shopping_items, start=1):
            pdf.cell(200, 10, txt=f"{i}. {item['name']}", ln=True)

        try:
            pdf.output(save_path)
            QMessageBox.information(self, "Success", f"PDF saved at: {save_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save PDF: {str(e)}")

    def go_back_home(self):
        self.home = HomePageWindow(self.user_email)
        self.home.showMaximized()
        self.close()
