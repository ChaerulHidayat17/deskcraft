# DeskCraft — Precision Workstation Provisioning Platform 🖥️⚡

> An enterprise-grade, cloud-powered IT Operations and Systems Engineering tool designed to automate endpoint provisioning, unattended multi-package deployment, and Windows operating system baseline hardening in under 5 minutes.

Developed by **Chaerul Hidayat** ([@ChaerulHidayat17](https://github.com/ChaerulHidayat17)) for professional IT Support, Systems Engineering, and Cloud Infrastructure portfolios.

🌐 **Live Web Portal**: [https://it-setup-portal-app.vercel.app](https://it-setup-portal-app.vercel.app)  
🐙 **GitHub Repository**: [https://github.com/ChaerulHidayat17/deskcraft](https://github.com/ChaerulHidayat17/deskcraft)

---

## 🚀 Key Highlights & Architectural Features

* **Zero-Touch 1-Line Execution Engine**:
  * Dynamically generates an in-memory execution command:
    ```powershell
    irm "https://it-setup-portal-app.vercel.app/run?apps=chrome,zoom,slack,7zip&tz=WIB&dns=cloudflare&pc_name=JKT-FIN-01" | iex
    ```
  * Zero residual clutter on disk: scripts are fetched over TLS 1.2/1.3 and executed straight in RAM.
* **Apple iPadOS/macOS-Inspired Web Interface**:
  * Interactive light-mode UI engineered with Tailwind CSS.
  * Role presets for rapid onboarding: **Staff & Office**, **Software Engineer**, **IT Support**, and **Creative Media**.
  * Fully responsive mobile viewport with touch-swipeable category filters and sticky action bars.
* **Enterprise Guardrails & Automatic Privilege Elevation**:
  * **Auto-Elevate**: Detects whether PowerShell has High Integrity (Administrator); automatically spawns an elevated session with `-NoExit` if launched by a standard user.
  * **UAC Suppression**: Temporarily sets `ConsentPromptBehaviorAdmin` to `0` during setup to silence blocking elevation dialogs for child installers, restoring security policy upon completion.
  * **SmartScreen Bypass**: Enforces `$env:SEE_MASK_NOZONECHECKS = 1` to prevent Windows from pausing with *"Downloaded from the Internet"* security warnings.
* **Universal Hardware & OS Compatibility**:
  * **Winget Auto-Bootstrap**: Automatically discovers `winget.exe` in system `WindowsApps` directories or pulls the official MSIX package from Microsoft (`aka.ms/getwinget`).
  * **Smart Hash Override**: Gracefully recovers from upstream package SHA-256 hash mismatches by enabling `InstallerHashOverride` and retrying with `--ignore-security-hash`.
  * **Dual Power Plan Optimization**: Disables standby timeouts for both AC charger and DC laptop battery modes (`powercfg /change standby-timeout-dc 0`).
  * **Physical Network Filtering**: Targets only physical Wi-Fi and Ethernet adapters, safely skipping virtual and container adapters (WSL, Hyper-V, VMware).
* **Compliance & Audit Logging**:
  * Automatically compiles a tamper-evident HTML audit summary (`IT-Setup-Report.html`) directly on the target machine's Desktop, detailing hostname, operator, duration, and per-package exit codes.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Cloud Runtime** | Vercel Serverless Functions (Python 3.10) |
| **Backend Framework** | FastAPI, Uvicorn, Jinja2 Templates |
| **Frontend UI** | HTML5, Tailwind CSS, Plus Jakarta Sans, JetBrains Mono |
| **Automation Engine** | Windows Package Manager (`winget`), Windows PowerShell 5.1 / 7+ |
| **Reporting & Audit** | Self-contained Responsive HTML5 / CSS3 Report |

---

## 📖 3-Langkah Menjalankan di Workstation Baru

1. **Buka PowerShell Administrator**:
   * Tekan keyboard `Win + X`, lalu pilih **Terminal (Admin)** atau **Windows PowerShell (Run as administrator)**.
2. **Salin & Tempel Perintah**:
   * Pilih paket software di [DeskCraft Portal](https://it-setup-portal-app.vercel.app), klik **Salin Perintah**, lalu paste ke PowerShell dan tekan `Enter`.
3. **Otomatis Selesai (Zero-Touch)**:
   * Seluruh software dan kebijakan sistem terpasang di latar belakang tanpa interupsi.
   * Laporan audit resmi `IT-Setup-Report.html` otomatis tersimpan di Desktop sebagai bukti serah terima unit.

---

## 💻 Menjalankan di Server Lokal (Offline LAN)

Untuk deployment di lingkungan jaringan kantor internal (Intranet/LAN) tanpa koneksi cloud:

1. Clone repositori:
   ```bash
   git clone https://github.com/ChaerulHidayat17/deskcraft.git
   cd deskcraft
   ```
2. Jalankan server lokal:
   ```cmd
   start.bat
   ```
   *atau via Python langsung:*
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8000
   ```
3. Akses portal dari browser laptop/HP di subnet LAN yang sama:
   `http://<IP-Laptop-Anda>:8000`

---

## 📄 Lisensi
Didistribusikan di bawah lisensi MIT. Bebas digunakan untuk keperluan operasional IT kantor maupun portofolio profesional.
