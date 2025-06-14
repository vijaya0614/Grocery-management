import sys
import re
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QSpacerItem, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class NutritionWindow(QWidget):
    # your code here

    def __init__(self, user_email=None):
        super().__init__()
        self.setWindowIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\9274EAE5C531194F50BBF029E38F0046\WhatsApp Image 2025-05-20 at 12.04.03_e57f465e.jpg"))
        self.user_email = user_email
        # Load nutrients data from JSON file
        with open('nutrients.json', 'r') as file:
            self.nutrients_data = json.load(file)
            

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Nutrient Companion')
       # self.setMinimumSize(650, 650)
        self.setMinimumSize(1000,600)
        self.showMaximized()

        self.setStyleSheet("background-color: #fdfdfd;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # Welcome Label
        self.welcome_label = QLabel('Nutrient Companion ', self)
        self.welcome_label.setFont(QFont('Georgia', 22, QFont.Bold))
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("""
            color: #53AAB8;
            padding: 15px;
            background-color: #ffffff;
            border-radius: 15px;
           
        """)
        main_layout.addWidget(self.welcome_label)

        # Search Bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText('Enter food items (eg.: Apple, Milk, Rice)...')
        self.search_bar.setFont(QFont('Arial', 14))
        self.search_bar.setStyleSheet("""
            padding: 12px;
            border: 2px solid #53AAB8;
            border-radius: 8px;
            background-color: #ffffff;
        """)
        main_layout.addWidget(self.search_bar)

        # Search Button
        self.search_button = QPushButton('🔍 Analyze Nutrients', self)
        self.search_button.setFont(QFont('Arial', 14, QFont.Bold))
        self.search_button.setStyleSheet("""
            background-color: #53AAB8;
            color: white;
            padding: 12px;
            border-radius: 8px;
            border: none;
        """)
        self.search_button.clicked.connect(self.search_food)
        main_layout.addWidget(self.search_button)

        # Spacer
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # Scroll Area for Output
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")

        # Scroll Area Content
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setSpacing(20)
        self.scroll_content.setLayout(self.scroll_layout)

        # Nutrient Result Label
        self.result_label = QLabel('', self)
        self.result_label.setFont(QFont('Arial', 13))
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("""
            color: #333;
            padding: 15px;
            background-color: #ffffff;
            border-radius: 8px;
            border: 1px solid #ccc;
        """)
        self.scroll_layout.addWidget(self.result_label)

        # Total Nutrients Title
        self.total_label = QLabel('Total Nutrients', self)
        self.total_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setStyleSheet("""
            color: #53AAB8;
            background-color: #f1f1f1;
            padding: 12px;
            border-radius: 10px;
        """)
        self.total_label.hide()
        self.scroll_layout.addWidget(self.total_label)

        # Total Nutrients Value
        self.total_nutrients_label = QLabel('', self)
        self.total_nutrients_label.setFont(QFont('Arial', 13))
        self.total_nutrients_label.setAlignment(Qt.AlignTop)
        self.total_nutrients_label.setWordWrap(True)
        self.total_nutrients_label.setStyleSheet("""
            color: #333;
            background-color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #ccc;
        """)
        self.total_nutrients_label.hide()
        self.scroll_layout.addWidget(self.total_nutrients_label)

        # Comparison Title
        self.comparison_label = QLabel('Comparison with Recommended Intake', self)
        self.comparison_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.comparison_label.setAlignment(Qt.AlignCenter)
        self.comparison_label.setStyleSheet("""
            color: #53AAB8;
            background-color: #f1f1f1;
            padding: 12px;
            border-radius: 10px;
        """)
        self.comparison_label.hide()
        self.scroll_layout.addWidget(self.comparison_label)

        # Comparison Results
        self.comparison_result_label = QLabel('', self)
        self.comparison_result_label.setFont(QFont('Arial', 13))
        self.comparison_result_label.setAlignment(Qt.AlignTop)
        self.comparison_result_label.setWordWrap(True)
        self.comparison_result_label.setStyleSheet("""
            color: #333;
            background-color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #ccc;
        """)
        self.comparison_result_label.hide()
        self.scroll_layout.addWidget(self.comparison_result_label)

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)
                # Back to Homepage Button
        self.back_button = QPushButton(self)
        self.back_button.setIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\3152E3B1E52E2CB123363787D5F76C95\WhatsApp Image 2025-05-20 at 12.15.56_ef90f3ac.jpg"))
        self.back_button.setIconSize(QSize(32, 32))
        self.back_button.setStyleSheet("""
            background-color: white;
            color: #53AAB8;
            padding: 10px;
            border-radius: 8px;
        """)
        self.back_button.clicked.connect(self.go_back_home)
        main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        self.setLayout(main_layout)
        self.show()


   
    def search_food(self):
     food_items = self.search_bar.text().strip().split(',')
     total_calories = total_protein = total_carbs = total_fats = 0
     result_text = ''

     for item in food_items:
        item = item.strip().lower()

        # Extract quantity (default = 1)
        match = re.match(r'(?P<qty>\d*\.?\d+)?\s*(?:[a-zA-Z\s]+of)?\s*(?P<name>[a-zA-Z\s]+)', item)
        if match:
            qty = float(match.group('qty')) if match.group('qty') else 1
            name = match.group('name').strip()

            # Capitalize first letter for consistent dictionary lookup
            name_cap = name.capitalize()

            if name_cap in self.nutrients_data:
                nutrients = self.nutrients_data[name_cap]
                result_text += (
                    f"<b>{qty} {name}</b> ➤ "
                    f"Calories: {nutrients['calories'] * qty:.2f} kcal | "
                    f"Protein: {nutrients['protein'] * qty:.2f} g | "
                    f"Carbs: {nutrients['carbs'] * qty:.2f} g | "
                    f"Fats: {nutrients['fats'] * qty:.2f} g<br><br>"
                )
                total_calories += nutrients['calories'] * qty
                total_protein += nutrients['protein'] * qty
                total_carbs += nutrients['carbs'] * qty
                total_fats += nutrients['fats'] * qty
            else:
                result_text += f"⚠️ <b>{name}</b>: Data not found.<br><br>"
        else:
            result_text += f"⚠️ Invalid input: <b>{item}</b><br><br>"

     self.result_label.setText(result_text)

    # Show total nutrients only after search
     self.total_label.show()
     self.total_nutrients_label.show()
     self.comparison_label.show()
     self.comparison_result_label.show()

     self.total_nutrients_label.setText(
        f"<b>Total Calories:</b> {total_calories:.2f} kcal<br>"
        f"<b>Total Protein:</b> {total_protein:.2f} g<br>"
        f"<b>Total Carbs:</b> {total_carbs:.2f} g<br>"
        f"<b>Total Fats:</b> {total_fats:.2f} g"
    )

    # Compare with Recommended Intake
     recommended = {'calories': 2000, 'protein': 50, 'carbs': 300, 'fats': 70}
     comparison = ''
     comparison += self.compare_value("Calories", total_calories, recommended['calories'], "kcal")
     comparison += self.compare_value("Protein", total_protein, recommended['protein'], "g")
     comparison += self.compare_value("Carbs", total_carbs, recommended['carbs'], "g")
     comparison += self.compare_value("Fats", total_fats, recommended['fats'], "g")

     self.comparison_result_label.setText(comparison)

    def compare_value(self, name, value, recommended, unit):
        if value >= recommended:
            return f"✅ <b>{name}:</b> {value} {unit} (Sufficient)<br>"
        else:
            diff = recommended - value
            return f"❌ <b>{name}:</b> {value} {unit} (Need {diff} more)<br>"
    def go_back_home(self):
        from home import HomePageWindow
        self.home_window = HomePageWindow(self.user_email)
        self.home_window.showMaximized()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NutritionWindow()   # Use correct class name
    ex.show()
    sys.exit(app.exec_())
