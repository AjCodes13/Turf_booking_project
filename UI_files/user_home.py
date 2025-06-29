from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
import sys
import os
import mysql.connector
from dotenv import load_dotenv

from UI_files.book_slot import BookSlot  # Updated: expects user_name argument

load_dotenv()  # Load credentials from .env file

class UserHome(QWidget):
    def __init__(self, user_name):
        super().__init__()
        self.setWindowTitle("User Home")
        self.setFixedSize(500, 650)
        self.user_name = user_name

        layout = QVBoxLayout()

        self.welcome_label = QLabel("Welcome User")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setObjectName("welcome_label")

        self.name_label = QLabel(f"User: {self.user_name}")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setObjectName("name_label")

        layout.addWidget(self.welcome_label)
        layout.addWidget(self.name_label)

        self.city_dropdown = QComboBox()
        self.city_dropdown.addItem("-- Select City --")
        self.city_dropdown.currentIndexChanged.connect(self.load_grounds)

        self.ground_dropdown = QComboBox()
        self.ground_dropdown.addItem("-- Select Ground --")
        self.ground_dropdown.currentIndexChanged.connect(self.show_ground_details)

        self.details_box = QTextEdit()
        self.details_box.setReadOnly(True)

        self.book_btn = QPushButton("Book Slot")
        self.book_btn.setEnabled(False)
        self.book_btn.clicked.connect(self.go_to_booking)

        self.back_btn = QPushButton("Go Back")
        self.back_btn.clicked.connect(self.go_back)

        layout.addWidget(QLabel("Select City:"))
        layout.addWidget(self.city_dropdown)
        layout.addWidget(QLabel("Select Ground:"))
        layout.addWidget(self.ground_dropdown)
        layout.addWidget(QLabel("Ground Details & Feedback:"))
        layout.addWidget(self.details_box)
        layout.addWidget(self.book_btn)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: Segoe UI, sans-serif;
            }
            QLabel#welcome_label {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel#name_label {
                font-size: 18px;
                color: #34495e;
            }
            QLabel {
                font-size: 14px;
                margin-top: 10px;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QTextEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QPushButton {
                padding: 10px;
                border-radius: 6px;
                font-size: 14px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: white;
            }
            QPushButton:hover {
                background-color: #2e86de;
            }
        """)

        self.load_cities()

    def load_cities(self):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            cursor = conn.cursor()
            cursor.execute("SELECT city_name FROM cities")
            cities = cursor.fetchall()
            for city in cities:
                self.city_dropdown.addItem(city[0])
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Could not load cities:\n{err}")

    def load_grounds(self):
        self.ground_dropdown.clear()
        self.ground_dropdown.addItem("-- Select Ground --")
        self.details_box.clear()
        self.book_btn.setEnabled(False)

        city_name = self.city_dropdown.currentText()
        if city_name == "-- Select City --":
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
                SELECT ground_name FROM grounds
                JOIN cities ON grounds.city_id = cities.city_id
                WHERE cities.city_name = %s
            """, (city_name,))
            grounds = cursor.fetchall()
            for ground in grounds:
                self.ground_dropdown.addItem(ground[0])
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Could not load grounds:\n{err}")

    def show_ground_details(self):
        ground_name = self.ground_dropdown.currentText()
        if ground_name == "-- Select Ground --":
            self.details_box.clear()
            self.book_btn.setEnabled(False)
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
                SELECT g.ground_name, c.city_name, g.status, g.capacity, g.price
                FROM grounds g
                JOIN cities c ON g.city_id = c.city_id
                WHERE g.ground_name = %s
            """, (ground_name,))
            ground_data = cursor.fetchone()

            cursor.execute("""
                SELECT u.name, f.comment, f.rating
                FROM feedback f
                JOIN grounds g ON f.ground_id = g.ground_id
                JOIN users u ON f.user_id = u.user_id
                WHERE g.ground_name = %s
            """, (ground_name,))
            feedbacks = cursor.fetchall()

            if ground_data:
                status = ground_data[2].lower()
                can_book = status == 'available'

                details = (
                    f"<b>Ground Name:</b> {ground_data[0]}<br>"
                    f"<b>City:</b> {ground_data[1]}<br>"
                    f"<b>Status:</b> {ground_data[2]}<br>"
                    f"<b>Capacity:</b> {ground_data[3]}<br>"
                    f"<b>Price/hour:</b> ₹{ground_data[4]}<br><br>"
                )

                if not can_book:
                    details += (
                        "<span style='color:red; font-weight:bold;'>"
                        "This ground is currently unavailable and cannot be booked."
                        "</span><br><br>"
                    )

                details += "<b>Feedbacks:</b><br>"
                if feedbacks:
                    for fb in feedbacks:
                        details += f"&bull; <i>{fb[0]}</i> ({fb[2]}/5): {fb[1]}<br>"
                else:
                    details += "No feedback yet."

                self.book_btn.setEnabled(can_book)
            else:
                details = "Ground details not found."
                self.book_btn.setEnabled(False)

            self.details_box.setHtml(details)
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Could not load details:\n{err}")
            self.book_btn.setEnabled(False)

    def go_to_booking(self):
        ground_name = self.ground_dropdown.currentText()
        if ground_name and ground_name != "-- Select Ground --":
            self.book_slot_window = BookSlot(ground_name, self.user_name, user_home_callback=self.show_user_home)
            self.book_slot_window.show()
            self.close()

    def show_user_home(self):
        self.show()

    def go_back(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
