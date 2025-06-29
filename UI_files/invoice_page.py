from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class InvoicePage(QMainWindow):
    def __init__(self, transaction_id, payment_mode, amount_paid, invoice_id, invoice_date, payment_id, user_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Invoice")
        self.setFixedSize(400, 400)

        self.transaction_id = transaction_id
        self.payment_mode = payment_mode
        self.amount_paid = amount_paid
        self.invoice_id = invoice_id
        self.invoice_date = invoice_date
        self.payment_id = payment_id
        self.user_name = user_name

        self.init_ui()
        self.save_invoice_to_db()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        heading = QLabel("✅ Payment Successful!")
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2ECC71;
            margin-bottom: 20px;
        """)
        layout.addWidget(heading)

        layout.addWidget(self.create_label(f"🧾 Invoice ID: {self.invoice_id}"))
        layout.addWidget(self.create_label(f"💳 Payment Mode: {self.payment_mode}"))
        layout.addWidget(self.create_label(f"🔢 Transaction ID: {self.transaction_id}"))
        layout.addWidget(self.create_label(f"💰 Amount Paid: ₹{self.amount_paid:.2f}"))
        layout.addWidget(self.create_label(f"📅 Invoice Date: {self.invoice_date}"))

        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #5DADE2;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #F4F6F7;
                border: 1px solid #D6DBDF;
                border-radius: 8px;
            }
        """)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_label(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 16px;
            color: #2C3E50;
            padding: 4px;
        """)
        return label

    def save_invoice_to_db(self):
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

            cursor.execute("""
                INSERT INTO Invoice (P_id, invoice_date)
                VALUES (%s, %s)
            """, (self.payment_id, self.invoice_date))
            conn.commit()

        except mysql.connector.Error as err:
            print(f"[ERROR] Saving invoice to DB failed: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
