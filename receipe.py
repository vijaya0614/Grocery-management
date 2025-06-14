import sys
import json
from PyQt5.QtCore import Qt
import speech_recognition as sr
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QHBoxLayout

class RecipeGeneratorWindow(QWidget):
    def __init__(self, user_email=None):
        super().__init__()
        self.setWindowIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\FC50322932B29B26CFC46FD9A91EC474\WhatsApp Image 2025-05-20 at 12.04.03_ee28e27a.jpg"))
        self.user_email = user_email
        self.setWindowTitle("Recipe Generator")
        self.resize(500, 600)
        self.set_theme()
        self.load_recipes()
        self.init_ui()

    def set_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)

    def load_recipes(self):
        try:
            with open("recipes.json", "r") as f:
                self.recipes = json.load(f)
        except Exception as e:
            self.recipes = {}
            print("Error loading recipes:", e)

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Recipe Generator")
        title.setFont(QFont("Arial", 30, QFont.Bold))
        title.setStyleSheet("color: #53AAB8;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter dish name...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                height: 60px;
                border: 2px solid #53AAB8;
                border-radius: 30px;
                padding-left: 20px;
                font-size: 18px;
            }
            QLineEdit:focus {
                border: 2.5px solid #3c8b97;
            }
        """)
        layout.addWidget(self.input_field)

        buttons_layout = QHBoxLayout()

        search_btn = QPushButton("Search")
        search_btn.setStyleSheet(self.button_style())
        search_btn.clicked.connect(self.handle_text_input)
        buttons_layout.addWidget(search_btn)

        voice_btn = QPushButton("🎤 Voice")
        voice_btn.setStyleSheet(self.button_style())
        voice_btn.clicked.connect(self.handle_voice_input)
        buttons_layout.addWidget(voice_btn)

        layout.addLayout(buttons_layout)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setStyleSheet("""
            QTextEdit {
                font-size: 30px;
                padding: 12px;
                border: 1px solid #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
        """)
        layout.addWidget(self.output_box)

                # Back to Homepage button
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 20, 0, 20)  # Top, Right, Bottom, Left margins

        # Back arrow icon button
        self.back_button = QPushButton()
     #   self.back_button.setIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\3152E3B1E52E2CB123363787D5F76C95\WhatsApp Image 2025-05-20 at 12.15.55_b79206c1.jpg"))  # Your arrow image
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

        # Add this bottom layout to your main layout (at the end)
        layout.addLayout(bottom_layout)



        self.setLayout(layout)
    def button_style(self):
        return """
            QPushButton {
                background-color: #53AAB8;
                color: white;
                border-radius: 30px;
                font-size: 22px;
                font-weight: bold;
                padding: 20px;
                height: 20px;
            }
            QPushButton:hover {
                background-color: #3c8b97;
            }
        """

    def show_recipe(self, dish):
        dish = dish.strip().lower()
        if dish in self.recipes:
            recipe = self.recipes[dish]
            result = f"""
            <h2 style='color: #53AAB8;'>🍽️ Recipe for {dish.title()}</h2>
            <h3 style='color: #3c8b97;'>🧂 Ingredients:</h3>
            <ul>
            {''.join(f"<li>{item}</li>" for item in recipe['ingredients'])}
            </ul>
            <h3 style='color: #3c8b97;'>📋 Procedure:</h3>
            <ol>
            {''.join(f"<li>{step}</li>" for step in recipe['steps'])}
            </ol>
            """
            self.output_box.setHtml(result)
        else:
            self.output_box.setHtml(f"<p style='font-size:16px;'>❓ Sorry, no recipe found for '<b>{dish}</b>'.</p>")

    def handle_text_input(self):
        dish = self.input_field.text()
        if dish:
            self.show_recipe(dish)
        else:
            self.output_box.setText("⚠️ Please enter a recipe name.")

    def handle_voice_input(self):
        recognizer = sr.Recognizer()
        self.output_box.setText("🎧 Listening... Please speak the dish name.")
        QApplication.processEvents()
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5)
                query = recognizer.recognize_google(audio).lower()
                self.input_field.setText(query)
                self.show_recipe(query)
        except sr.UnknownValueError:
            self.output_box.setText("⚠️ Sorry, I couldn't understand your voice.")
        except sr.WaitTimeoutError:
            self.output_box.setText("⌛ Listening timed out. Please try again.")
        except Exception as e:
            self.output_box.setText(f"❌ Error: {str(e)}")

    def go_back_home(self):
        from home import HomePageWindow  # Delayed import
        self.home = HomePageWindow(self.user_email)
        self.home.showMaximized()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RecipeGeneratorWindow("testuser@example.com")
    ex.show()
    sys.exit(app.exec_())
