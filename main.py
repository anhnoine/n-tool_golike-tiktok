import json
import os
import subprocess
import sys
import time
import random
import re
import xml.etree.ElementTree as ET
import importlib
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box


# =============================================================================
# AUTO INSTALL DEPENDENCIES
# =============================================================================

_REQUIRED_PACKAGES = [
    "rich",
    "requests",
    "pure-python-adb",
]

# Map pip package names -> actual Python module import names
# Only needed when the module name differs from the package name
_PACKAGE_IMPORT_MAP = {
    "pure-python-adb": "ppadb",
}

def _get_import_name(pkg: str) -> str:
    """Trả về tên module Python thực tế cho một package."""
    return _PACKAGE_IMPORT_MAP.get(pkg, pkg.replace("-", "_").replace(".", ""))

def auto_install_dependencies():
    """Kiểm tra và tự động cài đặt các thư viện Python cần thiết."""
    missing = []
    for pkg in _REQUIRED_PACKAGES:
        try:
            importlib.import_module(_get_import_name(pkg))
        except ImportError:
            missing.append(pkg)

    if not missing:
        return

    print("\033[1;33m[!] Đang cài đặt thư viện cần thiết...\033[0m")
    for pkg in missing:
        print(f"\033[1;34m  ⟳ Đang cài {pkg}...\033[0m")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"\033[1;32m  ✓ Đã cài {pkg}\033[0m")
        except subprocess.CalledProcessError:
            # Fallback: dùng pip3
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip3", "install", pkg],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                print(f"\033[1;32m  ✓ Đã cài {pkg}\033[0m")
            except Exception:
                print(f"\033[1;31m  ✗ Lỗi cài {pkg}, hãy cài thủ công: pip install {pkg}\033[0m")
                sys.exit(1)

    # Load lại module
    for pkg in missing:
        importlib.import_module(_get_import_name(pkg))

    print("\033[1;32m✓ Tất cả thư viện đã sẵn sàng!\033[0m")
    time.sleep(1)


# =============================================================================
# CẤU HÌNH
# =============================================================================

# Biến toàn cục - sẽ được cập nhật từ Authorization.txt
AUTHORIZATION = ""
USER_AGENT = "Mozilla/5.0 (Linux; Android 10; SC-03L Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/136.0.7103.60 Mobile Safari/537.36"
CURL_HEADERS: list[str] = []

BASE_URL = os.getenv("GOLIKE_API_URL", "https://gateway.golike.net")
TIKTOK_ACCOUNT_URL = f"{BASE_URL}/api/tiktok-account"
JOBS_URL = f"{BASE_URL}/api/advertising/publishers/tiktok/jobs"
COMPLETE_URL = f"{BASE_URL}/api/advertising/publishers/tiktok/complete-jobs"

FILE_CLICK = "click.txt"
FILE_DEVICES = "devices.txt"
FILE_AUTHORIZATION = "Authorization.txt"
UI_XML_LOCAL = "ui.xml"

# =============================================================================
# MÀU SẮC CHO TERMINAL
# =============================================================================

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    PRIMARY = '\033[38;5;141m'
    SECONDARY = '\033[38;5;117m'
    SUCCESS = '\033[38;5;120m'
    WARNING = '\033[38;5;221m'
    ERROR = '\033[38;5;210m'
    INFO = '\033[38;5;159m'
    ACCENT = '\033[38;5;183m'
    MUTED = '\033[38;5;250m'
    WHITE = '\033[97m'
    GRAY = '\033[38;5;242m'
    GOLD_1 = '\033[38;5;220m'
    CYAN = '\033[38;5;51m'
    YELLOW = '\033[38;5;220m'
    ORANGE = '\033[38;5;208m'
    SOFT_RED = '\033[38;5;211m'
    TT8_GREEN_PRIMARY = '\033[38;5;114m'
    TT9_BLUE_PRIMARY = '\033[38;5;39m'
    GRAD1 = '\033[38;5;147m'
    GRAD2 = '\033[38;5;153m'
    GRAD3 = '\033[38;5;159m'
    TT8_GREEN_SECONDARY = '\033[38;5;150m'
    TT8_GREEN_INFO = '\033[38;5;156m'
    TT8_GREEN_ACCENT = '\033[38;5;157m'
    TT9_BLUE_SECONDARY = '\033[38;5;81m'
    TT9_BLUE_INFO = '\033[38;5;87m'
    TT9_BLUE_ACCENT = '\033[38;5;123m'
    CASTORICE_PRIMARY = '\033[38;5;141m'
    CASTORICE_SECONDARY = '\033[38;5;177m'
    CASTORICE_ACCENT = '\033[38;5;183m'
    CASTORICE_LIGHT = '\033[38;5;189m'
    CASTORICE_DARK = '\033[38;5;135m'
    SOFT_RED_SECONDARY = '\033[38;5;217m'
    SOFT_RED_ACCENT = '\033[38;5;224m'
    AMETHYST_DARK = '\033[38;5;54m'
    AMETHYST_MID = '\033[38;5;99m'
    AMETHYST_LIGHT = '\033[38;5;189m'
    SAKURA_DEEP = '\033[38;5;204m'
    SAKURA_MID = '\033[38;5;218m'
    SAKURA_LIGHT = '\033[38;5;225m'
C = Colors()

time_str = time.strftime("%d/%m/%Y", time.localtime())

console = Console()

ASCII_ART = [
    f"{C.CASTORICE_DARK} __   __          ___________   ______     ______    __      ",
    f"{C.CASTORICE_PRIMARY}|  \\ |  |        |           | /  __  \\   /  __  \\  |  |     ",
    f"{C.CASTORICE_SECONDARY}|   \\|  |  ______`---|  |----`|  |  |  | |  |  |  | |  |     ",
    f"{C.CASTORICE_ACCENT}|  . `  | |______|   |  |     |  |  |  | |  |  |  | |  |     ",
    f"{C.CASTORICE_LIGHT}|  |\\   |            |  |     |  `--'  | |  `--'  | |  `----.",
    f"{C.CASTORICE_DARK}|__| \\__|            |__|      \\______/   \\______/  |_______|\n"
    f"{C.RESET}"
]

_MINECRAFT_COLORS = {
    '0': '000000', '1': '0000AA', '2': '00AA00', '3': '00AAAA',
    '4': 'AA0000', '5': 'AA00AA', '6': 'FFAA00', '7': 'AAAAAA',
    '8': '555555', '9': '5555FF', 'a': '55FF55', 'b': '55FFFF',
    'c': 'FF5555', 'd': 'FF55FF', 'e': 'FFFF55', 'f': 'FFFFFF',
}

_MINECRAFT_FORMATS = {
    'l': '\033[1m',   # bold
    'm': '\033[9m',   # strikethrough
    'n': '\033[4m',   # underline
    'o': '\033[3m',   # italic
    'k': '',           # obfuscated — unsupported in terminal
    'r': '\033[0m',   # reset
}


def c_n(text: str) -> str:
    result = []
    i = 0
    n = len(text)

    while i < n:
        if text[i] == '&' and i + 1 < n:
            code = text[i + 1].lower()

            if code == 'x' and i + 14 <= n:
                hex_digits = []
                valid = True
                for j in range(6):
                    pos = i + 2 + j * 2
                    if pos + 1 < n and text[pos] == '&':
                        d = text[pos + 1]
                        if d.lower() in '0123456789abcdef':
                            hex_digits.append(d)
                        else:
                            valid = False
                            break
                    else:
                        valid = False
                        break
                if valid:
                    rgb = ''.join(hex_digits)
                    r = int(rgb[0:2], 16)
                    g = int(rgb[2:4], 16)
                    b = int(rgb[4:6], 16)
                    result.append(f'\033[38;2;{r};{g};{b}m')
                    i += 14
                    continue

            if code in _MINECRAFT_COLORS:
                rgb = _MINECRAFT_COLORS[code]
                r = int(rgb[0:2], 16)
                g = int(rgb[2:4], 16)
                b = int(rgb[4:6], 16)
                result.append(f'\033[38;2;{r};{g};{b}m')
                i += 2
                continue

            if code in _MINECRAFT_FORMATS:
                result.append(_MINECRAFT_FORMATS[code])
                i += 2
                continue

            # Unknown & — emit as literal
            result.append('&')
            i += 1
            continue
          
        result.append(text[i])
        i += 1

    result.append('\033[0m')
    return ''.join(result)

TITLE_COLORED = c_n(
    "&x&F&F&8&5&C&7&lI&x&F&C&9&2&C&C&ld&x&F&A&9&F&D&0&ll"
    "&x&F&7&A&C&D&5&le&x&F&5&B&9&D&9&lr"
    " &x&F&9&A&6&D&3&lH&x&F&F&8&5&C&7&la"
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def idlerhatool():
    screen_width = console.size.width
    box_width = 75
    if screen_width < 79:
        box_width = max(screen_width - 2, 40)

    banner_content = Text.from_ansi("\n".join(ASCII_ART) + C.RESET)

    panel = Panel(
        Align.center(banner_content),
        title=Text.from_ansi(TITLE_COLORED),
        title_align="center",
        subtitle=f"[white] Version: v1.0.0 [black]|[/black] Date: {time_str} [/white]",
        subtitle_align="center",
        width=box_width,
        border_style="bold magenta",
        box=box.SQUARE,
    )

    console.print(Align.center(panel))


# =============================================================================
# AUTHORIZATION MANAGEMENT
# =============================================================================

def set_authorization(token: str):
    """Cập nhật token Authorization và CURL_HEADERS."""
    global AUTHORIZATION, CURL_HEADERS
    if not token.startswith("Bearer "):
        token = f"Bearer {token}"
    AUTHORIZATION = token
    CURL_HEADERS = [
        "-H", f"Authorization: {AUTHORIZATION}",
        "-H", f"User-Agent: {USER_AGENT}",
        "-H", "Content-Type: application/json;charset=UTF-8",
    ]

def is_authorization_valid() -> bool:
    """Kiểm tra token Authorization hiện tại có hợp lệ không."""
    if not AUTHORIZATION or not CURL_HEADERS:
        return False
    data = _curl_get(TIKTOK_ACCOUNT_URL, timeout=10)
    if data is None:
        return False
    return data.get("success", False)

def ensure_required_files():
    """Tạo file click.txt và devices.txt nếu chưa tồn tại."""
    if not os.path.exists(FILE_CLICK):
        with open(FILE_CLICK, "w", encoding="utf-8") as f:
            f.write('follow_user="0.277, 0.36"\n')
        print(f"  {C.INFO}📄 Đã tạo file {FILE_CLICK} (mặc định){C.RESET}")

    if not os.path.exists(FILE_DEVICES):
        with open(FILE_DEVICES, "w") as f:
            f.write("")
        print(f"  {C.INFO}📄 Đã tạo file {FILE_DEVICES}{C.RESET}")

def load_or_request_authorization() -> str:
    """
    Kiểm tra Authorization.txt, nếu có thì dùng thử.
    Nếu không hợp lệ hoặc không có, yêu cầu nhập và validate.
    Lưu vào file khi hợp lệ.
    """
    clear_screen()
    idlerhatool()
    print()
    console.print(Align.center(Panel(            " ",
            title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}XÁC THỰC AUTHORIZATION{C.RESET}"),
            title_align="center",
            border_style="bold #ca80ff",
            box=box.SQUARE,
            padding=(0, 0),
    )))
    print()

    # Kiểm tra file Authorization.txt
    if os.path.exists(FILE_AUTHORIZATION):
        with open(FILE_AUTHORIZATION, "r") as f:
            saved_token = f.read().strip()
        if saved_token:
            print(f"  {C.INFO}⟳ Đang kiểm tra Authorization đã lưu...{C.RESET}")
            set_authorization(saved_token)
            time.sleep(1)
            if is_authorization_valid():
                print(f"  {C.SUCCESS}✅ Authorization hợp lệ!{C.RESET}")
                time.sleep(1)
                return saved_token
            else:
                print(f"  {C.ERROR}❌ Authorization đã lưu không hợp lệ hoặc đã hết hạn.{C.RESET}")
                time.sleep(1)

    # Yêu cầu nhập token mới
    while True:
        clear_screen()
        idlerhatool()
        print()
        console.print(Align.center(Panel(
            " ",
            title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}NHẬP AUTHORIZATION{C.RESET}"),
            title_align="center",
            border_style="bold #ca80ff",
            box=box.SQUARE,
            padding=(0, 0),
        )))
        print()
        print(f"  {C.INFO}Vui lòng nhập Authorization token từ Golike:{C.RESET}")
        print(f"  {C.MUTED}  (Ví dụ: Bearer eyanhnoidz...){C.RESET}\n")
        token = input(f"  {C.CYAN}└── Authorization: {C.RESET}").strip()

        if not token:
            print(f"  {C.ERROR}❌ Token không được để trống!{C.RESET}")
            time.sleep(1)
            continue

        set_authorization(token)
        print(f"\n  {C.INFO}⟳ Đang kiểm tra Authorization...{C.RESET}")
        time.sleep(1)

        if is_authorization_valid():
            print(f"  {C.SUCCESS}✅ Authorization hợp lệ! Đang lưu...{C.RESET}")
            with open(FILE_AUTHORIZATION, "w") as f:
                f.write(AUTHORIZATION)
            print(f"  {C.INFO}💾 Đã lưu vào {FILE_AUTHORIZATION}{C.RESET}")
            time.sleep(1)
            return AUTHORIZATION
        else:
            print(f"  {C.ERROR}❌ Authorization không hợp lệ! Vui lòng thử lại.{C.RESET}")
            print(f"  {C.MUTED}  Kiểm tra lại token trên Golike và nhập đúng.{C.RESET}")
            time.sleep(2)

# =============================================================================
# TIỆN ÍCH CURL – GOLIKE API
# =============================================================================

def _curl_get(url: str, timeout: int = 15) -> dict[str, Any] | None:
    if not CURL_HEADERS:
        return None
    cmd = ["curl", "-s", "--max-time", str(timeout), url] + CURL_HEADERS
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        if result.returncode != 0:
            return None
        return json.loads(result.stdout) if result.stdout.strip() else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        return None


def _curl_post(url: str, params: dict[str, Any], timeout: int = 15) -> dict[str, Any] | None:
    if not CURL_HEADERS:
        return None
    param_parts = [f"{k}={v}" for k, v in params.items()]
    full_url = f"{url}?{'&'.join(param_parts)}"
    cmd = ["curl", "-s", "--max-time", str(timeout), "-X", "POST", full_url] + CURL_HEADERS
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        if result.returncode != 0:
            return None
        return json.loads(result.stdout) if result.stdout.strip() else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        return None

# =============================================================================
# GOLIKE ACCOUNT & JOB MANAGEMENT
# =============================================================================

def get_tiktok_accounts() -> tuple[list[dict[str, Any]], str]:
    """Lấy danh sách tài khoản TikTok đã liên kết từ Golike."""
    data = _curl_get(TIKTOK_ACCOUNT_URL)
    if data is None:
        return [], "Không thể kết nối đến API (curl lỗi)"
    if data.get("success"):
        accounts = data.get("data", [])
        return [acc for acc in accounts if isinstance(acc, dict)], ""
    return [], data.get("message") or "API trả về success=false"


def select_tiktok_account() -> tuple[int, dict[str, Any]]:
    """
    Hiển thị danh sách tài khoản TikTok đã liên kết và cho người dùng chọn.
    Returns (account_id, account_info) hoặc (None, None) nếu không chọn được.
    """
    clear_screen()
    idlerhatool()
    print("")
    accounts, err = get_tiktok_accounts()

    if err:
        panel = Panel(
            Align.center(Text.from_ansi(f"{C.ERROR}❌ Lỗi: {err}{C.RESET}")),
            title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}CHỌN TÀI KHOẢN TIKTOK{C.RESET}"),
            title_align="center",
            border_style="bold #ca80ff",
            box=box.SQUARE,
            padding=(1, 2),
        )
        console.print(Align.center(panel))
        return None, None

    if not accounts:
        panel = Panel(
            Align.center(Text.from_ansi(f"{C.WARNING}⚠️ Không có tài khoản TikTok nào được liên kết.{C.RESET}")),
            title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}CHỌN TÀI KHOẢN TIKTOK{C.RESET}"),
            title_align="center",
            border_style="bold #ca80ff",
            box=box.SQUARE,
            padding=(1, 2),
        )
        console.print(Align.center(panel))
        return None, None

    content_lines = [
        Text.from_ansi(f"{C.RESET}"),
    ]

    for i, acc in enumerate(accounts, 1):
        nickname = acc.get('nickname', '?')
        username = acc.get('username', '?')
        acc_id = acc.get('id', '?')
        status = acc.get('status', '?')
        banned = acc.get('is_banned', False)
        status_icon = "🟢" if not banned and status == "active" else "🔴"
        content_lines.append(Text.from_ansi(
            f"{C.GOLD_1}[{i}]{C.RESET} {status_icon} {C.BOLD}{nickname}{C.RESET} (@{username})\n"
            f"      {C.MUTED}ID: {acc_id} | Status: {status} | Banned: {banned}{C.RESET}"
        ))

    # Combine content lines into a single renderable
    combined_content = Text()
    for line in content_lines:
        if combined_content:
            combined_content.append("\n")
        combined_content.append(line)
    
    panel = Panel(
        Align.center(combined_content),
        title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}CHỌN TÀI KHOẢN TIKTOK{C.RESET}"),
        title_align="center",
        border_style="bold #ca80ff",
        box=box.SQUARE,
        padding=(1, 2),
    )
    console.print(Align.center(panel))

    print()
    while True:
        try:
            choice = input(f"➤ Chọn tài khoản (1-{len(accounts)}): ").strip()
            if not choice:
                console.print(Align.center(Text.from_ansi(f"{C.ERROR}❌ Vui lòng chọn một tài khoản!{C.RESET}")))
                time.sleep(1)
                continue
            idx = int(choice) - 1
            if 0 <= idx < len(accounts):
                selected = accounts[idx]
                console.print(Align.center(Text.from_ansi(
                    f"{C.SUCCESS}✅ Đã chọn: {selected.get('nickname', '?')} (@{selected.get('username', '?')}){C.RESET}"
                )))
                time.sleep(1)
                return selected.get('id'), selected
            else:
                console.print(Align.center(Text.from_ansi(
                    f"{C.ERROR}❌ Lựa chọn không hợp lệ. Vui lòng chọn từ 1-{len(accounts)}.{C.RESET}"
                )))
                time.sleep(1)
        except (ValueError, IndexError):
            console.print(Align.center(Text.from_ansi(
                f"{C.ERROR}❌ Lựa chọn không hợp lệ. Vui lòng chọn từ 1-{len(accounts)}.{C.RESET}"
            )))
            time.sleep(1)


def get_jobs(account_id: int | None = None) -> tuple[list[dict[str, Any]], str]:
    jobs: list[dict[str, Any]] = []

    if account_id is None:
        accounts, acc_err = get_tiktok_accounts()
        if acc_err:
            return [], acc_err
        account_ids = [acc["id"] for acc in accounts if "id" in acc]
    else:
        account_ids = [account_id]

    if not account_ids:
        return [], "Không có tài khoản TikTok nào."

    last_error = ""
    for acc_id in account_ids:
        url = f"{JOBS_URL}?account_id={acc_id}&data=null"
        data = _curl_get(url)
        if data is None:
            last_error = f"Acc {acc_id}: curl lỗi"
            continue
        if data.get("success") and data.get("data"):
            raw = data["data"]
            if isinstance(raw, dict):
                job = dict(raw)
                job["_account_id"] = acc_id
                jobs.append(job)
            elif isinstance(raw, list):
                for item in raw:
                    if isinstance(item, dict):
                        job = dict(item)
                        job["_account_id"] = acc_id
                        jobs.append(job)
        elif data.get("success") and not data.get("data"):
            last_error = f"Acc {acc_id}: không có job"
        else:
            last_error = f"Acc {acc_id}: {data.get('message', 'lỗi không rõ')}"

    return jobs, last_error if not jobs else ""


def complete_job(ads_id: int, account_id: int, object_id: str, job_type: str, **extra: Any) -> tuple[bool, str, dict[str, Any] | None]:
    params: dict[str, Any] = {
        "ads_id": ads_id,
        "account_id": account_id,
        "object_id": object_id,
        "async": "true",
        "data": "null",
        "type": job_type,
    }
    params.update(extra)

    max_retries = 2
    for attempt in range(max_retries + 1):
        if attempt > 0:
            time.sleep(2)
        data = _curl_post(COMPLETE_URL, params)
        if data is None:
            continue
        if data.get("success"):
            return True, data.get("message") or "Thành công", data.get("data")
        # API trả về success=false, retry
        if attempt < max_retries:
            continue
        return False, data.get("message", "Thất bại"), data.get("data")
    return False, "Không thể kết nối đến API (curl lỗi)", None


# =============================================================================
# ADB BACKEND — Hỗ trợ cả system ADB và pure-python-adb (ppadb)
# =============================================================================

class _AdbBackend:
    """
    Lớp trừu tượng hóa ADB backend.
    - 'system': gọi adb binary qua subprocess
    - 'ppadb' : dùng thư viện pure-python-adb (ppadb)
    Tự động phát hiện backend phù hợp.
    """

    def __init__(self):
        self._type = 'system'
        self._ppadb_client = None
        self._detect()

    def _detect(self):
        """Phát hiện backend: ưu tiên system ADB, fallback ppadb."""
        # Thử system ADB trước
        try:
            subprocess.run(
                ["adb", "version"],
                capture_output=True, text=True, timeout=5
            )
            self._type = 'system'
            return
        except (FileNotFoundError, Exception):
            pass

        # Thử ppadb
        try:
            from ppadb.client import Client as AdbClient
            self._ppadb_client = AdbClient(host="127.0.0.1", port=5037)
            # Kiểm tra xem có kết nối được ADB server không
            self._ppadb_client.devices()
            self._type = 'ppadb'
        except Exception:
            # Không có backend nào — vẫn set ppadb để hiển thị lỗi sau
            self._type = 'ppadb'

    def get_type(self) -> str:
        return self._type

    def supports_pair(self) -> bool:
        """ppadb không hỗ trợ `adb pair`."""
        return self._type == 'system'

    def run(self, args: list[str], timeout: int = 15) -> tuple[int, str, str]:
        """
        Chạy lệnh ADB.
        args: list arguments (vd: ['devices'], ['-s', 'id', 'shell', 'echo', 'ok'])
        Returns (returncode, stdout, stderr)
        """
        if self._type == 'system':
            return self._system_run(args, timeout)
        return self._ppadb_run(args, timeout)

    def _system_run(self, args: list[str], timeout: int) -> tuple[int, str, str]:
        cmd = ["adb"] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return -1, "", "Timeout"
        except FileNotFoundError:
            return -1, "", "ADB not found"
        except Exception as e:
            return -1, "", str(e)

    def _ppadb_run(self, args: list[str], timeout: int) -> tuple[int, str, str]:
        """
        Xử lý lệnh ADB qua ppadb.
        Các lệnh được hỗ trợ:
          - ['devices']
          - ['connect', 'ip:port']
          - ['-s', 'device_id', 'shell', 'command...']
          - ['-s', 'device_id', 'pull', 'remote', 'local']
        """
        if self._ppadb_client is None:
            return -1, "", "PPADB client not initialized"

        try:
            # === devices ===
            if len(args) == 1 and args[0] == "devices":
                devices = self._ppadb_client.devices()
                lines = ["List of devices attached"]
                for d in devices:
                    serial = getattr(d, 'serial', str(d))
                    lines.append(f"{serial}\tdevice")
                text = "\n".join(lines)
                # fallback nếu devices() rỗng — thử remote_connect devices
                if not devices:
                    pass
                return 0, text, ""

            # === connect ===
            if len(args) >= 2 and args[0] == "connect":
                addr = args[1]
                if ":" in addr:
                    ip, port_str = addr.split(":", 1)
                    port = int(port_str)
                else:
                    ip = addr
                    port = 5555
                self._ppadb_client.remote_connect(ip, port)
                return 0, f"connected to {addr}", ""

            # === pair (KHÔNG hỗ trợ) ===
            if args[0] == "pair":
                return -1, "", "pair not supported in ppadb mode"

            # === -s <serial> shell <cmd...> ===
            if len(args) >= 4 and args[0] == "-s" and args[2] == "shell":
                device_id = args[1]
                command = " ".join(args[3:])
                device = self._ppadb_client.device(device_id)
                if device is None:
                    return -1, "", f"Device {device_id} not found"
                output = device.shell(command, timeout=timeout)
                return 0, (output or "").strip(), ""

            # === -s <serial> pull <remote> <local> ===
            if len(args) >= 5 and args[0] == "-s" and args[2] == "pull":
                device_id = args[1]
                remote = args[3]
                local = args[4]
                device = self._ppadb_client.device(device_id)
                if device is None:
                    return -1, "", f"Device {device_id} not found"
                device.pull(remote, local)
                return 0, f"pulled {remote} to {local}", ""

            return -1, "", f"Unsupported ppadb command: {args}"

        except Exception as e:
            return -1, "", str(e)

    def shell(self, device_id: str, command: str, timeout: int = 15) -> tuple[int, str, str]:
        """Chạy shell command trên thiết bị."""
        return self.run(["-s", device_id, "shell", command], timeout=timeout)

    def pull(self, device_id: str, remote: str, local: str, timeout: int = 15) -> tuple[int, str, str]:
        """Pull file từ thiết bị về local."""
        if self._type == 'system':
            return self._system_run(["-s", device_id, "pull", remote, local], timeout)
        return self._ppadb_run(["-s", device_id, "pull", remote, local], timeout)

    def connect(self, ip: str, port: str) -> tuple[bool, str]:
        """Kết nối đến thiết bị qua TCP/IP."""
        address = f"{ip}:{port}"
        code, stdout, stderr = self.run(["connect", address], timeout=20)
        if code != 0:
            return False, stderr or stdout or "Lỗi không xác định"
        if "connected" in stdout.lower() or "already connected" in stdout.lower():
            return True, stdout.strip()
        return False, stdout.strip()

    def get_connected_devices(self) -> list[str]:
        """Lấy danh sách device_id đã kết nối."""
        code, stdout, stderr = self.run(["devices"])
        if code != 0:
            return []
        devices = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line or line.startswith("List of devices"):
                continue
            if "\tdevice" in line:
                device_id = line.split("\t")[0].strip()
                if device_id:
                    devices.append(device_id)
        return devices

    def check_online(self, device_id: str) -> bool:
        """Kiểm tra thiết bị online bằng shell echo ok."""
        code, stdout, stderr = self.shell(device_id, "echo ok", timeout=8)
        return code == 0 and "ok" in stdout


# Khởi tạo global ADB backend
_adb = _AdbBackend()


# =============================================================================
# ADB DEVICE MANAGEMENT
# =============================================================================

def _adb_run(args: list[str], timeout: int = 15) -> tuple[int, str, str]:
    """Wrapper cho ADB backend — giữ nguyên API cũ."""
    return _adb.run(args, timeout=timeout)


def get_connected_devices() -> list[str]:
    """
    Lấy danh sách device_id đã kết nối ADB (chỉ device đang online).
    Returns list of device_id strings.
    """
    devices = _adb.get_connected_devices()
    if not devices and _adb.get_type() == 'system':
        print(f"  {C.ERROR}❌ Không tìm thấy thiết bị ADB nào.{C.RESET}")
    return devices


def check_device_online(device_id: str) -> bool:
    """
    Kiểm tra xem device có thực sự online và phản hồi không.
    """
    return _adb.check_online(device_id)


def adb_connect_device(ip: str, port: str) -> tuple[bool, str]:
    """Thực hiện `adb connect ip:port`."""
    return _adb.connect(ip, port)


def select_existing_device() -> str | None:
    """
    Hiển thị và cho người dùng chọn từ:
    1. Các device đang kết nối ADB (đã check online)
    2. Các device trong devices.txt (kiểm tra online, xóa nếu không được)
    Returns device_id nếu chọn được.
    """
    # Lấy danh sách device đang online
    connected = get_connected_devices()
    valid_devices = []
    removed_devices = []

    print(f"  {C.INFO}⟳ Đang kiểm tra thiết bị đã kết nối...{C.RESET}")
    for dev in connected:
        if check_device_online(dev):
            valid_devices.append(dev)
        else:
            print(f"  {C.WARNING}⚠️ Device {dev} không phản hồi.{C.RESET}")

    # Đọc devices.txt và kiểm tra
    if os.path.exists(FILE_DEVICES) and os.path.getsize(FILE_DEVICES) > 0:
        with open(FILE_DEVICES, "r") as f:
            saved_devices = [line.strip() for line in f if line.strip()]

        for dev in saved_devices:
            if ":" in dev:
                ip, port = dev.split(":", 1)
            else:
                ip, port = dev, "5555"
            success, _ = _adb.connect(ip, port)
            time.sleep(1)
            if check_device_online(dev):
                if dev not in valid_devices:
                    print(f"  {C.SUCCESS}✅ Device {dev} từ devices.txt kết nối lại được!{C.RESET}")
                    valid_devices.append(dev)
            else:
                print(f"  {C.ERROR}❌ Device {dev} trong devices.txt không kết nối được, sẽ xóa.{C.RESET}")
                removed_devices.append(dev)

    # Xóa device không dùng được khỏi devices.txt
    if removed_devices:
        if os.path.exists(FILE_DEVICES):
            with open(FILE_DEVICES, "r") as f:
                all_saved = [line.strip() for line in f if line.strip()]
            all_saved = [d for d in all_saved if d not in removed_devices]
            with open(FILE_DEVICES, "w") as f:
                for d in all_saved:
                    f.write(d + "\n")
            print(f"  {C.INFO}🗑️ Đã xóa {len(removed_devices)} device không dùng được khỏi {FILE_DEVICES}{C.RESET}")

    if not valid_devices:
        print(f"  {C.WARNING}⚠️ Không có thiết bị nào đang kết nối.{C.RESET}")
        return None

    # Hiển thị danh sách và cho chọn
    print(f"\n  {C.SUCCESS}✅ Thiết bị khả dụng ({len(valid_devices)}):{C.RESET}\n")
    for i, dev in enumerate(valid_devices, 1):
        print(f"  {C.GOLD_1}[{i}]{C.RESET} {C.BOLD}{dev}{C.RESET}")

    print()
    try:
        choice = input(f"  {C.CYAN}└── Chọn thiết bị (1-{len(valid_devices)}) hoặc Enter để quay lại: {C.RESET}").strip()
        if not choice:
            return None
        idx = int(choice) - 1
        if 0 <= idx < len(valid_devices):
            selected = valid_devices[idx]
            print(f"  {C.SUCCESS}✅ Đã chọn: {selected}{C.RESET}")
            with open(FILE_DEVICES, "w") as f:
                f.write(selected)
            return selected
        else:
            print(f"  {C.ERROR}❌ Lựa chọn không hợp lệ.{C.RESET}")
            return None
    except ValueError:
        print(f"  {C.ERROR}❌ Lựa chọn không hợp lệ.{C.RESET}")
        return None


def pair_new_device(ip: str) -> str | None:
    """
    Pair và connect thiết bị mới với retry loop.
    - Nếu dùng system ADB: Pair loop + Connect loop
    - Nếu dùng ppadb: Bỏ qua Pair, chỉ Connect loop
    Returns device_id nếu thành công.
    """
    using_ppadb = _adb.get_type() == 'ppadb'

    if not using_ppadb:
        # === PAIR LOOP (system ADB only) ===
        pair_success = False
        while not pair_success:
            clear_screen()
            print()
            console.print(Align.center(Panel(
                " ",
                title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}PAIR THIẾT BỊ MỚI{C.RESET}"),
                title_align="center",
                border_style="bold #ca80ff",
                box=box.SQUARE,
                padding=(0, 0),
            )))
            print()
            print(f"  {C.INFO}IP: {C.BOLD}{ip}{C.RESET}")
            print(f"  {C.MUTED}  • Vào Wireless Debugging → chọn 'Pair device with pairing code'{C.RESET}")
            print(f"  {C.MUTED}  • Nhập thông tin bên dưới{C.RESET}\n")

            pair_port = input(f"  {C.CYAN}└── Port pair (VD: 39755): {C.RESET}").strip()
            if not pair_port or not pair_port.isdigit():
                print(f"  {C.ERROR}❌ Port không hợp lệ!{C.RESET}")
                time.sleep(1)
                continue

            pair_code = input(f"  {C.CYAN}└── 6-digit Pairing Code: {C.RESET}").strip()
            if not pair_code or not pair_code.isdigit() or len(pair_code) != 6:
                print(f"  {C.ERROR}❌ Pairing code phải là 6 chữ số!{C.RESET}")
                time.sleep(1)
                continue

            print(f"\n  {C.GOLD_1}⟳ Đang pair với {ip}:{pair_port}...{C.RESET}")
            retcode, stdout, stderr = _adb_run(["pair", f"{ip}:{pair_port}", pair_code], timeout=25)

            if retcode == 0 and ("Successfully paired" in stdout or "success" in stdout.lower()):
                print(f"  {C.SUCCESS}✅ Pair thành công!{C.RESET}")
                pair_success = True
            else:
                error_msg = stderr or stdout or "Lỗi không xác định"
                print(f"  {C.ERROR}❌ Pair thất bại: {error_msg}{C.RESET}")
                retry = input(f"\n  {C.YELLOW}└── Thử lại pair? (Enter=thử lại, n=thoát): {C.RESET}").strip().lower()
                if retry == 'n':
                    print(f"  {C.ERROR}❌ Đã hủy pair thiết bị.{C.RESET}")
                    return None
                time.sleep(1)
    else:
        # ppadb mode: thông báo bỏ qua pair
        clear_screen()
        print()
        console.print(Align.center(Panel(
            " ",
            title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}KẾT NỐI TRỰC TIẾP{C.RESET}"),
            title_align="center",
            border_style="bold #ca80ff",
            box=box.SQUARE,
            padding=(0, 0),
        )))
        print()
        print(f"  {C.INFO}IP: {C.BOLD}{ip}{C.RESET}")
        print(f"  {C.MUTED}  • Chế độ pure-python-adb: bỏ qua bước Pair{C.RESET}")
        print(f"  {C.MUTED}  • Nhập port kết nối trực tiếp (thường là 5555){C.RESET}\n")

    # === CONNECT LOOP ===
    connect_success = False
    device_id = None
    while not connect_success:
        if not using_ppadb:
            clear_screen()
            print()
            console.print(Align.center(Panel(
                " ",
                title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}KẾT NỐI THIẾT BỊ{C.RESET}"),
                title_align="center",
                border_style="bold #ca80ff",
                box=box.SQUARE,
                padding=(0, 0),
            )))
            print()
            print(f"  {C.INFO}IP: {C.BOLD}{ip}{C.RESET} (đã pair thành công){C.RESET}\n")
        else:
            clear_screen()
            print()
            console.print(Align.center(Panel(
                " ",
                title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}KẾT NỐI THIẾT BỊ{C.RESET}"),
                title_align="center",
                border_style="bold #ca80ff",
                box=box.SQUARE,
                padding=(0, 0),
            )))
            print()
            print(f"  {C.INFO}IP: {C.BOLD}{ip}{C.RESET}{C.RESET}\n")

        connect_port = input(f"  {C.CYAN}└── Port connect (VD: 36091 hoặc 5555): {C.RESET}").strip()
        if not connect_port or not connect_port.isdigit():
            print(f"  {C.ERROR}❌ Port không hợp lệ!{C.RESET}")
            time.sleep(1)
            continue

        success, msg = adb_connect_device(ip, connect_port)
        if success:
            device_id = f"{ip}:{connect_port}"
            print(f"  {C.SUCCESS}✅ Connect thành công: {device_id}{C.RESET}")
            connect_success = True
        else:
            print(f"  {C.ERROR}❌ Connect thất bại: {msg}{C.RESET}")
            retry = input(f"\n  {C.YELLOW}└── Thử lại connect? (Enter=thử lại, n=thoát): {C.RESET}").strip().lower()
            if retry == 'n':
                print(f"  {C.ERROR}❌ Đã hủy kết nối thiết bị.{C.RESET}")
                return None
            time.sleep(1)

    # Lưu device
    with open(FILE_DEVICES, "w") as f:
        f.write(device_id)
    print(f"  {C.INFO}💾 Đã lưu device vào {FILE_DEVICES}{C.RESET}")

    # Verify
    print(f"  {C.INFO}⟳ Đang kiểm tra kết nối device...{C.RESET}")
    time.sleep(2)
    if check_device_online(device_id):
        print(f"  {C.SUCCESS}✅ Device online và sẵn sàng!{C.RESET}")
    else:
        print(f"  {C.WARNING}⚠️ Device đã connect nhưng chưa phản hồi.{C.RESET}")
    time.sleep(1)

    return device_id


def connect_device_with_retry() -> str:
    """
    Kết nối thiết bị ADB với retry loop.
    - Hỏi dùng device cũ hay pair mới
    - Nếu device cũ không được → chuyển sang pair mới
    - Pair loop đến khi được
    - Connect loop đến khi được
    Returns device_id.
    """
    using_ppadb = _adb.get_type() == 'ppadb'
    pair_label = "Connect thiết bị mới" if using_ppadb else "Pair & Connect thiết bị mới"

    while True:
        clear_screen()
        idlerhatool()
        print()
        console.print(Align.center(Panel(
            " ",
            title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}KẾT NỐI THIẾT BỊ ADB{C.RESET}"),
            title_align="center",
            border_style="bold #ca80ff",
            box=box.SQUARE,
            padding=(0, 0),
        )))
        print()
        print(f"  {C.GOLD_1}[1]{C.RESET} {C.BOLD}Sử dụng thiết bị đã kết nối{C.RESET}")
        print(f"  {C.GOLD_1}[2]{C.RESET} {C.BOLD}{pair_label}{C.RESET}\n")

        choice = input(f"  {C.CYAN}└── Chọn (1/2): {C.RESET}").strip()

        if choice == "1":
            device = select_existing_device()
            if device:
                return device
            print(f"\n  {C.WARNING}⚠️ Không thể dùng thiết bị cũ. Chuyển sang kết nối mới...{C.RESET}")
            time.sleep(1.5)
        elif choice == "2":
            pass  # Tiếp tục xuống phần kết nối mới
        else:
            print(f"\n  {C.ERROR}❌ Lựa chọn không hợp lệ! Vui lòng chọn 1 hoặc 2.{C.RESET}")
            time.sleep(1.5)
            continue

        # === Kết nối mới (choice 2 hoặc fallback từ choice 1) ===
        clear_screen()
        print()
        console.print(Align.center(Panel(
            " ",
            title=Text.from_ansi(f"{C.BOLD}{C.PRIMARY}THIẾT LẬP KẾT NỐI MỚI{C.RESET}"),
            title_align="center",
            border_style="bold #ca80ff",
            box=box.SQUARE,
            padding=(0, 0),
        )))
        print()
        ip = input(f"  {C.CYAN}└── IP điện thoại (VD: 192.168.1.10): {C.RESET}").strip()
        if not ip:
            print(f"  {C.ERROR}❌ IP không hợp lệ!{C.RESET}")
            time.sleep(1)
            continue

        device = pair_new_device(ip)
        if device:
            return device

        # Nếu pair/connect thất bại, hỏi có muốn thử lại không
        retry = input(f"\n  {C.YELLOW}└── Kết nối thất bại hoàn toàn. Thử lại? (Enter=thử lại, n=thoát): {C.RESET}").strip().lower()
        if retry == 'n':
            print(f"  {C.ERROR}❌ Không thể kết nối thiết bị. Thoát.{C.RESET}")
            sys.exit(1)
        time.sleep(1)


# =============================================================================
# TIKTOK AUTOMATION
# =============================================================================

def get_screen_size(device_id: str) -> tuple[int, int]:
    """Lấy kích thước màn hình thiết bị."""
    code, stdout, stderr = _adb.shell(device_id, "wm size")
    if code != 0:
        return 1080, 1920  # fallback
    try:
        res_str = stdout.split(": ")[1].strip().split('x')
        return int(res_str[0]), int(res_str[1])
    except Exception:
        return 1080, 1920


def tap_at_ratio(device_id: str, ratio_str: str) -> bool:
    try:
        ratio_x, ratio_y = map(float, ratio_str.split(","))
        width, height = get_screen_size(device_id)
        x = int(width * ratio_x)
        y = int(height * ratio_y)
        rx = x + random.randint(-5, 5)
        ry = y + random.randint(-5, 5)
        _adb.shell(device_id, f"input tap {rx} {ry}")
        return True
    except Exception as e:
        print(f"  Lỗi tap ratio: {e}")
        return False


def read_click_config() -> dict[str, str]:
    if not os.path.exists(FILE_CLICK):
        return {"follow_user": "0.277, 0.36"}
    data = {}
    with open(FILE_CLICK, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key = line.split("=")[0].strip()
                value = line.split("=")[1].strip().strip('"')
                data[key] = value
    return data


def _is_valid_username(username: str) -> bool:
    """Kiểm tra username TikTok có hợp lệ không (bỏ qua user ID dạng số)."""
    if not username:
        return False
    # User ID toàn số (19 digits) → không phải @username
    if username.isdigit():
        return False
    # Username TikTok: 2-30 ký tự, chứa chữ/số/dấu gạch
    if len(username) < 2 or len(username) > 30:
        return False
    return True


def extract_username_from_link(link: str | None) -> str | None:
    """
    Trích xuất @username từ link Golike API.
    Chỉ trả về nếu tìm thấy @username hợp lệ, không lấy user ID dạng số.
    """
    if not link:
        return None

    link = link.strip()

    # Pattern: @username anywhere in the link (TikTok profile/video URL)
    match = re.search(r"@([a-zA-Z0-9_.]+)", link)
    if match:
        username = match.group(1)
        if _is_valid_username(username):
            return username

    # Không tìm thấy @username hợp lệ
    return None


def open_tiktok_profile(device_id: str, username: str) -> bool:
    if not username:
        return False
    uri = f"snssdk1180://user/profile?unique_id={username}"
    try:
        code, stdout, stderr = _adb.shell(
            device_id,
            f"am start -a android.intent.action.VIEW -d '{uri}' com.ss.android.ugc.trill",
            timeout=20
        )
        return code == 0
    except Exception:
        return False


def resolve_short_link(link: str) -> str | None:
    """Follow redirect của TikTok short link (vt.tiktok.com/xxx) để lấy URL đầy đủ."""
    if not link:
        return None
    link = link.strip()
    if "vt.tiktok.com" not in link and "vm.tiktok.com" not in link:
        return link  # Không phải short link, trả về nguyên bản
    try:
        cmd = ["curl", "-s", "-L", "--max-time", "10", "-o", "/dev/null", "-w", "%{url_effective}", link]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        resolved = result.stdout.strip()
        if resolved and resolved != link:
            return resolved
        return link
    except Exception:
        return link


def extract_video_id_from_link(link: str | None, *, resolve_short: bool = True) -> str | None:
    """Trích xuất video ID từ link TikTok (/video/12345).
    
    Nếu resolve_short=True và link là short link (vt.tiktok.com, vm.tiktok.com),
    tự động follow redirect để lấy URL đầy đủ trước khi extract.
    """
    if not link:
        return None
    link = link.strip()
    
    # Nếu là short link, resolve trước
    if resolve_short and ("vt.tiktok.com" in link or "vm.tiktok.com" in link):
        resolved = resolve_short_link(link)
        if resolved and resolved != link:
            # Thử extract từ URL đã resolve
            match = re.search(r"/video/(\d+)", resolved)
            if match:
                return match.group(1)
    
    # Pattern: tiktok.com/@username/video/12345 hoặc /video/12345
    match = re.search(r"/video/(\d+)", link)
    if match:
        return match.group(1)
    return None


def open_tiktok_video(device_id: str, video_id: str) -> bool:
    """Mở video TikTok bằng deeplink."""
    if not video_id:
        return False
    uri = f"snssdk1180://video/detail?item_id={video_id}"
    try:
        code, stdout, stderr = _adb.shell(
            device_id,
            f"am start -a android.intent.action.VIEW -d '{uri}' com.ss.android.ugc.trill",
            timeout=20
        )
        return code == 0
    except Exception:
        return False


# =============================================================================
# UI DETECTION
# =============================================================================

def dump_ui(device_id: str) -> bool:
    if os.path.exists(UI_XML_LOCAL):
        try:
            os.remove(UI_XML_LOCAL)
        except OSError:
            pass

    # Dump UI
    _adb.shell(device_id, "uiautomator dump --compressed /sdcard/ui.xml", timeout=15)

    # Pull file
    code, _, _ = _adb.pull(device_id, "/sdcard/ui.xml", f"./{UI_XML_LOCAL}", timeout=15)
    if code == 0 and os.path.exists(UI_XML_LOCAL) and os.path.getsize(UI_XML_LOCAL) > 0:
        return True

    # Fallback: cat the file
    if code != 0:
        code2, stdout2, _ = _adb.shell(device_id, "cat /sdcard/ui.xml", timeout=15)
        if code2 == 0 and stdout2.strip():
            with open(UI_XML_LOCAL, "w", encoding="utf-8") as f:
                f.write(stdout2)
            if os.path.getsize(UI_XML_LOCAL) > 0:
                return True
    return False


def find_follow_button(keywords=("Follow", "Following", "Theo dõi")):
    if not os.path.exists(UI_XML_LOCAL):
        return None
    try:
        tree = ET.parse(UI_XML_LOCAL)
        root = tree.getroot()
        candidates = []
        for node in root.iter("node"):
            text = node.attrib.get("text", "").strip()
            content_desc = node.attrib.get("content-desc", "").strip()
            bounds = node.attrib.get("bounds", "")
            res_id = node.attrib.get("resource-id", "")
            target = (text + " " + content_desc).strip()
            if not target:
                continue
            if any(kw.lower() == target.lower() for kw in keywords):
                match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
                if match:
                    x1, y1, x2, y2 = map(int, match.groups())
                    x = (x1 + x2) // 2
                    y = (y1 + y2) // 2
                    candidates.append((x, y, res_id))
        for x, y, rid in candidates:
            if re.search(r":id/[a-z0-9]{2,4}$", rid):
                return (x, y)
        if candidates:
            return (candidates[0][0], candidates[0][1])
        return None
    except ET.ParseError:
        return None
    except Exception:
        return None


def find_like_button():
    """Tìm nút Like/Thích/Tim trên màn hình video TikTok."""
    if not os.path.exists(UI_XML_LOCAL):
        return None
    try:
        tree = ET.parse(UI_XML_LOCAL)
        root = tree.getroot()
        for node in root.iter("node"):
            text = node.attrib.get("text", "").strip()
            content_desc = node.attrib.get("content-desc", "").strip()
            bounds = node.attrib.get("bounds", "")
            target = (text + " " + content_desc).strip().lower()
            if not target:
                continue
            # Kiểm tra từ khóa Like (hỗ trợ nhiều ngôn ngữ)
            if any(kw in target for kw in ["like", "thích", "tim", "heart", "yêu thích"]):
                match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
                if match:
                    x1, y1, x2, y2 = map(int, match.groups())
                    x = (x1 + x2) // 2
                    y = (y1 + y2) // 2
                    return (x, y)
        return None
    except ET.ParseError:
        return None
    except Exception:
        return None


def find_share_button():
    """Tìm nút Share/Chia sẻ trên màn hình video TikTok."""
    if not os.path.exists(UI_XML_LOCAL):
        return None
    try:
        tree = ET.parse(UI_XML_LOCAL)
        root = tree.getroot()
        for node in root.iter("node"):
            text = node.attrib.get("text", "").strip()
            content_desc = node.attrib.get("content-desc", "").strip()
            bounds = node.attrib.get("bounds", "")
            target = (text + " " + content_desc).strip().lower()
            if not target:
                continue
            # Kiểm tra từ khóa Share (hỗ trợ nhiều ngôn ngữ)
            if any(kw in target for kw in ["share", "chia sẻ", "gửi", "chuyển tiếp", "send to"]):
                match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
                if match:
                    x1, y1, x2, y2 = map(int, match.groups())
                    x = (x1 + x2) // 2
                    y = (y1 + y2) // 2
                    return (x, y)
        return None
    except ET.ParseError:
        return None
    except Exception:
        return None


def like_current_video(device_id: str) -> bool:
    """Like video TikTok đang mở bằng UI detection."""
    time.sleep(3)  # Chờ video load

    for attempt in range(3):
        if dump_ui(device_id):
            pos = find_like_button()
            if pos:
                x, y = pos
                result = tap_at(device_id, x, y)
                cleanup_ui()
                return result
            time.sleep(2)
    cleanup_ui()
    return False


def share_current_video(device_id: str) -> bool:
    """Share video TikTok đang mở bằng UI detection."""
    time.sleep(3)  # Chờ video load

    for attempt in range(3):
        if dump_ui(device_id):
            pos = find_share_button()
            if pos:
                x, y = pos
                result = tap_at(device_id, x, y)
                cleanup_ui()
                # Đợi share sheet hiện lên rồi nhấn Back để đóng
                time.sleep(2)
                _adb.shell(device_id, "input keyevent KEYCODE_BACK")
                time.sleep(1)
                return result
            time.sleep(2)
    cleanup_ui()
    return False


def tap_at(device_id: str, x: int, y: int) -> bool:
    try:
        rx = x + random.randint(-3, 3)
        ry = y + random.randint(-3, 3)
        _adb.shell(device_id, f"input tap {rx} {ry}")
        return True
    except Exception:
        return False


def cleanup_ui():
    if os.path.exists(UI_XML_LOCAL):
        try:
            os.remove(UI_XML_LOCAL)
        except OSError:
            pass


def follow_tiktok_user(device_id: str, username: str, follow_ratio: str | None = None, wait_time: int = 8) -> bool:
    if follow_ratio is None:
        config = read_click_config()
        follow_ratio = config.get("follow_user", "0.277, 0.36")

    open_tiktok_profile(device_id, username)
    time.sleep(wait_time)

    # UI detection để tìm nút Follow
    if dump_ui(device_id):
        pos = find_follow_button()
        if pos:
            x, y = pos
            result = tap_at(device_id, x, y)
            cleanup_ui()
            return result
        time.sleep(2)
        if dump_ui(device_id):
            pos = find_follow_button()
            if pos:
                x, y = pos
                result = tap_at(device_id, x, y)
                cleanup_ui()
                return result
    cleanup_ui()
    return tap_at_ratio(device_id, follow_ratio)


# =============================================================================
# SEASON DISPLAY
# =============================================================================

def _center_indent(text_width: int) -> str:
    """Tính số spaces để căn giữa nội dung có độ rộng text_width."""
    screen_width = console.size.width
    padding = max(0, (screen_width - text_width) // 2)
    return " " * padding


def show_season_status(season: int, device_id: str, acc_nickname: str,
                       acc_username: str, job_done: int, total_jobs: int,
                       username: str, remaining_seconds: int,
                       job_type: str = "FOLLOW"):
    """Hiển thị bảng trạng thái season (xóa màn hình trước khi hiển thị)."""
    clear_screen()
    idlerhatool()
    W = 52
    indent = _center_indent(W)
    print(f"{indent}{C.BOLD}{C.PRIMARY}┌{'─' * (W - 2)}┐{C.RESET}")
    title = " SEASON STATUS "
    print(f"{indent}{C.BOLD}{C.PRIMARY}│  {title.center(W - 6)}  │{C.RESET}")
    print(f"{indent}{C.BOLD}{C.PRIMARY}└{'─' * (W - 2)}┘{C.RESET}")
    print()
    print(f"{indent}{C.GOLD_1}Season:{C.RESET}          {C.BOLD}{season}{C.RESET}")
    print(f"{indent}{C.GOLD_1}Device:{C.RESET}          {device_id}")
    print(f"{indent}{C.GOLD_1}Account:{C.RESET}         {acc_username}")
    print(f"{indent}{C.GOLD_1}Account Tiktok:{C.RESET}  {acc_nickname}")
    print(f"{indent}{C.GOLD_1}Job:{C.RESET}             {job_type.upper()} ({job_done}/{total_jobs})")
    print(f"{indent}{C.GOLD_1}Username:{C.RESET}        {username}")
    mins, secs = divmod(max(0, remaining_seconds), 60)
    remaining_formatted = f"{mins:02d}:{secs:02d}"
    print(f"{indent}{C.GOLD_1}Remaining time:{C.RESET}  {remaining_formatted}")
    print()
    print(f"{indent}{C.PRIMARY}└{'─' * (W - 2)}┘{C.RESET}")


def show_season_wait(season: int, remaining_seconds: int):
    """Hiển thị màn hình chờ giữa các season (xóa màn hình trước)."""
    clear_screen()
    idlerhatool()
    W = 52
    indent = _center_indent(W)
    print(f"{indent}{C.BOLD}{C.PRIMARY}┌{'─' * (W - 2)}┐{C.RESET}")
    title = " SEASON ENDED  "
    print(f"{indent}{C.BOLD}{C.PRIMARY}│{title.center(W - 6)}  │{C.RESET}")
    print(f"{indent}{C.BOLD}{C.PRIMARY}└{'─' * (W - 2)}┘{C.RESET}")
    print()
    print(f"{indent}{C.GOLD_1}Season:{C.RESET}          {C.BOLD}{season} wait{C.RESET}")
    mins, secs = divmod(max(0, remaining_seconds), 60)
    remaining_formatted = f"{mins:02d}:{secs:02d}"
    print(f"{indent}{C.GOLD_1}Remaining time to{C.RESET}")
    print(f"{indent}{C.GOLD_1}continue next season:{C.RESET}  {remaining_formatted}")
    print()
    print(f"{indent}{C.PRIMARY}└{'─' * (W - 2)}┘{C.RESET}")


# =============================================================================
# AUTO SEASON BOT
# =============================================================================

def run_auto_season(device_id: str, account_id: int | None, account_info: dict[str, Any] | None):
    """
    Chạy auto season với hiển thị bảng đẹp.
    """
    JOBS_PER_SEASON = 5
    SEASON_WAIT = 300
    PAUSE_BETWEEN_JOBS = 10
    season = 1
    seen_jobs: set[Any] = set()

    indent = _center_indent(52)
    acc_nickname = account_info.get('nickname', f'Acc#{account_id}') if account_info else f'Acc#{account_id}'
    acc_username = account_info.get('username', '?') if account_info else '?'

    try:
        while True:
            completed = 0

            while completed < JOBS_PER_SEASON:
                # Tìm job mới
                current_job = None
                while current_job is None:
                    jobs, err = get_jobs(account_id=account_id)
                    if err:
                        # Hiển thị lỗi trên status
                        clear_screen()
                        print(f"\n{indent}{C.ERROR}⚠️ Lỗi API: {err}{C.RESET}")
                        time.sleep(5)
                    else:
                        for j in jobs:
                            jid = j.get("id")
                            if jid and jid not in seen_jobs:
                                current_job = j
                                break
                    if current_job is None:
                        clear_screen()
                        idlerhatool()
                        print(f"\n{C.INFO}⏳ Đang chờ job mới...{C.RESET}")
                        time.sleep(5)

                # Lấy thông tin job
                job_id = current_job["id"]
                link = current_job.get("link", "")
                print(f"{indent}{C.INFO}📎 Link gốc từ API: {link}{C.RESET}")

                acc_id = current_job.get("_account_id")
                ads_id = current_job.get("id")
                object_id = current_job.get("object_id", "")
                jtype = current_job.get("type", "?").lower()

                # --- Phân loại job: follow hay video/like ---
                is_video_job = jtype in ("like", "view", "video", "favorites")
                is_follow_job = jtype == "follow"
                is_share_job = jtype == "share"

                display_name = "?"
                success = False

                if is_video_job:
                    # === VIDEO/LIKE/FAVORITES JOB ===
                    video_id = object_id or extract_video_id_from_link(link, resolve_short=True)
                    if not video_id:
                        print(f"{indent}{C.WARNING}⚠️ Job #{job_id} không có video ID, bỏ qua...{C.RESET}")
                        seen_jobs.add(job_id)
                        time.sleep(2)
                        continue

                    seen_jobs.add(job_id)
                    display_name = video_id

                    # Hiển thị trạng thái
                    show_season_status(
                        season, device_id, acc_nickname, acc_username,
                        completed + 1, JOBS_PER_SEASON, f"video:{video_id}", 0,
                        job_type=jtype
                    )

                    # Mở video & like
                    print(f"\n{indent}{C.INFO}🎬 Đang mở video {video_id} & like...{C.RESET}")
                    open_ok = open_tiktok_video(device_id, video_id)
                    time.sleep(5)
                    if open_ok:
                        like_ok = like_current_video(device_id)
                        if like_ok:
                            print(f"{indent}{C.SUCCESS}✅ Đã like video {video_id}{C.RESET}")
                            success = True
                        else:
                            print(f"{indent}{C.WARNING}⚠️ Không tìm thấy nút Like, vẫn complete job...{C.RESET}")
                            success = True  # Vẫn complete job kể cả không like được UI
                    else:
                        print(f"{indent}{C.ERROR}❌ Không mở được video {video_id}{C.RESET}")
                        success = False

                elif is_share_job:
                    # === SHARE JOB ===
                    video_id = object_id or extract_video_id_from_link(link, resolve_short=True)
                    if not video_id:
                        print(f"{indent}{C.WARNING}⚠️ Job #{job_id} không có video ID, bỏ qua...{C.RESET}")
                        seen_jobs.add(job_id)
                        time.sleep(2)
                        continue

                    seen_jobs.add(job_id)
                    display_name = video_id

                    # Hiển thị trạng thái
                    show_season_status(
                        season, device_id, acc_nickname, acc_username,
                        completed + 1, JOBS_PER_SEASON, f"share:{video_id}", 0,
                        job_type=jtype
                    )

                    # Mở video & share
                    print(f"\n{indent}{C.INFO}📤 Đang mở video {video_id} & chia sẻ...{C.RESET}")
                    open_ok = open_tiktok_video(device_id, video_id)
                    time.sleep(5)
                    if open_ok:
                        share_ok = share_current_video(device_id)
                        if share_ok:
                            print(f"{indent}{C.SUCCESS}✅ Đã chia sẻ video {video_id}{C.RESET}")
                            success = True
                        else:
                            print(f"{indent}{C.WARNING}⚠️ Không tìm thấy nút Share, vẫn complete job...{C.RESET}")
                            success = True
                    else:
                        print(f"{indent}{C.ERROR}❌ Không mở được video {video_id}{C.RESET}")
                        success = False

                elif is_follow_job:
                    # === FOLLOW JOB ===
                    username = extract_username_from_link(link)
                    if not username:
                        print(f"{indent}{C.WARNING}⚠️ Job #{job_id} không có username hợp lệ, bỏ qua...{C.RESET}")
                        seen_jobs.add(job_id)
                        time.sleep(2)
                        continue

                    seen_jobs.add(job_id)
                    display_name = username

                    # Hiển thị trạng thái
                    show_season_status(
                        season, device_id, acc_nickname, acc_username,
                        completed + 1, JOBS_PER_SEASON, username, 0,
                        job_type=jtype
                    )

                    # Follow user
                    print(f"\n{indent}{C.INFO}🔍 Đang follow @{username}...{C.RESET}")
                    success = follow_tiktok_user(device_id, username, wait_time=8)
                else:
                    # === UNKNOWN JOB TYPE ===
                    print(f"{indent}{C.WARNING}⚠️ Job #{job_id} có type '{jtype}' không hỗ trợ, bỏ qua...{C.RESET}")
                    seen_jobs.add(job_id)
                    time.sleep(2)
                    continue

                # --- Hoàn thành job ---
                job_ok = False
                if success:
                    if acc_id and ads_id:
                        print(f"{indent}{C.INFO}📤 Đang hoàn thành job #{ads_id}...{C.RESET}")
                        ok, msg, _ = complete_job(ads_id, acc_id, object_id, jtype)
                        if ok:
                            print(f"{indent}{C.SUCCESS}✅ Job #{ads_id} hoàn thành!{C.RESET}")
                            job_ok = True
                        else:
                            print(f"{indent}{C.ERROR}❌ Lỗi hoàn thành job #{ads_id}: {msg}{C.RESET}")
                    else:
                        print(f"{indent}{C.SUCCESS}✅ Thao tác thành công!{C.RESET}")
                        job_ok = True

                    if job_ok:
                        completed += 1
                        print(f"{indent}{C.SUCCESS}✅ Tiến độ: {completed}/{JOBS_PER_SEASON}{C.RESET}")
                    else:
                        print(f"{indent}{C.WARNING}⚠️ Job chưa hoàn thành, sẽ thử lại sau...{C.RESET}")
                        seen_jobs.discard(job_id)
                else:
                    print(f"{indent}{C.ERROR}❌ Thao tác thất bại, sẽ thử lại sau...{C.RESET}")
                    seen_jobs.discard(job_id)

                # Countdown giữa các job
                if completed < JOBS_PER_SEASON:
                    for i in range(PAUSE_BETWEEN_JOBS, 0, -1):
                        show_season_status(
                            season, device_id, acc_nickname, acc_username,
                            completed, JOBS_PER_SEASON, display_name, i,
                            job_type=jtype
                        )
                        print(f"\n{indent}{C.INFO}⏳ Chờ job tiếp theo...{C.RESET}")
                        time.sleep(1)

            # Season hoàn thành → chờ 5 phút
            for i in range(SEASON_WAIT, 0, -1):
                show_season_wait(season + 1, i)
                time.sleep(1)

            completed = 0
            seen_jobs = set()
            season += 1

    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{indent}{C.WARNING}🛑 Cảm ơn bạn đã sử dụng tool.{C.RESET}\n")
        sys.exit(0)


# =============================================================================
# MAIN - CHẠY TRỰC TIẾP, KHÔNG MENU
# =============================================================================

def main():
    try:
        # Bước 1: Auto cài đặt dependencies
        auto_install_dependencies()

        # Bước 2: Kiểm tra và tạo file cần thiết
        clear_screen()
        ensure_required_files()

        # Bước 3: Authorization
        load_or_request_authorization()

        # Bước 4: Chọn tài khoản TikTok
        account_id, account_info = select_tiktok_account()

        # Bước 5: Kết nối ADB (với retry loop)
        device_id = connect_device_with_retry()

        # Bước 6: Chạy auto season
        run_auto_season(device_id, account_id, account_info)

    except KeyboardInterrupt:
        clear_screen()
        print(f"\n  {C.WARNING}🛑 Đã dừng bởi người dùng.{C.RESET}\n")
        sys.exit(0)




if __name__ == "__main__":
    main()
