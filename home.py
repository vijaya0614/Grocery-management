import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QSize
from functools import partial
from inventory import InventoryWindow  # No circular import here
from login import LoginWindow

class HomePageWindow(QWidget):
    def __init__(self, user_email):
        super().__init__()
        self.setWindowIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\41965FDAB3CB2BD0FDC4536D321AD4FC\WhatsApp Image 2025-05-20 at 12.04.02_ce1bf6ab.jpg"))
        self.user_email = user_email
        self.user_file = f"user_data_{self.user_email}.json"
        self.setWindowTitle("Smart Grocery Manager - Home")
        self.setMinimumSize(1000, 600)
        self.showMaximized()
        self.set_theme()
        self.create_layout()

    def set_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

    def create_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Top bar with logout button
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setAlignment(Qt.AlignRight)
        logout_button = QPushButton("Logout")
        logout_button.setFixedSize(100, 40)
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e85a5a;
            }
        """)
        logout_button.clicked.connect(self.logout)
        top_bar.addWidget(logout_button)
        main_layout.addLayout(top_bar)

        # Welcome text
        subtitle = QLabel(f"Hello {self.user_email.title()}, Welcome to Smart Grocery Manager!")
        subtitle.setFont(QFont("Segoe UI", 40, QFont.Bold))
        subtitle.setStyleSheet("color: #53AAB8;")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(5)

        self.add_feature_buttons(main_layout)

        bottom_spacer = QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(bottom_spacer)

        self.setLayout(main_layout)


    def add_feature_buttons(self, layout):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)
        grid_layout.setAlignment(Qt.AlignCenter)

        features = [
            ("    Inventory\n  Management", r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\41965FDAB3CB2BD0FDC4536D321AD4FC\WhatsApp Image 2025-05-20 at 12.04.02_a13bb3fa.jpg", "inventory", "InventoryWindow"),
            ("    Receipe\n  Generator", r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\FC50322932B29B26CFC46FD9A91EC474\WhatsApp Image 2025-05-20 at 12.04.03_ee1f3313.jpg", "receipe", "RecipeGeneratorWindow"),
            (" Shopping List\n    Manager", r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\1FC8C3D03B0021478A8C9EBDCD457C67\WhatsApp Image 2025-05-20 at 12.04.02_e4419ea8.jpg", "shopping", "ShoppingListWindow"),
            ("   Budget\n   Tracker", r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\F1A706591E15F81814FAC5184B29E7B5\WhatsApp Image 2025-05-20 at 12.04.03_782affa4.jpg", "budget", "BudgetTrackerWindow"),
            ("     Nutrient\n   Companion", r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\1C6E02B62A98D8D9341A81521EDD3426\WhatsApp Image 2025-05-20 at 12.12.57_b775e7cb.jpg","nutrition","NutritionWindow"),
            ("   Ingredient\n   Substitute", r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\E476163101FF7CC61670AEC5DCE3991C\WhatsApp Image 2025-05-20 at 12.15.38_7b198891.jpg","substitution","SubstitutionWindow")
        ]
        row = col = 0
        for label, icon_path, module_name, class_name in features:
            btn = QPushButton(label)
            btn.setFixedSize(280, 200)
            btn.setFont(QFont("Arial", 10))
            btn.setStyleSheet("""
                QPushButton {
                    border: 3px solid #53AAB8;
                    border-radius: 30px;
                    background-color: white;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background-color: #d3e6f1;
                    border: 6px solid #53AAB8;
                }
            """)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(120, 120))

            if module_name == "inventory":
                btn.clicked.connect(partial(self.launch_inventory_window, self.user_email))
            else:
                btn.clicked.connect(partial(self.launch_feature_window, module_name, class_name))

            grid_layout.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        layout.addLayout(grid_layout)

    def launch_inventory_window(self, user_email):
        self.inventory_window = InventoryWindow(user_email)
        self.inventory_window.showMaximized()
        self.close()

    def launch_feature_window(self, module_name, class_name):
        print(f"Launching {class_name} from {module_name}...")
        try:
            module = __import__(module_name)
            WinClass = getattr(module, class_name)
            self.win = WinClass(user_email=self.user_email)
            self.win.showMaximized()
            self.close()
        except Exception as e:
            print(f"Error launching {class_name} from {module_name}: {e}")
    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.showMaximized()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePageWindow("testuser@example.com")
    window.showMaximized()
    sys.exit(app.exec_())
