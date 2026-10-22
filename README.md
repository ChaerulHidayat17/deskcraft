# AutoDeploy IT — Zero-Touch Workstation Provisioning Portal ⚡

A modern, web-based IT Operations and System Support tool designed to automate endpoint provisioning, silent software installation, and operating system hardening for enterprise workstations in under 5 minutes.

Developed by **Chaerul Hidayat** for professional IT Support & Operations portfolio.

---

## 🚀 Key Features

* **Interactive Web GUI (Clean Light Mode)**:
  * Select applications per department or customize individual packages.
  * Role presets: **Staff & Office**, **Software Engineer**, **IT Support**, and **Creative Media**.
* **1-Line Remote Execution**:
  * Automatically generates a one-line PowerShell command:
    ```powershell
    irm "http://192.168.1.13:8000/run?apps=chrome,zoom,slack,7zip&tz=WIB&dns=cloudflare" | iex
    ```
* **Offline Deployment Ready**:
  * Download standalone `.ps1` for USB deployment on machines without prior internet access.
* **Automated OS Policies**:
  * Set corporate standardized hostname (e.g., `JKT-FIN-01`).
  * Enforce high-speed secure DNS (Cloudflare `1.1.1.1` or Google `8.8.8.8`).
  * Timezone synchronization to `Asia/Jakarta (WIB GMT+7)`.
  * Power plan optimization to prevent sleep during enterprise deployment.
* **Audit & Compliance Reporting**:
  * Generates an automated, tamper-evident HTML audit report (`IT-Setup-Report.html`) on the user's desktop with installation timestamps and exit codes.
  * Sends telemetry back to the centralized dashboard.

---

## 🛠️ Architecture & Tech Stack

* **Backend**: FastAPI (Python 3.10)
* **Frontend**: HTML5, Tailwind CSS, Vanilla JS (Apple Minimalist Light Mode)
* **Execution Engine**: Microsoft Windows Package Manager (`winget`) & Native PowerShell Engine
* **Port**: `8000` (Local Subnet `192.168.1.0/24`)

---

## 💻 Quick Start

1. Run `start.bat` or execute:
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8000
   ```
2. Open your browser at `http://localhost:8000` or `http://192.168.1.13:8000`.
3. Pick apps or a role preset, configure policies, and copy the generated 1-line command.
4. On any new laptop/workstation, open **PowerShell (Admin)**, paste the command, and press **Enter**.
