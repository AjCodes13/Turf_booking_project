from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Load DB credentials from .env file

class GroundsBooked(QWidget):
    def __init__(self, admin_name=""):
        super().__init__()
        self.setWindowTitle("Grounds Booked")
        self.setFixedSize(600, 500)
        self.admin_name = admin_name

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        title_label = QLabel("📋 Booked Grounds")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-weight: bold;
            font-size: 24px;
            color: #2E4053;
            margin-bottom: 10px;
        """)
        self.layout.addWidget(title_label)

        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setStyleSheet("""
            background-color: #FBFCFC;
            font-size: 14px;
            padding: 10px;
            border: 1px solid #D5D8DC;
            border-radius: 8px;
        """)
        self.layout.addWidget(self.results_display)

        self.back_btn = QPushButton("⬅ Go Back")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2980B9;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3498DB;
            }
        """)
        self.layout.addWidget(self.back_btn, alignment=Qt.AlignRight)

        self.load_bookings()

    def load_bookings(self):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM BookedGroundsDetails")
            rows = cursor.fetchall()

            if not rows:
                self.results_display.setText("⚠️ No bookings found.")
                return

            display_text = ""
            for row in rows:
                invoice_id, invoice_date, amount_paid, slot_id, ground_name, city_name = row
                display_text += (
                    f"🧾 Invoice ID: {invoice_id}\n"
                    f"📅 Invoice Date: {invoice_date}\n"
                    f"💰 Amount Paid: ₹{amount_paid}\n"
                    f"⏱ Slot ID: {slot_id}\n"
                    f"🏟 Ground: {ground_name}\n"
                    f"🌆 City: {city_name}\n"
                    f"{'-'*45}\n\n"
                )

            self.results_display.setText(display_text)

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error loading bookings:\n{err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def go_back(self):
        try:
            self.previous_window.show()
        except AttributeError:
            QMessageBox.information(self, "Info", "Previous window reference not found.")
        self.close()
