import os
import random
import mysql.connector
from datetime import datetime
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QRadioButton, QButtonGroup, QMessageBox
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

class PaymentPage(QMainWindow):
    def __init__(self, ground_id, slot_id, amount, user_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slot_id = int(slot_id)        # Ensure int type early
        self.ground_id = ground_id
        self.amount = float(amount)        # Ensure float type early
        self.user_name = user_name

        self.setWindowTitle("Payment")
        self.setFixedSize(400, 320)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("💳 Select Payment Mode")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2C3E50;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.radio_group = QButtonGroup(self)
        self.radio_buttons = []

        for mode in ["Credit Card", "UPI", "Net Banking", "Cash"]:
            btn = QRadioButton(mode)
            btn.setStyleSheet("""
                QRadioButton {
                    font-size: 15px;
                    padding: 5px;
                }
            """)
            self.radio_group.addButton(btn)
            self.radio_buttons.append(btn)
            layout.addWidget(btn)

        self.amount_label = QLabel(f"💰 Amount to be Paid: ₹{self.amount:.2f}")
        self.amount_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1A5276;
        """)
        self.amount_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.amount_label)

        pay_button = QPushButton("Proceed to Pay")
        pay_button.setStyleSheet("""
            QPushButton {
                background-color: #28B463;
                color: white;
                font-size: 15px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #239B56;
            }
        """)
        pay_button.clicked.connect(self.process_payment)
        layout.addWidget(pay_button, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #F8F9F9;")
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def process_payment(self):
        from invoice_page import InvoicePage  # Import locally to avoid circular imports if any

        selected_button = self.radio_group.checkedButton()
        if selected_button is None:
            QMessageBox.warning(self, "Payment Error", "Please select a payment mode.")
            return

        selected = selected_button.text()
        transaction_id = random.randint(10000000, 99999999)
        invoice_id = random.randint(100000, 999999)
        payment_date = datetime.now().strftime('%Y-%m-%d')

        payment_id = None
        conn = None
        cursor = None

        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME
            )
            cursor = conn.cursor()

            # Insert payment record
            cursor.execute("""
                INSERT INTO Payments (slot_id, amount_paid, P_mode, payment_date)
                VALUES (%s, %s, %s, %s)
            """, (self.slot_id, self.amount, selected, payment_date))
            conn.commit()

            payment_id = cursor.lastrowid

            # Update slot availability
            cursor.execute("""
                UPDATE Slot_Available
                SET availability = 'booked'
                WHERE slot_id = %s
            """, (self.slot_id,))
            conn.commit()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"An error occurred:\n{err}")
            return

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        self.close()

        # Show invoice page
        self.invoice_page = InvoicePage(
            transaction_id, selected, self.amount, invoice_id, payment_date, payment_id, self.user_name
        )
        self.invoice_page.show()

