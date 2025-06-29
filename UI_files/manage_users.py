import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QDialog, QHBoxLayout,
    QMessageBox, QFormLayout, QDialogButtonBox, QComboBox
)
from PyQt5.QtCore import Qt
import mysql.connector

class UserDetailsDialog(QDialog):
    def __init__(self, user_data, parent=None, reload_users_callback=None):
        super().__init__(parent)
        self.setWindowTitle("User Details")
        self.setFixedSize(300, 300)
        self.user_data = user_data
        self.reload_users_callback = reload_users_callback

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Name: {user_data['name']}"))
        layout.addWidget(QLabel(f"Email: {user_data['email']}"))
        layout.addWidget(QLabel(f"Phone: {user_data['phone']}"))
        layout.addWidget(QLabel(f"Role: {user_data['role']}"))

        btn_layout = QHBoxLayout()
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")
        close_btn = QPushButton("Close")

        edit_btn.clicked.connect(self.edit_user)
        delete_btn.clicked.connect(self.delete_user)
        close_btn.clicked.connect(self.close)

        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)
        layout.addWidget(close_btn)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f7fa;
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #2c3e50;
                padding: 4px;
            }
            QPushButton {
                padding: 8px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QDialog {
                background-color: #fdfdfd;
            }
            QMessageBox {
                background-color: white;
            }
        """)

    def edit_user(self):
        dialog = EditUserDialog(self.user_data, self)
        if dialog.exec_():
            if self.reload_users_callback:
                self.reload_users_callback()
            self.close()

    def delete_user(self):
        confirm = QMessageBox.question(self, "Confirm Delete",
                                       f"Are you sure you want to delete {self.user_data['name']}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="AjIsj1316",
                    database="dbs_proj"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE user_id = %s", (self.user_data['user_id'],))
                conn.commit()
                cursor.close()
                conn.close()
                QMessageBox.information(self, "Deleted", "User deleted successfully.")
                if self.reload_users_callback:
                    self.reload_users_callback()
                self.close()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Database Error", f"Delete failed:\n{err}")


class EditUserDialog(QDialog):
    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit User")
        self.setFixedSize(300, 300)
        self.user_data = user_data

        layout = QFormLayout()

        self.name_input = QLineEdit(user_data['name'])
        self.email_input = QLineEdit(user_data['email'])
        self.phone_input = QLineEdit(user_data['phone'])
        self.role_input = QComboBox()
        self.role_input.addItems(["user", "admin"])
        self.role_input.setCurrentText(user_data['role'])

        layout.addRow("Name:", self.name_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Phone:", self.phone_input)
        layout.addRow("Role:", self.role_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save_changes)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f7fa;
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #2c3e50;
                padding: 4px;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 8px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QDialog {
                background-color: #fdfdfd;
            }
            QMessageBox {
                background-color: white;
            }
        """)

    def save_changes(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        role = self.role_input.currentText()

        # Basic validation
        if not name or not email or not phone or not role:
            QMessageBox.warning(self, "Validation Error", "All fields are required.")
            return

        # Email validation (simple regex)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.warning(self, "Validation Error", "Invalid email format.")
            return

        # Phone validation: digits only and length check
        if not phone.isdigit() or len(phone) < 7:
            QMessageBox.warning(self, "Validation Error", "Invalid phone number.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="AjIsj1316",
                database="dbs_proj"
            )
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users
                SET name=%s, email=%s, phone_no=%s, role=%s
                WHERE user_id=%s
            """, (
                name,
                email,
                phone,
                role,
                self.user_data['user_id']
            ))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "User updated successfully.")
            self.accept()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Update failed:\n{err}")


class ManageUsers(QWidget):
    def __init__(self, admin_name="", previous_window=None):
        super().__init__()
        self.setWindowTitle("Manage Users")
        self.setFixedSize(400, 500)
        self.admin_name = admin_name
        self.previous_window = previous_window

        layout = QVBoxLayout()

        title = QLabel("User Management")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search user by name...")
        self.search_input.textChanged.connect(self.search_users)

        self.user_list = QListWidget()
        self.user_list.itemClicked.connect(self.select_user)

        back_btn = QPushButton("Go Back")
        back_btn.clicked.connect(self.go_back)

        layout.addWidget(title)
        layout.addWidget(self.search_input)
        layout.addWidget(self.user_list)
        layout.addWidget(back_btn)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f7fa;
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }

            QLabel {
                color: #2c3e50;
                padding: 4px;
            }

            QLabel#title {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }

            QLineEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }

            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 4px;
            }

            QPushButton {
                padding: 8px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QMessageBox {
                background-color: white;
            }
        """)

        self.load_all_users()

    def load_all_users(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="AjIsj1316",
                database="dbs_proj"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name FROM users ORDER BY name")
            result = cursor.fetchall()

            # Save as list of dicts for convenience
            self.users = [{"user_id": r[0], "name": r[1]} for r in result]
            self.user_list.clear()
            self.user_list.addItems([u['name'] for u in self.users])

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Failed to load users:\n{err}")
            self.users = []

    def search_users(self):
        query = self.search_input.text().lower()
        filtered = [u for u in self.users if query in u['name'].lower()]
        self.user_list.clear()
        self.user_list.addItems([u['name'] for u in filtered])

    def select_user(self, item):
        selected_name = item.text()
        # Find user_id from self.users
        user_record = next((u for u in self.users if u['name'] == selected_name), None)
        if not user_record:
            QMessageBox.warning(self, "User Not Found", "Selected user not found in the list.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="AjIsj1316",
                database="dbs_proj"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name, email, phone_no, role FROM users WHERE user_id = %s", (user_record['user_id'],))
            result = cursor.fetchone()

            if result:
                user_data = {
                    "user_id": result[0],
                    "name": result[1],
                    "email": result[2],
                    "phone": result[3],
                    "role": result[4]
                }

                dialog = UserDetailsDialog(user_data, self, reload_users_callback=self.load_all_users)
                dialog.exec_()

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Could not load user details:\n{err}")

    def go_back(self):
        if self.previous_window:
            self.previous_window.show()
        self.close()
