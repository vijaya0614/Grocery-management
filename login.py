import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap,QIcon
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\7F2776F553FE2D5F8BC9A0E0A6D9EC12\WhatsApp Image 2025-05-12 at 07.23.14_1b25a84e.jpg"))
        self.setWindowTitle("Grocery management system-Login & Register System")
        self.setMinimumSize(1000, 600)
        self.create_layout()

    def create_layout(self):
        # Create the main layout and set it
        self.main_layout = QHBoxLayout(self)
        self.create_left_panel()
        self.create_right_panel()
        self.main_layout.addWidget(self.left_panel, 1)
        self.main_layout.addWidget(self.right_panel, 1)

    def create_left_panel(self):
        self.left_panel = QWidget()
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setAlignment(Qt.AlignCenter)

        self.left_panel.setAutoFillBackground(True)
        left_palette = self.left_panel.palette()
        left_palette.setColor(QPalette.Window, QColor("white"))
        self.left_panel.setPalette(left_palette)

        logo_image = QLabel()
        pixmap = QPixmap(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\7F2776F553FE2D5F8BC9A0E0A6D9EC12\WhatsApp Image 2025-05-12 at 07.23.14_1b25a84e.jpg")
        pixmap = pixmap.scaled(380, 380, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_image.setPixmap(pixmap)
        logo_image.setAlignment(Qt.AlignCenter)

        tagline = QLabel("Your Smart Grocery Partner!")
        tagline.setFont(QFont("Arial", 22))
        tagline.setStyleSheet("color: #444444;")
        tagline.setAlignment(Qt.AlignCenter)

        left_layout.addWidget(logo_image)
        left_layout.addWidget(tagline)

    def create_right_panel(self):
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(70, 100, 80, 80)
        self.right_layout.setAlignment(Qt.AlignCenter)

        self.right_panel.setAutoFillBackground(True)
        right_palette = self.right_panel.palette()
        right_palette.setColor(QPalette.Window, QColor("#53AAB8"))
        self.right_panel.setPalette(right_palette)

        self.card = QWidget()
        self.card.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 40px;
        """)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setAlignment(Qt.AlignCenter)
        self.card.setFixedHeight(650)
        self.card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.load_login_form()
        self.right_layout.addStretch()
        self.right_layout.addWidget(self.card)
        self.right_layout.addStretch()

    def load_login_form(self):
        self.clear_card()
        self.card_layout.setAlignment(Qt.AlignCenter)

        heading = QLabel("Login to Your Account")
        heading.setFont(QFont("Arial", 30, QFont.Bold))
        heading.setStyleSheet("font-size: 50px; color: #666666; font-weight: bold;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        for widget in (self.username_input, self.password_input):
            widget.setStyleSheet("""
                QLineEdit {
                    padding: 14px;
                    border: 2px solid #ccc;
                    border-radius: 16px;
                    font-size: 18px;
                }
            """)
            widget.setFixedWidth(500)

        login_btn = QPushButton("Login")
        login_btn.setFixedWidth(500)
        login_btn.setFixedHeight(55)
        login_btn.setStyleSheet(self.button_style())
        login_btn.clicked.connect(self.handle_login)

        signup_label = QLabel("Don't have an account?<a href='#'>Sign up</a>")
        signup_label.setStyleSheet("font-size: 16px; color: #444444;")
        signup_label.setTextFormat(Qt.RichText)
        signup_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        signup_label.setOpenExternalLinks(False)
        signup_label.linkActivated.connect(self.load_signup_form)
        signup_label.setAlignment(Qt.AlignCenter)

        self.card_layout.addWidget(heading)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(login_btn, alignment=Qt.AlignCenter)
        self.card_layout.addSpacing(20)
        self.card_layout.addWidget(signup_label)

    def load_signup_form(self):
        self.clear_card()
        self.card_layout.setAlignment(Qt.AlignCenter)

        heading = QLabel("Create a New Account")
        heading.setFont(QFont("Arial", 30, QFont.Bold))
        heading.setStyleSheet("font-size: 50px; color: #666666; font-weight: bold;")

        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Enter Username")
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Enter Password")
        self.reg_password.setEchoMode(QLineEdit.Password)
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.Password)

        for widget in (self.reg_username, self.reg_password, self.confirm_password):
            widget.setStyleSheet("""
                QLineEdit {
                    padding: 14px;
                    border: 2px solid #ccc;
                    border-radius: 16px;
                    font-size: 18px;
                }
            """)
            widget.setFixedWidth(500)

        register_btn = QPushButton("Register")
        register_btn.setFixedWidth(500)
        register_btn.setFixedHeight(55)
        register_btn.setStyleSheet(self.button_style())
        register_btn.clicked.connect(self.handle_registration)

        back_label = QLabel("<a href='#'>Back to Login</a>")
        back_label.setStyleSheet("font-size: 16px; color: #444444;")
        back_label.setTextFormat(Qt.RichText)
        back_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        back_label.setOpenExternalLinks(False)
        back_label.linkActivated.connect(self.load_login_form)
        back_label.setAlignment(Qt.AlignCenter)

        self.card_layout.addWidget(heading)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(self.reg_username, alignment=Qt.AlignCenter)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(self.reg_password, alignment=Qt.AlignCenter)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(self.confirm_password, alignment=Qt.AlignCenter)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(register_btn, alignment=Qt.AlignCenter)
        self.card_layout.addSpacing(20)
        self.card_layout.addWidget(back_label)

    def handle_registration(self):
        username = self.reg_username.text().strip()
        password = self.reg_password.text()
        confirm = self.confirm_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
        elif password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
        else:
            try:
                with open("users.json", "r") as file:
                    users = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                users = {}

            if username in users:
                QMessageBox.warning(self, "Error", "Username already exists.")
                return

            users[username] = password
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)

            QMessageBox.information(self, "Success", "Registration successful!")
            self.load_login_form()

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}

        if username in users and users[username] == password:
            self.open_homepage(username)  # pass username here
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_homepage(self, user_email):
        from home import HomePageWindow  # Import here to avoid circular imports if any

        # Create a user-specific JSON file if it doesn't exist
        user_file = f"user_data_{user_email}.json"
        if not os.path.exists(user_file):
            with open(user_file, "w") as f:
                json.dump({"username": user_email, "data": {}}, f, indent=4)

        # Pass the username to the HomePageWindow
        self.homepage = HomePageWindow(user_email)
        self.homepage.show()
        self.close()

    def clear_card(self):
        if hasattr(self, 'card_layout'):
            while self.card_layout.count():
                item = self.card_layout.takeAt(0)
                widget =item.widget()
                if widget:
                    widget.deleteLater()
    def button_style(self):
        return """
            QPushButton {
                background-color: #53AAB8;
                color: white;
                border-radius: 15px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66becd;
            }
            QPushButton:pressed {
                background-color: #3d8ca6;
            }
        """
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.showMaximized()
    login_window.show()
    sys.exit(app.exec_())

