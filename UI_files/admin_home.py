from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
import sys
import os

from UI_files.manage_users import ManageUsers
from UI_files.manage_grounds import ManageGrounds
from UI_files.payments_invoices import GroundsBooked  # Import the new page

class AdminHome(QWidget):
    def __init__(self, admin_name=""):
        super().__init__()
        self.setWindowTitle("Admin Home")
        self.setFixedSize(400, 400)
        self.admin_name = admin_name or "Admin"

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        welcome_label = QLabel("Welcome Admin")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setObjectName("welcome_label")

        admin_name_label = QLabel(f"Admin Name: {self.admin_name}")
        admin_name_label.setAlignment(Qt.AlignCenter)
        admin_name_label.setObjectName("admin_name_label")

        layout.addWidget(welcome_label)
        layout.addWidget(admin_name_label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        privileges_label = QLabel("Admin Privileges: ")
        privileges_label.setAlignment(Qt.AlignCenter)
        privileges_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        manage_users_btn = QPushButton("Manage Users")
        manage_users_btn.clicked.connect(self.open_manage_users)

        manage_grounds_btn = QPushButton("Manage Grounds")
        manage_grounds_btn.clicked.connect(self.open_manage_grounds)

        booked_grounds_btn = QPushButton("Booked Grounds")
        booked_grounds_btn.clicked.connect(self.open_booked_grounds)

        layout.addWidget(privileges_label)
        layout.addWidget(manage_users_btn)
        layout.addWidget(manage_grounds_btn)
        layout.addWidget(booked_grounds_btn)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.back_btn = QPushButton("Go Back")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)

        # Style
        self.setStyleSheet("""
            QWidget {
                background-color: #eef2f3;
                font-family: Segoe UI, sans-serif;
            }

            QLabel#welcome_label {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }

            QLabel#admin_name_label {
                font-size: 18px;
                color: #34495e;
            }

            QLabel {
                font-size: 14px;
                color: #333;
            }

            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QPushButton:disabled {
                background-color: #bdc3c7;
                color: white;
            }
        """)

    def go_back(self):
        # Warning: this restarts the app
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def open_manage_users(self):
        self.manage_users_window = ManageUsers(admin_name=self.admin_name)
        self.manage_users_window.previous_window = self
        self.manage_users_window.show()
        self.hide()

    def open_manage_grounds(self):
        self.manage_grounds_window = ManageGrounds(admin_name=self.admin_name)
        self.manage_grounds_window.previous_window = self
        self.manage_grounds_window.show()
        self.hide()

    def open_booked_grounds(self):
        self.grounds_booked_window = GroundsBooked(admin_name=self.admin_name)
        self.grounds_booked_window.previous_window = self
        self.grounds_booked_window.show()
        self.hide()
