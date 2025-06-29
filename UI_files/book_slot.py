from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt
import mysql.connector
import os
from dotenv import load_dotenv
from UI_files.payment_gateway import PaymentPage

# Load credentials securely
load_dotenv()

class BookSlot(QWidget):
    def __init__(self, ground_name, user_name, user_home_callback=None):
        super().__init__()
        self.setWindowTitle("Book Slot")
        self.setFixedSize(420, 400)
        self.ground_name = ground_name
        self.user_name = user_name
        self.user_home_callback = user_home_callback
        self.slots = []  # Ensure slots is defined

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel(f"📅 Available Slots for '{self.ground_name}'")
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2C3E50;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)

        slot_label = QLabel("🕓 Select Slot:")
        slot_label.setStyleSheet("font-size: 14px; color: #34495E;")

        self.slot_dropdown = QComboBox()
        self.slot_dropdown.setStyleSheet("""
            QComboBox {
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.slot_dropdown.currentIndexChanged.connect(self.show_slot_details)

        self.slot_info_label = QLabel("")
        self.slot_info_label.setWordWrap(True)
        self.slot_info_label.setVisible(False)
        self.slot_info_label.setStyleSheet("""
            font-size: 13px;
            padding: 6px;
            background-color: #F8F9F9;
            border: 1px solid #D5D8DC;
            border-radius: 6px;
        """)

        self.confirm_checkbox = QCheckBox("✅ Proceed to Payment")
        self.confirm_checkbox.setVisible(False)
        self.confirm_checkbox.setStyleSheet("font-size: 13px;")
        self.confirm_checkbox.stateChanged.connect(self.toggle_payment_button)

        self.payment_btn = QPushButton("💳 Payment Gateway")
        self.payment_btn.setEnabled(False)
        self.payment_btn.setVisible(False)
        self.payment_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2ECC71;
            }
        """)
        self.payment_btn.clicked.connect(self.go_to_payment)

        self.back_btn = QPushButton("⬅ Go Back")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #34495E;
                color: white;
                font-size: 13px;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #5D6D7E;
            }
        """)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(slot_label)
        self.layout.addWidget(self.slot_dropdown)
        self.layout.addWidget(self.slot_info_label)
        self.layout.addWidget(self.confirm_checkbox)
        self.layout.addWidget(self.payment_btn)
        self.layout.addWidget(self.back_btn, alignment=Qt.AlignRight)
        self.setLayout(self.layout)

        self.load_available_slots()

    def load_available_slots(self):
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            cursor = conn.cursor()

            cursor.execute("SELECT ground_id, price FROM Grounds WHERE ground_name = %s", (self.ground_name,))
            result = cursor.fetchone()
            if not result:
                QMessageBox.critical(self, "Error", "Ground not found in database.")
                return

            self.ground_id, self.price = result

            cursor.execute("""
                SELECT slot_id, slot_date, start_time, end_time
                FROM Slot_Available
                WHERE ground_id = %s AND availability = 'available'
                ORDER BY slot_date, start_time
            """, (self.ground_id,))
            self.slots = cursor.fetchall()
            self.slot_dropdown.clear()

            if self.slots:
                for slot in self.slots:
                    slot_id, slot_date, start_time, end_time = slot
                    label = f"{slot_date} | {start_time} - {end_time}"
                    self.slot_dropdown.addItem(label, userData=slot)
            else:
                self.slot_dropdown.addItem("No available slots to book")
                self.slot_dropdown.setEnabled(False)
                self.slot_info_label.setText("No available slots to book.")
                self.slot_info_label.setVisible(True)
                self.confirm_checkbox.setVisible(False)
                self.payment_btn.setVisible(False)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error fetching slots:\n{err}")

    def show_slot_details(self):
        index = self.slot_dropdown.currentIndex()
        if index < 0 or not self.slots or index >= len(self.slots):
            return

        slot = self.slot_dropdown.itemData(index)
        if slot:
            slot_id, slot_date, start_time, end_time = slot
            self.slot_info_label.setText(
                f"📆 Slot Date: {slot_date}\n⏰ Start Time: {start_time}\n⏳ End Time: {end_time}"
            )
            self.slot_info_label.setVisible(True)
            self.confirm_checkbox.setVisible(True)
            self.payment_btn.setVisible(True)
        else:
            self.slot_info_label.setText("Invalid slot selected.")
            self.slot_info_label.setVisible(True)
            self.confirm_checkbox.setVisible(False)
            self.payment_btn.setVisible(False)

    def toggle_payment_button(self, state):
        self.payment_btn.setEnabled(state == Qt.Checked)

    def go_to_payment(self):
        index = self.slot_dropdown.currentIndex()
        if index < 0 or not self.slots:
            return

        slot = self.slot_dropdown.itemData(index)
        if not slot:
            return

        slot_id = slot[0]
        self.payment_window = PaymentPage(self.ground_id, slot_id, self.price, self.user_name)
        self.payment_window.show()

    def go_back(self):
        self.close()
        if self.user_home_callback:
            self.user_home_callback()
