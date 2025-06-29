from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
import sys
import mysql.connector
import os
from dotenv import load_dotenv

from UI_files.book_slot import BookSlot
from UI_files.sign_in import SignInWindow
from UI_files.user_home import UserHome
from UI_files.admin_home import AdminHome

load_dotenv()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 450)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton {
                padding: 10px;
                border-radius: 6px;
                font-size: 14px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("Login Page")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Name")

        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Enter Password")

        self.login_btn = QPushButton("Log In")
        self.signin_btn = QPushButton("Sign Up")

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.name_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        layout.addSpacing(20)
        layout.addWidget(QLabel("New user?"))
        layout.addWidget(self.signin_btn)
        layout.addStretch()

        self.setLayout(layout)

        self.login_btn.clicked.connect(self.verify_login)
        self.signin_btn.clicked.connect(self.goto_signin)

    def verify_login(self):
        name = self.name_input.text().strip()
        password = self.pass_input.text().strip()

        if not name or not password:
            QMessageBox.warning(self, "Missing Info", "Please enter both name and password.")
            return

        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")

        try:
            conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE name=%s AND password=%s", (name, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                role = result[0]
                if role == 'user':
                    self.user_home = UserHome(name)
                    self.user_home.show()
                else:
                    self.admin_home = AdminHome(name)
                    self.admin_home.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid credentials.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Could not connect to the database:\n{err}")

    def goto_signin(self):
        self.signin_window = SignInWindow()
        self.signin_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

