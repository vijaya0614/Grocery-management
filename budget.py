import sys
import json
from collections import defaultdict

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QSize

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon


class BudgetTrackerWindow(QWidget):
    def __init__(self, user_email):
        super().__init__()
        self.username = user_email
        self.inventory_file = f"inventory_{self.username}.json"
        self.budget_file = f"budget_{self.username}.json"
        self.budget_amount = self.load_budget_amount()

        self.setWindowTitle("Budget Tracker")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("background-color: white;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        title = QLabel("Budget Tracker")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet("color: #53AAB8;")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        self.total_label = QLabel("Total Spent: ₹0")
        self.total_label.setFont(QFont("Arial", 24))
        self.total_label.setStyleSheet("color: #333333; margin-top: 20px;")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.total_label)

        # Budget input layout
        budget_layout = QHBoxLayout()

        budget_label = QLabel("Enter Total Budget (₹):")
        budget_label.setFont(QFont("Arial", 14))

        self.budget_input = QLineEdit()
        self.budget_input.setFixedWidth(150)
        self.budget_input.setText(str(self.budget_amount))
        self.budget_input.setPlaceholderText("e.g., 5000")
        self.budget_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 2px solid #53AAB8;
                border-radius: 8px;
            }
        """)

        set_budget_btn = QPushButton("Set Budget")
        set_budget_btn.setStyleSheet("""
            QPushButton {
                background-color: #53AAB8;
                color: white;
                border-radius: 8px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #3B8A98;
            }
        """)
        set_budget_btn.clicked.connect(self.handle_set_budget)

        budget_layout.addStretch()
        budget_layout.addWidget(budget_label)
        budget_layout.addWidget(self.budget_input)
        budget_layout.addWidget(set_budget_btn)
        budget_layout.addStretch()

        self.layout.addLayout(budget_layout)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Graph canvas
        self.figure_canvas = FigureCanvas(plt.Figure(figsize=(12, 6)))
        self.figure_canvas.setFixedHeight(500)
        self.layout.addWidget(self.figure_canvas)

        self.load_and_display_data()

        # Back button layout
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 20, 0, 20)

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\3152E3B1E52E2CB123363787D5F76C95\WhatsApp Image 2025-05-20 at 12.15.55_aea7ce2d.jpg"))
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
        self.layout.addLayout(bottom_layout)

    def load_and_display_data(self):
        try:
            with open(self.inventory_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        total = 0
        category_spending = defaultdict(float)

        for item in data:
            try:
                amount = float(item.get("amount", 0))
                category = item.get("category", "Unknown")
                total += amount
                category_spending[category] += amount
            except:
                continue

        self.total_label.setText(f"Total Spent: ₹{total:.2f}")

        # Clean category names
        clean_category_names = {
            "Grains and Grains": "Grains",
            "2 kg": "Grains",
            "5 KG": "Vegetables",
            "Personal care": "Personal Care"
        }
        categories = [clean_category_names.get(cat, cat) for cat in category_spending.keys()]
        amounts = list(category_spending.values())

        # Plotting
        self.figure_canvas.figure.clear()
        ax = self.figure_canvas.figure.add_subplot(111)

        bars = ax.bar(categories, amounts, color="#53AAB8")
        ax.set_title("Spending by Category", fontsize=16)
        ax.set_ylabel("Amount (₹)")
        ax.set_xlabel("Category")
        ax.tick_params(axis='x', rotation=45)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 5, f"₹{yval:.0f}",
                    ha='center', va='bottom', fontsize=10)

        self.figure_canvas.draw()

        # Budget comparison
        if self.budget_amount > 0:
            difference = self.budget_amount - total
            if difference >= 0:
                self.status_label.setText(
                    f"✅ You are ₹{difference:.2f} under your budget of ₹{self.budget_amount:.2f}."
                )
                self.status_label.setStyleSheet("color: green;")
            else:
                self.status_label.setText(
                    f"❌ You have exceeded your budget by ₹{-difference:.2f} (Budget: ₹{self.budget_amount:.2f})."
                )
                self.status_label.setStyleSheet("color: red;")
        else:
            self.status_label.setText("Set your total budget above to track spending!")
            self.status_label.setStyleSheet("color: #333333;")

    def handle_set_budget(self):
        try:
            amount = float(self.budget_input.text())
            self.budget_amount = amount
            self.save_budget_amount(amount)
            self.load_and_display_data()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for budget.")

    def load_budget_amount(self):
        try:
            with open(self.budget_file, 'r') as f:
                return float(json.load(f).get("budget", 0))
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 0

    def save_budget_amount(self, amount):
        with open(self.budget_file, 'w') as f:
            json.dump({"budget": amount}, f)

    def go_back_home(self):
        from home import HomePageWindow
        self.home = HomePageWindow(self.username)
        self.home.showMaximized()
        self.close()


