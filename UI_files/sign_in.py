from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
import mysql.connector
import os
import sys
from dotenv import load_dotenv

load_dotenv()  # Load .env file with DB credentials

class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign In")
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QWidget { background-color: #f9f9f9; }
            QLabel#title { font-size: 22px; font-weight: bold; color: #2c3e50; }
            QLineEdit, QComboBox {
                padding: 8px; border: 1px solid #ccc; border-radius: 6px; font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: black; selection-color: red; color: white;
            }
            QPushButton {
                padding: 10px; border-radius: 6px; font-size: 14px;
                background-color: #27ae60; color: white;
            }
            QPushButton:hover { background-color: #1e8449; }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("Sign In Page")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit(placeholderText="Name")
        self.email_input = QLineEdit(placeholderText="Email")
        self.phone_input = QLineEdit(placeholderText="Phone Number")
        self.role_select = QComboBox()
        self.role_select.addItems(["Select Role", "user", "admin"])
        self.pass_input = QLineEdit(placeholderText="Password")
        self.confirm_pass = QLineEdit(placeholderText="Confirm Password")
        self.secret_admin = QLineEdit(placeholderText="Admin Secret (only if Admin)")

        self.pass_input.setEchoMode(QLineEdit.Password)
        self.confirm_pass.setEchoMode(QLineEdit.Password)
        self.secret_admin.setEchoMode(QLineEdit.Password)
        self.secret_admin.hide()

        self.submit_btn = QPushButton("Sign In")
        self.back_btn = QPushButton("Go Back")

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.role_select)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.confirm_pass)
        layout.addWidget(self.secret_admin)
        layout.addWidget(self.submit_btn)
        layout.addWidget(self.back_btn)
        layout.addStretch()

        self.setLayout(layout)

        self.role_select.currentTextChanged.connect(self.toggle_admin_secret)
        self.submit_btn.clicked.connect(self.register_user)
        self.back_btn.clicked.connect(self.go_back)

    def toggle_admin_secret(self, role):
        if role == "admin":
            self.secret_admin.show()
        else:
            self.secret_admin.hide()
            self.secret_admin.clear()

    def register_user(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        role = self.role_select.currentText()
        password = self.pass_input.text()
        confirm = self.confirm_pass.text()
        secret = self.secret_admin.text()

        if role == "Select Role":
            QMessageBox.warning(self, "Input Error", "Please select a valid role.")
            return

        if not all([name, email, phone, password, confirm]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return

        if role == "admin":
            expected_secret = os.getenv("ADMIN_SECRET", "admin123")
            if secret != expected_secret:
                QMessageBox.warning(self, "Auth Error", "Invalid admin secret.")
                return

        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, phone_no, role, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, phone, role, password))
            conn.commit()

            QMessageBox.information(self, "Success", "Registered successfully! Redirecting to login...")
            self.go_back()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Failed to register:\n{err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def go_back(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
