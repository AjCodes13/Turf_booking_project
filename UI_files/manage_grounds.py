import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QListWidget, QMessageBox, QLineEdit, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
import mysql.connector

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

class ManageGrounds(QWidget):
    def __init__(self, admin_name=""):
        super().__init__()
        self.setWindowTitle("Manage Grounds")
        self.setFixedSize(450, 650)
        self.admin_name = admin_name
        self.current_ground_name = None  # Track selected ground

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("🏟️ Ground Management")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 24px; color: #2c3e50;")

        self.city_dropdown = QComboBox()
        self.city_dropdown.setStyleSheet("padding: 6px; font-size: 14px;")
        self.city_dropdown.currentIndexChanged.connect(self.load_grounds)

        self.ground_list = QListWidget()
        self.ground_list.setStyleSheet("font-size: 14px; padding: 6px;")
        self.ground_list.itemClicked.connect(self.show_ground_info)

        self.info_label = QLabel("")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 13px; padding: 6px; color: #34495e;")

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Available", "Unavailable", "Maintenance"])
        self.status_combo.setStyleSheet("padding: 6px; font-size: 14px;")

        self.capacity_input = QLineEdit()
        self.capacity_input.setPlaceholderText("Capacity")
        self.capacity_input.setStyleSheet("padding: 6px; font-size: 14px;")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price per hour")
        self.price_input.setStyleSheet("padding: 6px; font-size: 14px;")

        save_btn = QPushButton("💾 Save Changes")
        save_btn.setStyleSheet("padding: 10px; background-color: #27ae60; color: white; font-weight: bold; border-radius: 5px;")
        save_btn.clicked.connect(self.save_changes)

        delete_btn = QPushButton("🗑️ Delete Ground")
        delete_btn.setStyleSheet("padding: 10px; background-color: #c0392b; color: white; font-weight: bold; border-radius: 5px;")
        delete_btn.clicked.connect(self.delete_ground)

        back_btn = QPushButton("🔙 Go Back")
        back_btn.setStyleSheet("padding: 10px; background-color: #7f8c8d; color: white; font-weight: bold; border-radius: 5px;")
        back_btn.clicked.connect(self.go_back)

        layout.addWidget(title)
        layout.addWidget(QLabel("Select City:"))
        layout.addWidget(self.city_dropdown)
        layout.addWidget(QLabel("Available Grounds:"))
        layout.addWidget(self.ground_list)
        layout.addWidget(QLabel("Selected Ground Info:"))
        layout.addWidget(self.info_label)
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_combo)
        layout.addWidget(self.capacity_input)
        layout.addWidget(self.price_input)
        layout.addWidget(save_btn)
        layout.addWidget(delete_btn)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(back_btn)

        self.setLayout(layout)
        self.load_cities()

    def load_cities(self):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            cursor = conn.cursor()
            cursor.execute("SELECT city_name FROM cities")
            cities = cursor.fetchall()
            self.city_dropdown.clear()
            self.city_dropdown.addItem("-- Select City --")
            self.city_dropdown.addItems([city[0] for city in cities])
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Could not load cities:\n{err}")

    def load_grounds(self):
        city_name = self.city_dropdown.currentText()
        self.ground_list.clear()
        if city_name == "-- Select City --":
            return

        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ground_name FROM grounds
                JOIN cities ON grounds.city_id = cities.city_id
                WHERE cities.city_name = %s
            """, (city_name,))
            grounds = cursor.fetchall()
            self.ground_list.addItems([g[0] for g in grounds])
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Could not load grounds:\n{err}")

    def show_ground_info(self, item):
        ground_name = item.text()
        self.current_ground_name = ground_name

        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ground_name, status, capacity, price
                FROM grounds
                WHERE ground_name = %s
            """, (ground_name,))
            ground = cursor.fetchone()
            cursor.close()
            conn.close()

            if ground:
                name, status, capacity, price = ground
                self.info_label.setText(
                    f"<b>Ground:</b> {name}<br>"
                    f"<b>Status:</b> {status}<br>"
                    f"<b>Capacity:</b> {capacity}<br>"
                    f"<b>Price/Hour:</b> ₹{price}"
                )
                index = self.status_combo.findText(status)
                if index != -1:
                    self.status_combo.setCurrentIndex(index)
                self.capacity_input.setText(str(capacity))
                self.price_input.setText(str(price))
            else:
                QMessageBox.warning(self, "Not Found", "Ground details not found.")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Could not fetch ground info:\n{err}")

    def save_changes(self):
        if not self.current_ground_name:
            QMessageBox.warning(self, "No Selection", "Please select a ground first.")
            return

        new_status = self.status_combo.currentText()
        new_capacity = self.capacity_input.text()
        new_price = self.price_input.text()

        if not (new_status and new_capacity and new_price):
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields.")
            return

        try:
            new_capacity_int = int(new_capacity)
            new_price_float = float(new_price)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Capacity and price must be numbers.")
            return

        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE grounds
                SET status = %s, capacity = %s, price = %s
                WHERE ground_name = %s
            """, (new_status, new_capacity_int, new_price_float, self.current_ground_name))
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success", "Ground info updated successfully!")
            self.load_grounds()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Could not update ground:\n{err}")

    def delete_ground(self):
        if not self.current_ground_name:
            QMessageBox.warning(self, "No Selection", "Please select a ground first.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete '{self.current_ground_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                conn = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASS,
                    database=DB_NAME
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM grounds WHERE ground_name = %s", (self.current_ground_name,))
                conn.commit()
                cursor.close()
                conn.close()

                QMessageBox.information(self, "Deleted", "Ground deleted successfully!")
                self.current_ground_name = None
                self.status_combo.setCurrentIndex(0)
                self.capacity_input.clear()
                self.price_input.clear()
                self.info_label.clear()
                self.load_grounds()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Database Error", f"Could not delete ground:\n{err}")

    def go_back(self):
        self.previous_window.show()
        self.close()

