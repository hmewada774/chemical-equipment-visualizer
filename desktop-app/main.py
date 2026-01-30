import sys
import requests
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, 
                             QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

API_BASE = "http://127.0.0.1:8000/api"

def get_button_style(bg_color="#6366f1", text_color="white"):
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {adjust_color(bg_color, -20)};
        }}
        QPushButton:pressed {{
            background-color: {adjust_color(bg_color, -40)};
        }}
    """

def adjust_color(hex_color, amount):
    # Simple helper to darken color for hover effect
    hex_color = hex_color.lstrip('#')
    r = max(0, min(255, int(hex_color[0:2], 16) + amount))
    g = max(0, min(255, int(hex_color[2:4], 16) + amount))
    b = max(0, min(255, int(hex_color[4:6], 16) + amount))
    return f"#{r:02x}{g:02x}{b:02x}"

class LoginWindow(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        container = QFrame()
        container.setFixedWidth(400)
        container.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("ChemViz Login")
        title.setFont(QFont('Segoe UI', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e293b; border: none;")
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #6366f1;
            }
        """)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #6366f1;
            }
        """)
        
        login_btn = QPushButton("Login to Dashboard")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet(get_button_style())
        login_btn.clicked.connect(self.handle_login)

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()
        
        try:
            resp = requests.post(f"{API_BASE}/login/", json={'username': username, 'password': password})
            if resp.status_code == 200:
                token = resp.json()['access']
                self.switch_callback(token)
            else:
                QMessageBox.warning(self, "Error", "Invalid credentials")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection failed: {str(e)}")

class DashboardWindow(QWidget):
    def __init__(self, token, logout_callback):
        super().__init__()
        self.token = token
        self.logout_callback = logout_callback
        self.initUI()
        self.refresh_data()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # --- Header ---
        nav_layout = QHBoxLayout()
        title = QLabel("ChemViz Dashboard")
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setStyleSheet("color: #1e293b;")
        
        self.status_bar = QLabel("Ready")
        self.status_bar.setStyleSheet("color: #64748b; font-size: 12px; margin-left: 10px;")
        
        upload_btn = QPushButton("Upload CSV")
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.setStyleSheet(get_button_style("#4f46e5"))
        upload_btn.clicked.connect(self.upload_file)
        
        download_btn = QPushButton("Download PDF")
        download_btn.setCursor(Qt.PointingHandCursor)
        download_btn.setStyleSheet(get_button_style("#10b981"))
        download_btn.clicked.connect(self.download_report)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet(get_button_style("#ef4444"))
        logout_btn.clicked.connect(self.logout_callback)
        
        nav_layout.addWidget(title)
        nav_layout.addWidget(self.status_bar)
        nav_layout.addStretch()
        nav_layout.addWidget(upload_btn)
        nav_layout.addWidget(download_btn)
        nav_layout.addWidget(logout_btn)
        
        main_layout.addLayout(nav_layout)
        
        # --- Content ---
        content_layout = QHBoxLayout()
        
        # --- Left Panel ---
        left_panel = QVBoxLayout()
        
        # Stats Group
        stats_group = QGroupBox("Latest Dataset Statistics")
        stats_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        stats_layout = QVBoxLayout()
        
        self.stats_label = QLabel("No data loaded.\nPlease upload a CSV file.")
        self.stats_label.setFont(QFont('Segoe UI', 11))
        self.stats_label.setStyleSheet("color: #334155; padding: 10px;")
        stats_layout.addWidget(self.stats_label)
        stats_group.setLayout(stats_layout)
        left_panel.addWidget(stats_group)
        
        # History Group
        history_group = QGroupBox("Recent Uploads History")
        history_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        history_layout = QVBoxLayout()
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Filename", "Upload Date"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                gridline-color: #f1f5f9;
                font-family: 'Segoe UI';
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 6px;
                border: 1px solid #e2e8f0;
                font-weight: bold;
            }
        """)
        history_layout.addWidget(self.history_table)
        history_group.setLayout(history_layout)
        left_panel.addWidget(history_group)
        
        content_layout.addLayout(left_panel, 1)
        
        # --- Right Panel ---
        right_panel = QVBoxLayout()
        
        charts_group = QGroupBox("Data Visualization")
        charts_group.setFont(QFont('Segoe UI', 10, QFont.Bold))
        charts_layout = QVBoxLayout()
        
        self.bar_figure = plt.figure(figsize=(5, 3))
        self.bar_canvas = FigureCanvas(self.bar_figure)
        charts_layout.addWidget(self.bar_canvas)
        
        self.pie_figure = plt.figure(figsize=(5, 3))
        self.pie_canvas = FigureCanvas(self.pie_figure)
        charts_layout.addWidget(self.pie_canvas)
        
        charts_group.setLayout(charts_layout)
        right_panel.addWidget(charts_group)
        
        content_layout.addLayout(right_panel, 2)
        main_layout.addLayout(content_layout)
        
        self.setLayout(main_layout)

    def get_auth_header(self):
        return {'Authorization': f'Bearer {self.token}'}

    def set_status(self, message):
        self.status_bar.setText(f"Status: {message}")

    def refresh_data(self):
        self.set_status("Fetching data...")
        # Latest Summary
        try:
            resp = requests.get(f"{API_BASE}/summary/", headers=self.get_auth_header())
            if resp.status_code == 200:
                data = resp.json()
                self.update_stats(data)
                self.update_charts(data)
                self.set_status("Data updated successfully.")
            else:
                self.stats_label.setText("No data available.")
                self.set_status("Ready (No data)")
        except:
            self.stats_label.setText("Connection error.")
            self.set_status("Connection Error")

        # History
        try:
            resp = requests.get(f"{API_BASE}/history/", headers=self.get_auth_header())
            if resp.status_code == 200:
                history = resp.json()
                self.history_table.setRowCount(len(history))
                for i, item in enumerate(history):
                    self.history_table.setItem(i, 0, QTableWidgetItem(item['file_name']))
                    date_str = item['uploaded_at'].replace('T', ' ')[:16]
                    self.history_table.setItem(i, 1, QTableWidgetItem(date_str))
        except:
            pass

    def update_stats(self, data):
        # Format with engineering units and html for bolding
        text = (
            f"<b>File:</b> {data['file_name']}<br><br>"
            f"<b>Total Count:</b> {data['total_count']} units<br>"
            f"<b>Avg Flow:</b> {data['avg_flowrate']} m³/h<br>"
            f"<b>Avg Pressure:</b> {data['avg_pressure']} bar<br>"
            f"<b>Avg Temp:</b> {data['avg_temperature']} °C"
        )
        self.stats_label.setText(text)

    def update_charts(self, data):
        # Bar Chart
        self.bar_figure.clear()
        ax = self.bar_figure.add_subplot(111)
        ax.bar(['Flow\n(m³/h)', 'Press\n(bar)', 'Temp\n(°C)'], 
               [data['avg_flowrate'], data['avg_pressure'], data['avg_temperature']], 
               color=['#3b82f6', '#ef4444', '#10b981'])
        ax.set_title('Average Operational Metrics', fontsize=10)
        ax.tick_params(labelsize=8)
        self.bar_canvas.draw()

        # Pie Chart
        self.pie_figure.clear()
        ax = self.pie_figure.add_subplot(111)
        labels = data['type_distribution'].keys()
        sizes = data['type_distribution'].values()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, 
               colors=['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6'])
        ax.axis('equal')
        ax.set_title('Equipment Type Distribution', fontsize=10)
        self.pie_canvas.draw()

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Valid CSV', '.', "CSV files (*.csv)")
        if fname:
            self.set_status("Uploading file...")
            files = {'file': open(fname, 'rb')}
            try:
                resp = requests.post(f"{API_BASE}/upload/", files=files, headers=self.get_auth_header())
                if resp.status_code == 201:
                    QMessageBox.information(self, "Success", "Dataset uploaded successfully")
                    self.refresh_data()
                else:
                    self.set_status("Upload failed")
                    QMessageBox.warning(self, "Error", f"Upload failed: {resp.text}")
            except Exception as e:
                self.set_status("Error")
                QMessageBox.critical(self, "Error", str(e))
        else:
            self.set_status("Upload cancelled")

    def download_report(self):
        try:
            self.set_status("Downloading report...")
            resp = requests.get(f"{API_BASE}/report/", headers=self.get_auth_header())
            if resp.status_code == 200:
                path, _ = QFileDialog.getSaveFileName(self, "Save Report", "Chemical_Report.pdf", "PDF Files (*.pdf)")
                if path:
                    with open(path, 'wb') as f:
                        f.write(resp.content)
                    self.set_status("Report saved")
                    QMessageBox.information(self, "Success", "Report downloaded successfully!")
                else:
                    self.set_status("Download cancelled")
            else:
                self.set_status("Report fetch failed")
                QMessageBox.warning(self, "Error", "Could not fetch report.")
        except Exception as e:
            self.set_status("Error")
            QMessageBox.critical(self, "Error", str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemViz – Desktop Dashboard")
        self.resize(1100, 750)
        
        # Set Global App Styling
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                background-color: #f8fafc;
                color: #334155;
            }
            QGroupBox {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                margin-top: 20px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #475569;
            }
        """)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.login_screen = LoginWindow(self.show_dashboard)
        self.stack.addWidget(self.login_screen)
        
    def show_dashboard(self, token):
        self.dashboard_screen = DashboardWindow(token, self.logout)
        self.stack.addWidget(self.dashboard_screen)
        self.stack.setCurrentWidget(self.dashboard_screen)

    def logout(self):
        self.stack.setCurrentWidget(self.login_screen)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion engine for better generic looking widgets
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
