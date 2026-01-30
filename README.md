⚗️ Chemical Equipment Parameter Visualizer
ChemViz is a full-stack, hybrid application designed for the storage, analysis, and visualization of chemical equipment operational data. It demonstrates a unified architecture where a single Django REST API serves both a modern React Web Frontend and a native PyQt5 Desktop Application.

🚀 Features
Hybrid Frontend Support:
🌐 Web: Responsive Dashboard built with React, Vite, and Chart.js.
🖥️ Desktop: Native GUI built with PyQt5 and embedded Matplotlib charts.
Data Processing:
📂 CSV Upload: Validates and processes equipment logs (Flowrate, Pressure, Temperature).
📊 Analytics: Automatically calculates averages and equipment type distributions using Pandas.
💾 Data Retention: Automatically manages storage, keeping only the last 5 uploaded datasets.
Reporting:
📄 PDF Generation: Generates engineering-grade reports using ReportLab.
Security:
🔐 JWT Authentication: Secure login/signup flow for both Web and Desktop clients.
🛠️ Tech Stack
Backend
Framework: Django & Django REST Framework (DRF)
Data processing: Pandas, NumPy
Database: SQLite (Development)
Auth: SimpleJWT
Reporting: ReportLab
Web Frontend
Framework: React.js (Vite)
Styling: Vanilla CSS (Modern Variables)
Charts: Chart.js (react-chartjs-2)
Networking: Axios
Desktop Frontend
Framework: PyQt5
Charts: Matplotlib (FigureCanvasQTAgg)
Networking: Python Requests
⚡ Quick Start
1. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
2. Web Dashboard
cd web-frontend
npm install
npm run dev
# Open http://localhost:5173
3. Desktop App
cd desktop-app
pip install -r requirements.txt
python main.py
📝 Usage
Register/Login using the application (Default admin: admin / password123).
Upload a CSV file containing columns: Equipment Name, Type, Flowrate, Pressure, Temperature.
View Analytics on the dashboard.
Download a PDF summary report.
📄 License
This project is licensed under the MIT License.
