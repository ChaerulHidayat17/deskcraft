import os
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import socket, datetime, json

app = FastAPI(title="AutoDeploy IT Portal")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# If running in api/ subdirectory (Vercel)
if os.path.basename(BASE_DIR) == "api":
    TEMPLATES_DIR = os.path.join(os.path.dirname(BASE_DIR), "templates")
else:
    TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.168.1.1', 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()

CATALOG = [
    # Office & Productivity
    {"id": "chrome", "name": "Google Chrome", "category": "Office", "icon": "🌐", "winget": "Google.Chrome", "desc": "Browser standar perusahaan dengan ekstensi keamanan."},
    {"id": "firefox", "name": "Mozilla Firefox", "category": "Office", "icon": "🦊", "winget": "Mozilla.Firefox", "desc": "Browser alternatif privasi tinggi."},
    {"id": "zoom", "name": "Zoom Meetings", "category": "Office", "icon": "📹", "winget": "Zoom.Zoom", "desc": "Aplikasi video conference resmi kantor."},
    {"id": "slack", "name": "Slack", "category": "Office", "icon": "💬", "winget": "SlackTechnologies.Slack", "desc": "Komunikasi tim dan kolaborasi kerja."},
    {"id": "teams", "name": "Microsoft Teams", "category": "Office", "icon": "👥", "winget": "Microsoft.Teams", "desc": "Chat dan meeting ekosistem Microsoft."},
    {"id": "7zip", "name": "7-Zip", "category": "Office", "icon": "📦", "winget": "7zip.7zip", "desc": "Kompresi dan enkripsi berkas ZIP/7z dengan password AES-256."},
    {"id": "sumatrapdf", "name": "SumatraPDF", "category": "Office", "icon": "📄", "winget": "SumatraPDF.SumatraPDF", "desc": "Reader PDF super ringan, cepat, dan hemat RAM."},
    {"id": "acrobat", "name": "Adobe Acrobat Reader", "category": "Office", "icon": "📑", "winget": "Adobe.Acrobat.Reader.64-bit", "desc": "Viewer PDF resmi untuk form dan tanda tangan digital."},
    {"id": "libreoffice", "name": "LibreOffice", "category": "Office", "icon": "📝", "winget": "TheDocumentFoundation.LibreOffice", "desc": "Office suite gratis (Writer, Calc, Impress)."},
    {"id": "notion", "name": "Notion", "category": "Office", "icon": "📓", "winget": "Notion.Notion", "desc": "Workspace dokumentasi dan manajemen tugas tim."},

    # Remote & IT Support
    {"id": "anydesk", "name": "AnyDesk", "category": "IT Support", "icon": "⚡", "winget": "AnyDeskSoftwareGmbH.AnyDesk", "desc": "Remote desktop cepat untuk asistensi jarak jauh IT Support."},
    {"id": "rustdesk", "name": "RustDesk", "category": "IT Support", "icon": "🛡️", "winget": "RustDesk.RustDesk", "desc": "Remote desktop open-source aman tanpa lisensi komersial."},
    {"id": "terminal", "name": "Windows Terminal", "category": "IT Support", "icon": "💻", "winget": "Microsoft.WindowsTerminal", "desc": "Terminal modern multi-tab untuk PowerShell dan SSH."},
    {"id": "putty", "name": "PuTTY", "category": "IT Support", "icon": "🔌", "winget": "PuTTY.PuTTY", "desc": "Klien SSH dan Telnet untuk konfigurasi server dan router."},
    {"id": "wireshark", "name": "Wireshark", "category": "IT Support", "icon": "🦈", "winget": "WiresharkFoundation.Wireshark", "desc": "Analisis paket dan troubleshooting lalu lintas jaringan LAN."},
    {"id": "sysinternals", "name": "Sysinternals Suite", "category": "IT Support", "icon": "🔧", "winget": "Microsoft.Sysinternals.Suite", "desc": "Tool diagnosa tingkat lanjut (Process Explorer, Autoruns)."},

    # Developer & Engineering
    {"id": "vscode", "name": "VS Code", "category": "Developer", "icon": "🟦", "winget": "Microsoft.VisualStudioCode", "desc": "Editor kode standar industri dengan ribuan ekstensi."},
    {"id": "git", "name": "Git SCM", "category": "Developer", "icon": "🐙", "winget": "Git.Git", "desc": "Version control system untuk kolaborasi repository kode."},
    {"id": "nodejs", "name": "Node.js (LTS)", "category": "Developer", "icon": "🟢", "winget": "OpenJS.NodeJS.LTS", "desc": "JavaScript runtime untuk frontend dan backend development."},
    {"id": "python", "name": "Python 3", "category": "Developer", "icon": "🐍", "winget": "Python.Python.3.12", "desc": "Bahasa pemrograman untuk scripting, otomatisasi, dan data."},
    {"id": "docker", "name": "Docker Desktop", "category": "Developer", "icon": "🐳", "winget": "Docker.DockerDesktop", "desc": "Platform kontainerisasi untuk isolasi microservices."},
    {"id": "dbeaver", "name": "DBeaver CE", "category": "Developer", "icon": "🦫", "winget": "dbeaver.dbeaver", "desc": "Universal database manager (PostgreSQL, MySQL, SQLite)."},
    {"id": "postman", "name": "Postman", "category": "Developer", "icon": "🚀", "winget": "Postman.Postman", "desc": "Platform pengujian dan dokumentasi REST API."},

    # Media & Creative
    {"id": "vlc", "name": "VLC Media Player", "category": "Media", "icon": "🎬", "winget": "VideoLAN.VLC", "desc": "Pemutar video dan audio universal tanpa perlu install codec."},
    {"id": "obs", "name": "OBS Studio", "category": "Media", "icon": "🎥", "winget": "OBSProject.OBSStudio", "desc": "Perekam layar untuk pembuatan video tutorial dan tutorial IT."},
    {"id": "gimp", "name": "GIMP", "category": "Media", "icon": "🎨", "winget": "GIMP.GIMP", "desc": "Editor gambar bitmap alternatif gratis Adobe Photoshop."}
]

PRESETS = {
    "office": ["chrome", "zoom", "slack", "7zip", "sumatrapdf", "anydesk"],
    "developer": ["chrome", "vscode", "git", "nodejs", "python", "terminal", "7zip", "slack", "dbeaver"],
    "support": ["anydesk", "rustdesk", "wireshark", "putty", "terminal", "7zip", "chrome", "sysinternals"],
    "creative": ["chrome", "vlc", "obs", "gimp", "notion", "7zip", "zoom"]
}

REPORTS = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    local_ip = get_local_ip()
    categories = sorted(list(set(a["category"] for a in CATALOG)))
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "catalog": CATALOG,
            "categories": categories,
            "presets": PRESETS,
            "local_ip": local_ip,
            "reports": REPORTS[:10]
        }
    )

@app.get("/api/catalog")
async def get_catalog():
    return {"catalog": CATALOG, "presets": PRESETS}

def build_ps1(apps_str: str, tz: str = "WIB", dns: str = "cloudflare", pc_name: str = "", debloat: bool = False, server_host: str = "127.0.0.1:8000", protocol: str = "http"):
    app_ids = [a.strip() for a in apps_str.split(",") if a.strip()]
    selected_apps = [a for a in CATALOG if a["id"] in app_ids]

    packages_ps = "@(\n" + ",\n".join([f'    @{{ id = "{a["id"]}"; name = "{a["name"]}"; winget = "{a["winget"]}" }}' for a in selected_apps]) + "\n)"

    query_params = f"apps={apps_str}&tz={tz}&dns={dns}"
    if pc_name:
        query_params += f"&pc_name={pc_name}"
    run_url = f"{protocol}://{server_host}/run?{query_params}"

    script = f"""# ==============================================================================
# AutoDeploy IT - Zero-Touch Workstation Provisioning Script
# Generated by IT Support Portal on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Target Server: {protocol}://{server_host}
# ==============================================================================

# 0. PRIVILEGE & ZERO-TOUCH ENVIRONMENT SETUP
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {{
    Write-Host "[AutoDeploy IT] Mengaktifkan hak akses Administrator otomatis..." -ForegroundColor Yellow
    $elevateCmd = "& {{ [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; irm '{run_url}' | iex }}"
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `"$elevateCmd`"" -Verb RunAs
    exit
}}

$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Bypass Windows 'Downloaded from the Internet' & SmartScreen security prompts
$env:SEE_MASK_NOZONECHECKS = 1

# Temporarily silence UAC consent popups for child installers
$uacReg = "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"
$origUac = $null
try {{
    $origUac = (Get-ItemProperty $uacReg -Name ConsentPromptBehaviorAdmin -ErrorAction SilentlyContinue).ConsentPromptBehaviorAdmin
    Set-ItemProperty $uacReg -Name ConsentPromptBehaviorAdmin -Value 0 -Force -ErrorAction SilentlyContinue
}} catch {{}}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "       AutoDeploy IT - Zero-Touch Workstation Provisioning       " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Waktu Mulai : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "Host Target : $env:COMPUTERNAME ($env:USERNAME)" -ForegroundColor Gray
Write-Host "OS          : $([System.Environment]::OSVersion.VersionString)" -ForegroundColor Gray
Write-Host "-----------------------------------------------------------------" -ForegroundColor DarkGray

$startTime = [System.Diagnostics.Stopwatch]::StartNew()
$results = @()

# 1. OPTIMIZE POWER PLAN (Prevent sleep during setup)
try {{
    Write-Host "[1/5] Mengatur Power Plan (Mencegah sleep saat instalasi)..." -ForegroundColor Cyan
    powercfg /change standby-timeout-ac 0 2>$null
    powercfg /change monitor-timeout-ac 15 2>$null
    Write-Host "      Power plan berhasil dioptimalkan." -ForegroundColor Green
}} catch {{}}

# 2. CONFIGURE TIMEZONE
"""
    if tz == "WIB":
        script += """try {
    Write-Host "[2/5] Mengatur zona waktu ke WIB (Asia/Jakarta)..." -ForegroundColor Cyan
    Set-TimeZone -Id "SE Asia Standard Time" -ErrorAction SilentlyContinue
    Write-Host "      Zona waktu: SE Asia Standard Time (WIB) Aktif." -ForegroundColor Green
} catch {
    Write-Host "      Gagal mengatur zona waktu." -ForegroundColor Red
}
"""
    else:
        script += """Write-Host "[2/5] Zona waktu dilewati." -ForegroundColor Gray
"""

    # 3. CONFIGURE SECURE DNS
    if dns == "cloudflare":
        script += """try {
    Write-Host "[3/5] Mengatur DNS Berkecepatan Tinggi (Cloudflare 1.1.1.1)..." -ForegroundColor Cyan
    $adapters = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' }
    foreach ($adapter in $adapters) {
        Set-DnsClientServerAddress -InterfaceAlias $adapter.Name -ServerAddresses ('1.1.1.1', '1.0.0.1') -ErrorAction SilentlyContinue
    }
    Write-Host "      DNS Cloudflare (1.1.1.1, 1.0.0.1) berhasil diterapkan." -ForegroundColor Green
} catch {
    Write-Host "      Gagal mengatur DNS." -ForegroundColor Red
}
"""
    elif dns == "google":
        script += """try {
    Write-Host "[3/5] Mengatur DNS Berkecepatan Tinggi (Google 8.8.8.8)..." -ForegroundColor Cyan
    $adapters = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' }
    foreach ($adapter in $adapters) {
        Set-DnsClientServerAddress -InterfaceAlias $adapter.Name -ServerAddresses ('8.8.8.8', '8.8.4.4') -ErrorAction SilentlyContinue
    }
    Write-Host "      DNS Google (8.8.8.8, 8.8.4.4) berhasil diterapkan." -ForegroundColor Green
} catch {
    Write-Host "      Gagal mengatur DNS." -ForegroundColor Red
}
"""
    else:
        script += """Write-Host "[3/5] Pengaturan DNS dilewati." -ForegroundColor Gray
"""

    # 4. RENAME COMPUTER IF REQUESTED
    if pc_name:
        clean_name = pc_name.strip()
        script += f"""try {{
    Write-Host "[4/5] Mengubah nama komputer menjadi: {clean_name}..." -ForegroundColor Cyan
    Rename-Computer -NewName "{clean_name}" -Force -ErrorAction SilentlyContinue
    Write-Host "      Nama komputer diatur ke {clean_name} (efektif setelah restart)." -ForegroundColor Green
}} catch {{
    Write-Host "      Gagal mengubah nama komputer." -ForegroundColor Red
}}
"""
    else:
        script += """Write-Host "[4/5] Pergantian nama komputer dilewati." -ForegroundColor Gray
"""

    # 5. INSTALL SOFTWARE PACKAGES
    script += f"""
Write-Host "[5/5] Memulai instalasi otomatis aplikasi ({len(selected_apps)} aplikasi)..." -ForegroundColor Yellow
$packages = {packages_ps}

$wingetCmd = Get-Command winget -ErrorAction SilentlyContinue
if (-not $wingetCmd) {{
    Write-Host "CRITICAL ERROR: Windows Package Manager (winget) belum terpasang." -ForegroundColor Red
    Write-Host "Silakan update App Installer via Microsoft Store terlebih dahulu." -ForegroundColor Yellow
    exit 1
}}

$count = 0
foreach ($pkg in $packages) {{
    $count++
    $packageId = $pkg.winget
    $pName = $pkg.name
    Write-Host "  [$count/$($packages.Count)] Memasang $pName ($packageId)..." -ForegroundColor White -NoNewline
    
    $proc = Start-Process -FilePath "winget" -ArgumentList "install --id `"$packageId`" --exact --silent --accept-package-agreements --accept-source-agreements --disable-interactivity" -Wait -PassThru -NoNewWindow
    
    if ($proc.ExitCode -eq 0 -or $proc.ExitCode -eq 3010 -or $proc.ExitCode -eq -1978335189) {{
        Write-Host " [BERHASIL]" -ForegroundColor Green
        $results += [PSCustomObject]@{{ Name = $pName; ID = $packageId; Status = "Success" }}
    }} else {{
        Write-Host " [KODE EXIT: $($proc.ExitCode)]" -ForegroundColor Red
        $results += [PSCustomObject]@{{ Name = $pName; ID = $packageId; Status = "Failed (Code: $($proc.ExitCode))" }}
    }}
}}

$startTime.Stop()
$elapsed = $startTime.Elapsed.ToString("mm\\:ss")

# GENERATE AUDIT REPORT
Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host "          PROVISIONING SELESAI DALAM $elapsed MENIT          " -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan

$reportHtml = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>IT Provisioning Audit Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #F2F2F7; padding: 30px; color: #1C1C1E; }}
        .card {{ background: #FFFFFF; border-radius: 14px; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); max-width: 700px; margin: 0 auto; }}
        h1 {{ font-size: 22px; margin-top: 0; color: #007AFF; }}
        .meta {{ background: #F2F2F7; border-radius: 10px; padding: 12px; margin-bottom: 20px; font-size: 13px; line-height: 1.6; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }}
        th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #E5E5EA; }}
        th {{ background: #F8F9FA; font-weight: 600; color: #6C6C70; }}
        .badge-success {{ background: #D1E7DD; color: #0F5132; padding: 4px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; }}
        .badge-failed {{ background: #F8D7DA; color: #842029; padding: 4px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>IT Workstation Provisioning Report</h1>
        <div class="meta">
            <b>Hostname:</b> $env:COMPUTERNAME<br>
            <b>User:</b> $env:USERNAME<br>
            <b>Waktu Eksekusi:</b> $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')<br>
            <b>Total Durasi:</b> $elapsed Menit
        </div>
        <table>
            <tr><th>Aplikasi</th><th>Package ID</th><th>Status</th></tr>
"@

foreach ($r in $results) {{
    $badge = if ($r.Status -eq "Success") {{ "<span class='badge-success'>BERHASIL</span>" }} else {{ "<span class='badge-failed'>GAGAL</span>" }}
    $reportHtml += "<tr><td>$($r.Name)</td><td><code>$($r.ID)</code></td><td>$badge</td></tr>`n"
}}

$reportHtml += @"
        </table>
        <p style="margin-top: 20px; font-size: 12px; color: #8E8E93; text-align: center;">Generated automatically by AutoDeploy IT Portal.</p>
    </div>
</body>
</html>
"@

$desktopReport = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"), "IT-Setup-Report.html")
$reportHtml | Out-File -FilePath $desktopReport -Encoding utf8
Write-Host "Laporan Audit HTML disimpan di: $desktopReport" -ForegroundColor Yellow

# Post telemetry back to portal if reachable
try {{
    $body = @{{
        hostname = $env:COMPUTERNAME
        user = $env:USERNAME
        duration = $elapsed
        apps_installed = ($results | Where-Object {{ $_.Status -eq 'Success' }}).Count
        apps_total = $results.Count
        status = "Completed"
    }} | ConvertTo-Json
    Invoke-RestMethod -Uri "{protocol}://{server_host}/api/report" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 3 -ErrorAction SilentlyContinue
}} catch {{}}

# Restore UAC security policy
try {{
    if ($null -ne $origUac) {{
        Set-ItemProperty $uacReg -Name ConsentPromptBehaviorAdmin -Value $origUac -Force -ErrorAction SilentlyContinue
    }} else {{
        Set-ItemProperty $uacReg -Name ConsentPromptBehaviorAdmin -Value 5 -Force -ErrorAction SilentlyContinue
    }}
}} catch {{}}

Write-Host "Semua proses selesai! Workstation siap diserahkan kepada pengguna.`n" -ForegroundColor Green
"""
    return script

@app.get("/run", response_class=PlainTextResponse)
async def run_script(
    request: Request,
    apps: str = Query("chrome,zoom,slack,7zip"),
    tz: str = Query("WIB"),
    dns: str = Query("cloudflare"),
    pc_name: str = Query(""),
    debloat: bool = Query(False)
):
    host = request.headers.get("host") or f"{get_local_ip()}:8000"
    proto = "https" if "vercel.app" in host or "trycloudflare.com" in host or request.headers.get("x-forwarded-proto") == "https" else "http"
    script = build_ps1(apps, tz, dns, pc_name, debloat, server_host=host, protocol=proto)
    return PlainTextResponse(script, media_type="text/plain; charset=utf-8")

@app.get("/download")
async def download_script(
    request: Request,
    apps: str = Query("chrome,zoom,slack,7zip"),
    tz: str = Query("WIB"),
    dns: str = Query("cloudflare"),
    pc_name: str = Query(""),
    debloat: bool = Query(False)
):
    host = request.headers.get("host") or f"{get_local_ip()}:8000"
    proto = "https" if "vercel.app" in host or "trycloudflare.com" in host or request.headers.get("x-forwarded-proto") == "https" else "http"
    script = build_ps1(apps, tz, dns, pc_name, debloat, server_host=host, protocol=proto)
    return Response(
        content=script,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=Setup-Workstation.ps1"}
    )

@app.post("/api/report")
async def receive_report(report: dict):
    report["timestamp"] = datetime.datetime.now().strftime("%H:%M:%S")
    REPORTS.insert(0, report)
    if len(REPORTS) > 20:
        REPORTS.pop()
    return {"status": "ok"}