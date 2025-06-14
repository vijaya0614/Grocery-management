import sys
import json
import pyttsx3
import pyperclip
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QHBoxLayout


def load_substitutions():
    with open("substitutions.json", "r") as file:
        return json.load(file)

def get_substitutes(item_name):
    item_name = item_name.lower()
    data = load_substitutions()
    return data.get(item_name, None)

def speak_substitution(substitutes):
    engine = pyttsx3.init()
    text = f"Substitutes: {', '.join(substitutes)}"
    engine.say(text)
    engine.runAndWait()

class SubstitutionWindow(QWidget):
    def __init__(self, user_email=None):
        super().__init__()
        self.setWindowIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\E476163101FF7CC61670AEC5DCE3991C\WhatsApp Image 2025-05-20 at 12.15.39_85462e73.jpg"))
        self.user_email = user_email
        self.setWindowTitle("Ingredient Substitute")
        self.setGeometry(100, 100, 620, 450)

        self.setStyleSheet("background-color: white;")
        self.setMinimumSize(1000,600)
        self.showMaximized()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Shadowed heading
        self.heading = QLabel("Ingredient Substitute ")
        self.heading.setFont(QFont("Arial", 24, QFont.Bold))
        self.heading.setStyleSheet("color: #53AAB8;")
        self.heading.setAlignment(Qt.AlignCenter)


        layout.addWidget(self.heading)

        # Search bar
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a missing ingredient... (e.g., 'egg')")
        self.input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 18px;
                border: 2px solid #53AAB8;
                border-radius: 15px;
                background-color: #f9fcfd;
            }
        """)
        self.input.returnPressed.connect(self.show_substitutes)
        layout.addWidget(self.input)

        # Search button
        self.button = QPushButton("🔍 Find Substitutes")
        self.button.setStyleSheet("""
            QPushButton {
                background:#53AAB8;
                border: none;
                color: white;
                padding: 14px;
                font-size: 18px;
                border-radius: 12px;
                
            }
            QPushButton:hover {
                background-color: #4db0c1;
            }
        """)
        self.button.clicked.connect(self.show_substitutes)
        layout.addWidget(self.button)

        # Result list
        self.sub_list = QListWidget()
        self.sub_list.setStyleSheet("""
            QListWidget {
                font-size: 17px;
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid #aaa;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                margin: 6px 0;
                border-radius: 8px;
                background: #e8f6f9;
            }
            QListWidget::item:selected {
                background-color: #53AAB8;
                color: white;
            }
        """)
        self.sub_list.itemClicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.sub_list)
                # Back to Homepage button
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 20, 0, 20)  # Top, Right, Bottom, Left margins

        # Back arrow icon button
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(r"c:\Users\VIJAYASREE\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\3152E3B1E52E2CB123363787D5F76C95\WhatsApp Image 2025-05-20 at 12.15.56_ef90f3ac.jpg"))  # Your arrow image
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
        self.back_button.clicked.connect(self.back_to_homepage)

        bottom_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Add this bottom layout to your main layout (at the end)
        layout.addLayout(bottom_layout)



        self.setLayout(layout)

    def show_substitutes(self):
        ingredient = self.input.text().strip()
        self.sub_list.clear()
        if ingredient:
            subs = get_substitutes(ingredient)
            if subs:
                formatted = [f"💡 {s}" for s in subs]
                for sub in formatted:
                    item = QListWidgetItem(sub)
                    self.sub_list.addItem(item)
                speak_substitution(subs)
            else:
                self.sub_list.addItem(f"❌ No known substitute for '{ingredient}'")
                speak_substitution([f"No known substitute for {ingredient}"])
        else:
            self.sub_list.addItem("⚠️ Please enter an ingredient.")
            speak_substitution(["Please enter an ingredient."])

    def copy_to_clipboard(self, item):
        cleaned = item.text().replace("💡 ", "")
        pyperclip.copy(cleaned)
        speak_substitution([f"{cleaned} copied to clipboard."])
    def back_to_homepage(self):
        try:
            from home import HomePageWindow  # Delayed import to avoid circular issue
            self.home = HomePageWindow(self.user_email)
            self.home.showMaximized()
            self.close()
        except Exception as e:
            print(f"Error returning to homepage: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubstitutionWindow("testuser@example.com")
    window.show()
    sys.exit(app.exec_())
