#!/usr/bin/env python3
import sys, os, json, datetime, time, urllib.parse, shutil
from pathlib import Path

from PyQt6.QtCore import (
    QUrl, QSize, Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QPoint,
    QSequentialAnimationGroup, QParallelAnimationGroup, QRectF, QEvent, QStandardPaths
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QTabWidget, QLineEdit, QProgressBar, QDialog,
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QToolButton, QTreeWidget, QTreeWidgetItem,
    QFileDialog, QMessageBox, QPushButton, QStatusBar, QMenu, QSizePolicy, QFontDialog,
    QComboBox, QCheckBox, QInputDialog, QDockWidget, QGraphicsOpacityEffect, QWidgetAction
)
from PyQt6.QtGui import (
    QIcon, QAction, QDesktopServices, QFont, QShortcut, QKeySequence, QPixmap, QPainter, QPainterPath, QCursor, QGuiApplication, QMovie, QFont, QFontDatabase, QPalette, QColor
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile, QWebEnginePage, QWebEngineScript, QWebEngineDownloadRequest,
    QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo, QWebEngineFullScreenRequest, QWebEngineSettings
)

# -------------------- Paths and Configuration --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIGS_DIR = os.path.join(BASE_DIR, "configs")
os.makedirs(CONFIGS_DIR, exist_ok=True)

ICONS_DIR = os.path.join(BASE_DIR, "icons")
HISTORY_FILE = os.path.join(CONFIGS_DIR, "history.json")
DOWNLOADS_FILE = os.path.join(CONFIGS_DIR, "downloads.json")
SETTINGS_FILE = os.path.join(CONFIGS_DIR, "settings.json")
EXTENSIONS_FILE = os.path.join(CONFIGS_DIR, "extensions.json")
BOOKMARKS_FILE = os.path.join(CONFIGS_DIR, "bookmarks.json")
EXCEPTIONS_FILE = os.path.join(CONFIGS_DIR, "exceptions.json")

# Альтернативный путь (site/global/assets/config/settings.json)
ALT_CONFIG_DIR = os.path.join(BASE_DIR, "site", "global", "assets", "config")
ALT_SETTINGS_FILE = os.path.join(ALT_CONFIG_DIR, "settings.json")

EXTENSIONS_DIR = os.path.join(BASE_DIR, "extensions")
os.makedirs(EXTENSIONS_DIR, exist_ok=True)

USER_SCRIPT_FILE = os.path.join(EXTENSIONS_DIR, "adblock.js")
DARKREADER_FILE = os.path.join(EXTENSIONS_DIR, "darkreader.js")


ENGINE_URLS = {
    "google": "https://www.google.com/search?q=",
    "yandex": "https://yandex.ru/search/?text=",
    "bing": "https://www.bing.com/search?q=",
    "duckduckgo": "https://duckduckgo.com/?q="
}

LANGS = ["ru", "en"]
TRANSLATIONS = {
    "ru": {
        "new_tab": "Новая вкладка",
        "new_window": "Новое окно",
        "private_on": "Новое приватное окно",
        "private_off": "Вернуться в обычный режим",
        "history": "История",
        "downloads": "Загрузки",
        "settings": "Настройки",
        "extensions": "Расширения",
        "exit": "Выход",
        "browser_title": "MiHa Browser",
        "search_engine": "Поисковая система",
        "language": "Язык",
        "font": "Шрифт",
        "homepage": "Домашняя страница",
        "settings_title": "Настройки",
        "restart_info": "Для применения изменений перезапустите браузер.",
        "download_mode": "Режим загрузки",
        "ask": "Спрашивать каждый раз",
        "default": "Папка загрузок по умолчанию",
        "custom": "Кастомный путь",
        "custom_download_path": "Путь загрузок (при Кастом)",
        "delete_on_close": "Удалять куки и данные сайтов при закрытии браузера",
        "cookies_data": "Куки и данные сайтов",
        "cookies_data_info": "Ваши куки, данные сайтов и кэш занимают ~{} MB.",
        "delete_data": "Удалить данные…",
        "manage_data": "Управление данными…",
        "manage_exceptions": "Управление исключениями…",
        "extensions_title": "Расширения (JS-скрипты)",
        "extensions_add": "Добавить",
        "extensions_remove": "Удалить",
        "extensions_toggle": "Вкл/Выкл",
        "extensions_need_restart": "Для применения новых скриптов перезапустите браузер.",
        "default_extension_description": "AdBlock разработан MiHaTsKiYi специально для MiHa Browser",
        "bookmarks": "Закладки",
        "add_bookmark": "Добавить закладку",
        "manage_bookmarks": "Управлять закладками",
        "bookmarks_title": "Мои закладки",
        "set_default_browser": "Сделать браузером по умолчанию",
        "welcome_title": "Добро пожаловать!",
        "welcome_text": "Спасибо, что выбрали MiHa Browser.\nНажмите «Настройки», чтобы настроить браузер по своему вкусу.",
        "open_settings": "Открыть настройки",
        "close": "Закрыть"
    },
    "en": {
        "new_tab": "New Tab",
        "new_window": "New Window",
        "private_on": "New Private Window",
        "private_off": "Return to Normal Mode",
        "history": "History",
        "downloads": "Downloads",
        "settings": "Settings",
        "extensions": "Extensions",
        "exit": "Exit",
        "browser_title": "MiHa Browser",
        "search_engine": "Search Engine",
        "language": "Language",
        "font": "Font",
        "homepage": "Homepage",
        "settings_title": "Settings",
        "restart_info": "Please restart the browser to apply new scripts.",
        "download_mode": "Download Mode",
        "ask": "Ask each time",
        "default": "Default Downloads Folder",
        "custom": "Custom Path",
        "custom_download_path": "Custom Download Path",
        "delete_on_close": "Delete cookies and site data when closing browser",
        "cookies_data": "Cookies and Site Data",
        "cookies_data_info": "Your cookies, site data, and cache are using ~{} MB.",
        "delete_data": "Delete Data…",
        "manage_data": "Manage Data…",
        "manage_exceptions": "Manage Exceptions…",
        "extensions_title": "Extensions (JS scripts)",
        "extensions_add": "Add",
        "extensions_remove": "Remove",
        "extensions_toggle": "Toggle On/Off",
        "extensions_need_restart": "Please restart the browser to apply new scripts.",
        "default_extension_description": "AdBlock is an adblock developed by MiHaTsKiYi specifically for MiHa Browser",
        "bookmarks": "Bookmarks",
        "add_bookmark": "Add Bookmark",
        "manage_bookmarks": "Manage Bookmarks",
        "bookmarks_title": "My Bookmarks",
        "set_default_browser": "Set as default browser",
        "welcome_title": "Welcome!",
        "welcome_text": "Thank you for choosing MiHa Browser.\nClick 'Settings' to customize your browser.",
        "open_settings": "Open Settings",
        "close": "Close"
    }
}


# Встроенное расширение: Google Dark (UserScript)
GOOGLE_DARK_EXTENSION = """// ==UserScript==
// @name         Google Dark
// @version      0.3
// @description  Google dark theme.
// @author       ekin@gmx.us
// @namespace    https://greasyfork.org/en/users/6473-ekin
// @include      /^https?://www\\.google\\.[a-z\\.]+/.*/
// @grant        none
// @require      https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js
// @downloadURL  https://update.greasyfork.org/scripts/6666/Google%20Dark.user.js
// @updateURL    https://update.greasyfork.org/scripts/6666/Google%20Dark.meta.js
// ==/UserScript==

function initStyle() {
    jQuery("html, body").css("color", "#666");
    jQuery("html, body").css("background-color", "#2C2C2C");
    jQuery(".fbar").css("background-color", "#2C2C2C");
    jQuery("#fbar").css("background-color", "#2C2C2C");
    jQuery("#fbar").css("border-top", "1px solid #494949");
    jQuery("#topabar").css("background-color", "#2C2C2C");
    jQuery("#hdtbSum").css("border-bottom", "1px solid #494949");
    jQuery("#center_col ._Ak").css("border-bottom", "1px solid #494949");
    jQuery("a:visited").css("color", "#fff");
    jQuery("a").css("color", "#8B8B8B");
    jQuery("h3.r a").css("color", "#8C8C8C");
    jQuery("#res a").css("background-color", "rgba(0, 0, 0, 0)");
    jQuery("#nav").css("opacity", "0.8");
    jQuery("#hplogo").css("opacity", "0.8");
    jQuery("#hdtbSum").css("background-color", "#2C2C2C");
    jQuery(".gb_Sb").css("background-color", "#3D3D3D");
    jQuery(".sect").css("color", "#666");
    jQuery(".sect").css("border-bottom", "1px solid #494949");
    jQuery(".mitem").css("background-color", "#424242");
    jQuery(".mitem:unhover").css("background-color", "#424242");
    jQuery(".appbar").css("border-bottom", "1px solid #494949");
    jQuery(".ab_button").css("background-image", "-webkit-linear-gradient(top,#515151,#474747)");
    jQuery(".ab_button").css("background-image", "linear-gradient(top,#515151,#474747)");
    jQuery(".ab_button").css("background-color", "#515151");
    jQuery(".ab_button.selected").css("border", "1px solid #494949");
    jQuery("#hdtb_tls:hover").css("background-image", "-webkit-linear-gradient(top,#515151,#474747)");
    jQuery("#hdtb_tls:hover").css("background-image", "linear-gradient(top,#515151,#474747)");
    jQuery("#hdtb_tls:hover").css("background-color", "#515151");
    jQuery("#hdtbMenus").css("background-color", "#424242");
    jQuery(".gb_na .gb_V").css("background-color", "#454545");
    jQuery(".gb_na .gb_V").css("border-color", "#545454;");
    jQuery(".flyr-o").css("opacity", "0.1");
}

initStyle();

setInterval(function() {
    initStyle();
}, 250);
"""


# -------------------- Utility Functions --------------------
def load_settings():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Определяем текущую папку
    homepage_path = os.path.join(base_dir, "site", "global", "index.html")  # Путь к index.html
    homepage_url = f"file:///{homepage_path.replace(os.sep, '/')}"  # Преобразуем в URL

    default_settings = {
        "is_private": False,
        "search_engine": "google",
        "language": "ru",
        "font_family": "Poppins",
        "font_size": 10,
        "homepage": homepage_url,  # Принудительно заменяем homepage
        "download_mode": "ask",
        "download_path": "",
        "delete_on_close": False,
        "smooth_animations": True,
        "ui_theme": "Default",
        "first_launch": True
    }

    # Загружаем сохранённые настройки, если файл существует
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                user_settings = json.load(f)
                default_settings.update(user_settings)  # Обновляем значениями пользователя
        except (json.JSONDecodeError, OSError):
            print("Ошибка при загрузке настроек, используются значения по умолчанию.")

    # Принудительно устанавливаем homepage, даже если в json сохранено другое значение
    default_settings["homepage"] = homepage_url

    return default_settings


def save_settings(settings: dict):
    """Сохраняет настройки сразу в два файла."""
    # Сохранение в основной файл
    os.makedirs(CONFIGS_DIR, exist_ok=True)  # Создаёт папку, если её нет
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

    # Сохранение в альтернативное местоположение
    os.makedirs(ALT_CONFIG_DIR, exist_ok=True)  # Создаёт папку, если её нет
    with open(ALT_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

    print(f"Настройки сохранены в:\n 1) {SETTINGS_FILE}\n 2) {ALT_SETTINGS_FILE}")

def load_history_from_file():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except:
            pass
    return []

def save_history_to_file(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_downloads_from_file():
    if os.path.exists(DOWNLOADS_FILE):
        try:
            with open(DOWNLOADS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except:
            pass
    return []

def load_downloads_from_file():
    if os.path.exists(DOWNLOADS_FILE):
        try:
            with open(DOWNLOADS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except:
            pass
    return []

def save_downloads_to_file(downloads):
    with open(DOWNLOADS_FILE, "w", encoding="utf-8") as f:
        json.dump(downloads, f, ensure_ascii=False, indent=2)

def load_extensions_from_file():
    if os.path.exists(EXTENSIONS_FILE):
        try:
            with open(EXTENSIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except:
            pass
    return []

    def load_finished(self):
        self.progress.hide()
        webview = self.current_webview()
        if webview:
            url = webview.url().toString()
            title = webview.page().title()
            if not self.is_private:
                history = load_history_from_file()
                history.append({
                    "url": url,
                    "title": title,
                    "timestamp": datetime.datetime.now().isoformat()
                })
                save_history_to_file(history)


def save_extensions_to_file(ext_list):
    with open(EXTENSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(ext_list, f, ensure_ascii=False, indent=2)

def load_bookmarks():
    if os.path.exists(BOOKMARKS_FILE):
        try:
            with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except:
            pass
    return []

def save_bookmarks(bookmarks):
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)

def get_cache_size() -> int:
    total_bytes = 0
    for folder in ["cache", "storage"]:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file_ in files:
                    fp = os.path.join(root, file_)
                    try:
                        total_bytes += os.path.getsize(fp)
                    except:
                        pass
    return total_bytes // (1024 * 1024)

def clear_browser_data(profile, cache_path: str, storage_path: str):
    cookie_store = profile.cookieStore()
    cookie_store.deleteAllCookies()
    shutil.rmtree(cache_path, ignore_errors=True)
    shutil.rmtree(storage_path, ignore_errors=True)
    os.makedirs(cache_path, exist_ok=True)
    os.makedirs(storage_path, exist_ok=True)

# -------------------- AdBlock Interceptor --------------------
class AdBlockInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ad_hosts = [
            "doubleclick.net", "googlesyndication.com", "adservice.google.com",
            "ads.youtube.com", "amazon-adsystem.com", "ads.exoclick.com",
            "adnxs.com", "ads.yahoo.com", "adtech.de", "adbrite.com",
            "scorecardresearch.com", "adserver.", "youtube.com/pagead",
            "youtube.com/get_video_info?adformat=", "youtube.com/api/stats/ads",
            "youtube.com/ptracking", "youtube.com/ads", "youtube.com/ad"
        ]
        self.big_filters = []
        self.load_big_filters()

    def load_big_filters(self):
        BIGFILTERS_FILE = os.path.join(BASE_DIR, "bigfilters.txt")
        if os.path.exists(BIGFILTERS_FILE):
            with open(BIGFILTERS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip().lower()
                    if word and not word.startswith("#"):
                        self.big_filters.append(word)

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        url = info.requestUrl()
        full_url = url.toString().lower()
        if "maps.google.com" in full_url or "googleapis.com/maps" in full_url:
            return
        for pattern in self.ad_hosts:
            if pattern in full_url:
                info.block(True)
                return
        for w in self.big_filters:
            if w in full_url:
                info.block(True)
                return

# -------------------- Custom WebEnginePage --------------------
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent, main_window):
        super().__init__(profile, parent)
        self.main_window = main_window

    def createWindow(self, _type):
        new_view = self.main_window.add_new_tab()
        return new_view.page()

    def consoleMessage(self, level, message, line, sourceID):
        if "Dev Tools is now avalible in russian" in message:
            return
        super().consoleMessage(level, message, line, sourceID)

# -------------------- Dialogs --------------------
class ManageDataDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Управление данными")
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(x1:0, y:0, x2:1, y:1,
                    stop:0 #2c2c2c, stop:1 #2f2f2f);
                color: #e0e0e0;
                border-radius: 10px;
            }
            QLabel { font-size: 14px; }
            QPushButton {
                background-color: #3b3b3b;
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #505050; }
        """)
        self.resize(400, 200)
        layout = QVBoxLayout(self)
        self.lbl_cache = QLabel("")
        layout.addWidget(self.lbl_cache)
        btn_clear = QPushButton("Очистить данные")
        btn_clear.clicked.connect(self.clear_data)
        layout.addWidget(btn_clear)
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)
        self.update_info()

    def update_info(self):
        size = get_cache_size()
        self.lbl_cache.setText(f"Ваши куки, данные сайтов и кэш занимают ~{size} MB.")

    def clear_data(self):
        self.parent().clear_browser_data_manually()
        self.update_info()
        QMessageBox.information(self, "Очистка", "Данные успешно удалены!")

class ManageExceptionsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Управление исключениями")
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(x1:0, y:0, x2:1, y:1,
                    stop:0 #2c2c2c, stop:1 #2f2f2f);
                color: #e0e0e0;
                border-radius: 10px;
            }
            QTreeWidget {
                background-color: #1e1e1e;
                border: 1px solid #555;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #3b3b3b;
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #505050; }
        """)
        self.resize(400, 300)
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Домен"])
        layout.addWidget(self.tree)
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Добавить")
        btn_remove = QPushButton("Удалить")
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_remove)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        btn_add.clicked.connect(self.add_exception)
        btn_remove.clicked.connect(self.remove_exception)
        self.exceptions = self.load_exceptions()
        self.refresh_tree()
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

    def load_exceptions(self):
        if os.path.exists(EXCEPTIONS_FILE):
            try:
                with open(EXCEPTIONS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except:
                return []
        return []

    def save_exceptions(self):
        with open(EXCEPTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.exceptions, f, ensure_ascii=False, indent=2)

    def refresh_tree(self):
        self.tree.clear()
        for domain in self.exceptions:
            item = QTreeWidgetItem([domain])
            self.tree.addTopLevelItem(item)


    def home(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        homepage_path = os.path.join(base_dir, "site", "global", "index.html")
        homepage_url = f"file:///{homepage_path.replace(os.sep, '/')}"


    def add_exception(self):
        domain, ok = QInputDialog.getText(self, "Добавить исключение", "Введите домен:")
        if ok and domain.strip():
            self.exceptions.append(domain.strip())
            self.save_exceptions()
            self.refresh_tree()

    def remove_exception(self):
        item = self.tree.currentItem()
        if item:
            domain = item.text(0)
            if domain in self.exceptions:
                self.exceptions.remove(domain)
                self.save_exceptions()
                self.refresh_tree()

class DownloadManagerWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Загрузки")
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "download.png")))
        self.resize(700, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(x1:0, y:0, x2:1, y:1,
                    stop:0 #2b2b2b, stop:1 #2f2f2f);
                border: none;
                border-radius: 10px;
            }
            QTreeWidget {
                background-color: rgba(30,30,30,0.95);
                color: #e0e0e0;
                border: none;
                border-radius: 5px;
            }
            QTreeWidget::item { padding: 6px; }
            QTreeWidget::item:hover { background-color: rgba(80,80,80,0.95); }
            QTreeWidget::item:selected { background-color: rgba(50,50,50,0.95); }
            QPushButton {
                background-color: #808080;
                border: none;
                border-radius: 5px;
                padding: 6px 12px;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #707070; }
        """)
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(["Файл", "Прогресс", "Скорость", "Статус", "Управление"])
        layout.addWidget(self.tree)
        self.tree.itemDoubleClicked.connect(self.open_downloaded_file)
        self.downloads = {}
        self.speed_info = {}
        self.finished_downloads = set()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all_downloads)
        self.timer.start(1000)
        self.speed_smoothing = 0.1
        if self.parent() and not self.parent().is_private:
            self.load_persistent_downloads()
        self.setLayout(layout)

    def load_persistent_downloads(self):
        persistent_downloads = load_downloads_from_file()
        for d in persistent_downloads:
            file_path = d.get("file_path", "")
            if os.path.exists(file_path):
                tree_item = QTreeWidgetItem([
                    d.get("file_name", ""), "100%", "0 B/s", d.get("status", "Завершено"), ""
                ])
                tree_item.setData(0, Qt.ItemDataRole.UserRole, file_path)
                self.tree.addTopLevelItem(tree_item)

    def update_persistent_downloads(self):
        if self.parent() and self.parent().is_private:
            return
        downloads_list = []
        items_to_check = [self.tree.topLevelItem(i) for i in range(self.tree.topLevelItemCount())]
        for item in items_to_check:
            file_path = item.data(0, Qt.ItemDataRole.UserRole)
            if os.path.exists(file_path):
                downloads_list.append({
                    "file_name": item.text(0),
                    "file_path": file_path,
                    "status": item.text(3)
                })
            else:
                self.remove_download_item(item)
        save_downloads_to_file(downloads_list)

    def format_speed(self, speed):
        if speed < 1024:
            return f"{speed:.0f} B/s"
        elif speed < 1024 * 1024:
            return f"{speed / 1024:.1f} KB/s"
        else:
            return f"{speed / (1024 * 1024):.1f} MB/s"

    def add_download(self, download_item: QWebEngineDownloadRequest):
        tree_item = QTreeWidgetItem([
            download_item.downloadFileName(), "0%", "0 B/s", "Загрузка", ""
        ])
        full_path = os.path.join(download_item.downloadDirectory(), download_item.downloadFileName())
        tree_item.setData(0, Qt.ItemDataRole.UserRole, full_path)
        self.tree.addTopLevelItem(tree_item)
        self.downloads[id(download_item)] = (download_item, tree_item)
        self.speed_info[id(download_item)] = (download_item.receivedBytes(), time.time(), 0.0)
        # Создаем кастомный виджет для пункта меню загрузок
        widget = QWidget()
        hlayout = QHBoxLayout(widget)
        hlayout.setContentsMargins(2, 2, 2, 2)
        hlayout.setSpacing(5)
        label = QLabel(download_item.downloadFileName())
        label.setStyleSheet("color: #e0e0e0;")
        def label_mouse_press(event):
            self.download_manager.open_downloaded_file(tree_item, 0)
        label.mousePressEvent = label_mouse_press
        hlayout.addWidget(label)
        btn_explorer = QPushButton()
        btn_explorer.setIcon(QIcon(os.path.join(ICONS_DIR, "explorer.png")))
        btn_explorer.setFixedSize(24, 24)
        btn_explorer.setStyleSheet("border: none;")
        def on_explorer_clicked():
            file_path = tree_item.data(0, Qt.ItemDataRole.UserRole)
            if file_path and os.path.exists(file_path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(file_path)))
        btn_explorer.clicked.connect(on_explorer_clicked)
        hlayout.addWidget(btn_explorer)
        hlayout.addStretch()
        self.tree.setItemWidget(tree_item, 4, widget)

    def toggle_pause(self, download_item, tree_item, control_button):
        if download_item.isPaused():
            download_item.resume()
            tree_item.setText(3, "Загрузка")
            control_button.setText("Пауза")
        else:
            download_item.pause()
            tree_item.setText(3, "Пауза")
            control_button.setText("Возобновить")

    def cancel_download(self, download_item, tree_item):
        download_item.cancel()
        tree_item.setText(3, "Отменено")
        self.tree.setItemWidget(tree_item, 4, None)
        self.update_persistent_downloads()
        if id(download_item) in self.downloads:
            del self.downloads[id(download_item)]

    def update_all_downloads(self):
        current_time = time.time()
        for key in list(self.downloads.keys()):
            download_item, tree_item = self.downloads[key]
            try:
                total = download_item.totalBytes()
            except RuntimeError:
                self.remove_download_item(tree_item)
                del self.downloads[key]
                continue
            if total > 0:
                received = download_item.receivedBytes()
                tree_item.setText(1, f"{int(received / total * 100)}%")
            else:
                tree_item.setText(1, "0%")
            if download_item.isPaused():
                tree_item.setText(2, "0 B/s")
                smoothed_speed = 0.0
            else:
                prev_received, prev_time, prev_smoothed_speed = self.speed_info.get(key, (0, current_time, 0.0))
                delta_time = current_time - prev_time
                received = download_item.receivedBytes()
                if delta_time > 0:
                    instantaneous_speed = (received - prev_received) / delta_time
                    smoothed_speed = (0.1 * instantaneous_speed + 0.9 * prev_smoothed_speed)
                    tree_item.setText(2, self.format_speed(smoothed_speed))
                else:
                    smoothed_speed = prev_smoothed_speed
                    tree_item.setText(2, "0 B/s")
                self.speed_info[key] = (received, current_time, smoothed_speed)
            if download_item.isFinished():
                tree_item.setText(1, "100%")
                tree_item.setText(3, "Завершено")
                self.tree.setItemWidget(tree_item, 4, None)
                if key not in self.finished_downloads:
                    finished_info = {
                        "file_name": download_item.downloadFileName(),
                        "file_path": os.path.join(download_item.downloadDirectory(), download_item.downloadFileName()),
                        "timestamp": datetime.datetime.now().isoformat(),
                        "status": "Завершено"
                    }
                    if self.parent() and not self.parent().is_private:
                        downloads_list = load_downloads_from_file()
                        downloads_list.append(finished_info)
                        save_downloads_to_file(downloads_list)
                    self.finished_downloads.add(key)

    def open_downloaded_file(self, item, column):
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and os.path.exists(file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        else:
            self.remove_download_item(item)

    def remove_download_item(self, item):
        idx = self.tree.indexOfTopLevelItem(item)
        if idx != -1:
            self.tree.takeTopLevelItem(idx)
            self.update_persistent_downloads()

class HistoryWindow(QDialog):
    def __init__(self, history_items, load_callback, parent=None):
        super().__init__(parent)
        self.setWindowTitle("История")
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "history.png")))
        self.load_callback = load_callback
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(x1:0, y:0, x2:1, y:1,
                    stop:0 #2c2c2c, stop:1 #2f2f2f);
                border: none;
                border-radius: 10px;
            }
            QTreeWidget {
                background-color: rgba(30,30,30,0.95);
                color: #e0e0e0;
                border: none;
                border-radius: 5px;
            }
            QTreeWidget::item { padding: 5px; }
            QTreeWidget::item:hover { background-color: rgba(80,80,80,0.95); }
            QTreeWidget::item:selected { background-color: rgba(50,50,50,0.95); }
            QPushButton {
                background-color: #808080;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                color: #FFFFFF;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #707070; }
        """)
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderHidden(True)
        layout.addWidget(self.tree)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        clear_btn = QPushButton("Очистить историю")
        clear_btn.clicked.connect(self.clear_history)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)
        groups = {}
        for item in history_items:
            try:
                ts = datetime.datetime.fromisoformat(item["timestamp"])
                date_str = ts.strftime("%d.%m.%Y")
            except:
                date_str = "Неизвестно"
            groups.setdefault(date_str, []).append((ts, item))
        for date in sorted(groups.keys(), key=lambda d: datetime.datetime.strptime(d, "%d.%m.%Y"), reverse=True):
            date_item = QTreeWidgetItem([date])
            self.tree.addTopLevelItem(date_item)
            for ts, it in sorted(groups[date], key=lambda x: x[0], reverse=True):
                time_str = ts.strftime("%H:%M:%S")
                child = QTreeWidgetItem([f"{time_str} - {it['title']}"])
                child.setData(0, Qt.ItemDataRole.UserRole, it["url"])
                date_item.addChild(child)
            date_item.setExpanded(True)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.resize(300, 600)

    def on_item_double_clicked(self, item, column):
        url = item.data(0, Qt.ItemDataRole.UserRole)
        if url:
            self.load_callback(QUrl(url))
            self.close()

    def clear_history(self):
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы действительно хотите очистить историю?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            save_history_to_file([])
            self.tree.clear()
            QMessageBox.information(self, "История", "История успешно очищена.")

class BookmarksWindow(QDialog):
    def __init__(self, bookmarks, load_callback, parent=None):
        super().__init__(parent)
        self.parent_win = parent
        self.load_callback = load_callback
        self.bookmarks = bookmarks[:]
        self.setWindowTitle(self.parent_win.tr_str("bookmarks_title"))
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "star.png")))
        self.resize(400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(x1:0, y:0, x2:1, y:1,
                    stop:0 #2c2c2c, stop:1 #2f2f2f);
                border: none;
                border-radius: 10px;
            }
            QTreeWidget {
                background-color: rgba(30,30,30,0.95);
                color: #e0e0e0;
                border: none;
                border-radius: 5px;
            }
            QTreeWidget::item { padding: 5px; }
            QTreeWidget::item:hover { background-color: rgba(80,80,80,0.95); }
            QTreeWidget::item:selected { background-color: rgba(50,50,50,0.95); }
            QPushButton {
                background-color: #808080;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                color: #FFFFFF;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #707070; }
        """)
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Название", "URL"])
        layout.addWidget(self.tree)
        btn_layout = QHBoxLayout()
        btn_add = QPushButton(self.parent_win.tr_str("add_bookmark"))
        btn_remove = QPushButton("Удалить")
        btn_rename = QPushButton("Переименовать")
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_rename)
        btn_layout.addWidget(btn_remove)
        layout.addLayout(btn_layout)
        btn_close = QPushButton("Закрыть")
        layout.addWidget(btn_close)
        btn_add.clicked.connect(self.add_bookmark_manually)
        btn_remove.clicked.connect(self.remove_bookmark)
        btn_rename.clicked.connect(self.rename_bookmark)
        btn_close.clicked.connect(self.close)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.refresh_tree()
        self.setLayout(layout)

    def refresh_tree(self):
        self.tree.clear()
        for bm in self.bookmarks:
            title = bm.get("title", "")
            url = bm.get("url", "")
            item = QTreeWidgetItem([title, url])
            self.tree.addTopLevelItem(item)

    def on_item_double_clicked(self, item, column):
        url = item.text(1)
        if url:
            self.load_callback(QUrl(url))
            self.close()

    def add_bookmark_manually(self):
        title, ok = QInputDialog.getText(self, "Добавить закладку", "Введите название:")
        if not ok or not title.strip():
            return
        url, ok2 = QInputDialog.getText(self, "Добавить закладку", "Введите URL:")
        if not ok2 or not url.strip():
            return
        bm = {"title": title.strip(), "url": url.strip()}
        self.bookmarks.append(bm)
        self.refresh_tree()

    def remove_bookmark(self):
        item = self.tree.currentItem()
        if not item:
            return
        title = item.text(0)
        url = item.text(1)
        for bm in self.bookmarks:
            if bm.get("title") == title and bm.get("url") == url:
                self.bookmarks.remove(bm)
                break
        self.refresh_tree()

    def rename_bookmark(self):
        item = self.tree.currentItem()
        if not item:
            return
        old_title = item.text(0)
        old_url = item.text(1)
        new_title, ok = QInputDialog.getText(self, "Переименовать закладку", "Новое название:", text=old_title)
        if ok and new_title.strip():
            for bm in self.bookmarks:
                if bm.get("title") == old_title and bm.get("url") == old_url:
                    bm["title"] = new_title.strip()
                    break
            self.refresh_tree()

    def closeEvent(self, event):
        save_bookmarks(self.bookmarks)
        event.accept()

class ExtensionsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_win = parent
        self.setModal(True)
        self.setWindowTitle(self.tr_str("extensions_title"))
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(x1:0, y:0, x2:1, y:1,
                    stop:0 #2e2e2e, stop:1 #3b3b3b);
                border: none;
                border-radius: 10px;
            }
            QTreeWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #555;
                border-radius: 5px;
            }
            QTreeWidget::item { padding: 5px; }
            QTreeWidget::item:hover { background-color: #505050; }
            QPushButton {
                background-color: #3b3b3b;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                color: #fff;
            }
            QPushButton:hover { background-color: #707070; }
        """)
        self.resize(650, 450)
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Название", "Описание", "Состояние"])
        layout.addWidget(self.tree)
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton(self.tr_str("extensions_add"))
        self.btn_remove = QPushButton(self.tr_str("extensions_remove"))
        self.btn_toggle = QPushButton(self.tr_str("extensions_toggle"))
        self.btn_edit = QPushButton("Редактировать описание")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        btn_layout.addWidget(self.btn_toggle)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        self.btn_add.clicked.connect(self.add_extension)
        self.btn_remove.clicked.connect(self.remove_extension)
        self.btn_toggle.clicked.connect(self.toggle_selected_extension)
        self.btn_edit.clicked.connect(self.edit_extension_description)
        self.extensions = load_extensions_from_file()
        if not any(ext.get("name", "").lower() == "miblock" for ext in self.extensions):
            if os.path.exists(USER_SCRIPT_FILE):
                with open(USER_SCRIPT_FILE, "r", encoding="utf-8") as f:
                    code = f.read()
            else:
                code = "console.log('MiBlock is running!');"
            self.extensions.append({
                "name": "miblock",
                "code": code,
                "enabled": True,
                "description": self.tr_str("default_extension_description")
            })
            save_extensions_to_file(self.extensions)
        if not any(ext.get("name", "").lower() == "darkmode" for ext in self.extensions):
            if os.path.exists(DARKREADER_FILE):
                with open(DARKREADER_FILE, "r", encoding="utf-8") as f:
                    code = f.read()
            else:
                code = "console.log('Dark Mode is running!');"
            darkmode_desc = "Dark Mode расширение, которое меняет цветовую схему сайтов на тёмную, разработано MiHaTsKiYi специально для MiHa Browser"
            self.extensions.append({
                "name": "darkmode",
                "code": code,
                "enabled": True,
                "description": darkmode_desc
            })
            save_extensions_to_file(self.extensions)
        self.refresh_tree()
        self.setLayout(layout)

    def tr_str(self, key: str) -> str:
        lang = self.parent_win.settings["language"]
        return TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, key)

    def edit_extension_description(self):
        item = self.tree.currentItem()
        if not item:
            return
        idx = self.tree.indexOfTopLevelItem(item)
        if idx < 0:
            return
        ext = self.extensions[idx]
        if ext.get("name", "").lower() == "miblock":
            QMessageBox.information(self, "Info", "Нельзя редактировать описание стандартного расширения.")
            return
        new_desc, ok = QInputDialog.getText(self, "Редактировать описание", "Введите новое описание:", text=ext.get("description", ""))
        if ok:
            ext["description"] = new_desc.strip()
            save_extensions_to_file(self.extensions)
            self.refresh_tree()
            QMessageBox.information(self, "Info", "Описание обновлено.")

    def refresh_tree(self):
        self.tree.clear()
        for ext in self.extensions:
            name = ext.get("name", "Unnamed")
            description = ext.get("description", "")
            enabled = ext.get("enabled", True)
            state_text = "Включено" if enabled else "Отключено"
            if self.parent_win.settings["language"] == "en":
                state_text = "Enabled" if enabled else "Disabled"
            item = QTreeWidgetItem([name, description, state_text])
            self.tree.addTopLevelItem(item)

    def add_extension(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите JS файл", "", "JavaScript Files (*.js)")
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        base_name = os.path.splitext(os.path.basename(path))[0]
        name, ok = QInputDialog.getText(self, "Название скрипта", "Введите название скрипта:", text=base_name)
        if not ok or not name.strip():
            return
        new_ext = {
            "name": name.strip(),
            "code": code,
            "enabled": True,
            "description": ""
        }
        self.extensions.append(new_ext)
        save_extensions_to_file(self.extensions)
        self.refresh_tree()
        QMessageBox.information(self, "Info", self.tr_str("extensions_need_restart"))
        self.parent_win.update_extensions()

    def remove_extension(self):
        item = self.tree.currentItem()
        if not item:
            return
        idx = self.tree.indexOfTopLevelItem(item)
        if idx >= 0:
            ext = self.extensions[idx]
            if ext.get("name", "").lower() == "miblock":
                QMessageBox.warning(self, "Ошибка", "Нельзя удалить стандартное расширение miblock.")
                return
            if ext.get("name", "").lower() == "darkmode":
                QMessageBox.warning(self, "Ошибка", "Нельзя удалить стандартное расширение Dark Mode.")
                return
            reply = QMessageBox.question(
                self, "Удалить скрипт?",
                "Вы уверены, что хотите удалить выбранное расширение?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.extensions.pop(idx)
                save_extensions_to_file(self.extensions)
                self.refresh_tree()
                QMessageBox.information(self, "Info", self.tr_str("extensions_need_restart"))
                self.parent_win.update_extensions()

    def toggle_selected_extension(self):
        item = self.tree.currentItem()
        if not item:
            return
        idx = self.tree.indexOfTopLevelItem(item)
        if idx < 0:
            return
        ext = self.extensions[idx]
        current_state = ext.get("enabled", True)
        ext["enabled"] = not current_state
        save_extensions_to_file(self.extensions)
        self.refresh_tree()
        QMessageBox.information(self, "Info", self.tr_str("extensions_need_restart"))
        self.parent_win.update_extensions()

class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_win = parent
        self.setModal(True)
        self.setWindowTitle(self.tr_str("settings_title"))

        # Плавная анимация проявления
        self.setWindowOpacity(0.0)
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.fade_animation.start()

        # Общий стиль
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(x1:0, y:0, x2:1, y:1,
                    stop:0 #2c2c2b, stop:1 #2f2f2f);
                border: none;
                border-radius: 10px;
            }

            QLabel, QComboBox, QLineEdit, QPushButton, QCheckBox {
                font-size: 14px;
                color: #e0e0e0;
            }

            QComboBox, QLineEdit {
                background-color: #2e2e2e;
                border: 1px solid #555;
                padding: 4px;
                border-radius: 5px;
                padding-right: 30px; /* место под стрелку */
            }

            /* Область кнопки раскрытия */
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 28px;
                border-left: 1px solid #555;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                background-color: #3b3b3b;
            }

            /* Стрелка без круга вокруг */
            QComboBox::down-arrow {
                image: url("icons/down.png"); /* путь к файлу down.png */
                width: 16px;
                height: 16px;
                margin: 6px;       /* чтобы иконка оказалась по центру */
                background: none;  /* убираем заливку */
                border-radius: 0;  /* убираем скругление */
            }

            /* Список */
            QComboBox QAbstractItemView {
                background-color: #3b3b3b;
                border: 1px solid #555;
                selection-background-color: #505050;
                selection-color: #ffffff;
            }

            QPushButton {
                background-color: #3b3b3b;
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #505050;
            }
        """)

        self.resize(480, 420)
        self.init_ui()

    def tr_str(self, key: str) -> str:
        lang = self.parent_win.settings["language"]
        return TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, key)

    def init_ui(self):
        layout = QVBoxLayout(self)

        # ----- Поисковый движок -----
        hl_engine = QHBoxLayout()
        lbl_engine = QLabel(self.tr_str("search_engine") + ":")
        self.cmb_engine = QComboBox()
        if self.parent_win.is_private:
            self.cmb_engine.addItems(["duckduckgo"])
        else:
            self.cmb_engine.addItems(["google", "yandex", "bing", "duckduckgo"])
        self.cmb_engine.setCurrentText(self.parent_win.settings["search_engine"])
        if self.parent_win.is_private:
            self.cmb_engine.setEnabled(False)
        hl_engine.addWidget(lbl_engine)
        hl_engine.addWidget(self.cmb_engine)
        layout.addLayout(hl_engine)

        # ----- Домашняя страница -----
        hl_home = QHBoxLayout()
        lbl_home = QLabel(self.tr_str("homepage") + ":")
        self.le_home = QLineEdit()
        self.le_home.setText(self.parent_win.settings["homepage"])
        if self.parent_win.is_private:
            self.le_home.setEnabled(False)
        hl_home.addWidget(lbl_home)
        hl_home.addWidget(self.le_home)
        layout.addLayout(hl_home)

        # ----- Режим загрузки -----
        hl_dl = QHBoxLayout()
        lbl_dl = QLabel(self.tr_str("download_mode") + ":")
        self.cmb_dl = QComboBox()
        self.cmb_dl.addItems([
            self.tr_str("ask"),
            self.tr_str("default"),
            self.tr_str("custom")
        ])
        current_dl_mode = self.parent_win.settings.get("download_mode", "ask")
        self.cmb_dl.setCurrentIndex({
            "ask": 0, "default": 1, "custom": 2
        }.get(current_dl_mode, 0))
        hl_dl.addWidget(lbl_dl)
        hl_dl.addWidget(self.cmb_dl)
        layout.addLayout(hl_dl)

        # ----- Путь загрузки -----
        hl_path = QHBoxLayout()
        lbl_path = QLabel(self.tr_str("custom_download_path") + ":")
        self.le_path = QLineEdit()
        self.le_path.setText(self.parent_win.settings.get("download_path", ""))
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.choose_download_path)
        hl_path.addWidget(lbl_path)
        hl_path.addWidget(self.le_path)
        hl_path.addWidget(self.btn_browse)
        layout.addLayout(hl_path)

        self.cmb_dl.currentIndexChanged.connect(self.update_dl_mode)
        self.update_dl_mode(self.cmb_dl.currentIndex())

        # ----- Язык -----
        hl_lang = QHBoxLayout()
        lbl_lang = QLabel(self.tr_str("language") + ":")
        self.cmb_lang = QComboBox()
        self.cmb_lang.addItems(LANGS)
        self.cmb_lang.setCurrentText(self.parent_win.settings["language"])
        hl_lang.addWidget(lbl_lang)
        hl_lang.addWidget(self.cmb_lang)
        layout.addLayout(hl_lang)

        # ----- Шрифт -----
        hl_font = QHBoxLayout()
        lbl_font = QLabel(self.tr_str("font") + ":")
        self.btn_font = QPushButton(self.parent_win.settings["font_family"])
        self.btn_font.clicked.connect(self.choose_font)
        hl_font.addWidget(lbl_font)
        hl_font.addWidget(self.btn_font)
        layout.addLayout(hl_font)

        # ----- Данные и куки -----
        lbl_cookies = QLabel(f"<b>{self.tr_str('cookies_data')}</b>")
        layout.addWidget(lbl_cookies)
        usage_mb = get_cache_size()
        lbl_usage = QLabel(self.tr_str("cookies_data_info").format(usage_mb))
        lbl_usage.setStyleSheet("color: #cccccc; font-size: 13px;")
        layout.addWidget(lbl_usage)

        cookies_btn_layout = QHBoxLayout()
        btn_delete = QPushButton(self.tr_str("delete_data"))
        btn_manage = QPushButton(self.tr_str("manage_data"))
        btn_exceptions = QPushButton(self.tr_str("manage_exceptions"))
        btn_delete.clicked.connect(self.on_delete_data)
        btn_manage.clicked.connect(lambda: ManageDataDialog(self.parent_win).exec())
        btn_exceptions.clicked.connect(lambda: ManageExceptionsDialog(self.parent_win).exec())
        cookies_btn_layout.addWidget(btn_delete)
        cookies_btn_layout.addWidget(btn_manage)
        cookies_btn_layout.addWidget(btn_exceptions)
        layout.addLayout(cookies_btn_layout)

        self.chk_delete_on_close = QCheckBox(self.tr_str("delete_on_close"))
        self.chk_delete_on_close.setChecked(self.parent_win.settings.get("delete_on_close", False))
        layout.addWidget(self.chk_delete_on_close)

        lbl_info = QLabel(self.tr_str("restart_info"))
        lbl_info.setStyleSheet("color: #999999; font-size: 12px;")
        layout.addWidget(lbl_info)

        bottom_layout = QHBoxLayout()

        # Лейбл с текстом лицензии
        self.license_label = QLabel("Made with Python")
        self.license_label.setStyleSheet("font-size: 10px; color: #aaaaaa;")

        class ClickableLabel(QLabel):
            def __init__(self, parent_win, url, tab_title):
                # Передаём родительское окно, чтобы потом использовать его метод add_new_tab
                super().__init__(parent_win)
                self.parent_win = parent_win
                self.url = url
                self.tab_title = tab_title
                # Меняем курсор на указатель (руку) при наведении
                self.setCursor(Qt.CursorShape.PointingHandCursor)

            def mousePressEvent(self, event):
                # Открываем новую вкладку внутри нашего браузера, вызывая метод главного окна
                self.parent_win.add_new_tab(QUrl(self.url), self.tab_title)
                super().mousePressEvent(event)

        # Пример использования в вашем коде:
        self.gif_label = ClickableLabel(self.parent_win,
                                        "https://github.com/MiHaTsKiYi13/MiHa-Browser",
                                        "GitHub Repo")
        pixmap = QPixmap("icons/python.png")
        self.gif_label.setPixmap(pixmap)
        self.gif_label.setScaledContents(True)
        self.gif_label.setFixedSize(16, 16)

        # Контейнер для лицензии и гифки
        license_layout = QHBoxLayout()
        license_layout.addWidget(self.gif_label)
        license_layout.addWidget(self.license_label)
        license_layout.addStretch()  # Отправляет всё влево

        # Добавляем в основной layout
        layout.addLayout(license_layout)

        # Кнопки: OK / Cancel / Exit
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancel")
        btn_exit = QPushButton(self.tr_str("exit"))

        btn_ok.clicked.connect(self.on_ok)
        btn_cancel.clicked.connect(self.on_cancel)
        btn_exit.clicked.connect(self.parent_win.close)

        bottom_layout.addWidget(btn_ok)
        bottom_layout.addWidget(btn_cancel)
        bottom_layout.addWidget(btn_exit)

        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def choose_download_path(self):
        path = QFileDialog.getExistingDirectory(self, "Choose download folder")
        if path:
            self.le_path.setText(path)

    def update_dl_mode(self, idx):
        # idx == 2 -> "custom"
        if idx == 2:
            self.le_path.setEnabled(True)
            self.btn_browse.setEnabled(True)
        else:
            self.le_path.setEnabled(False)
            self.btn_browse.setEnabled(False)

    def choose_font(self):
        current_family = self.parent_win.settings["font_family"]
        current_size = self.parent_win.settings["font_size"]
        initial_font = QFont(current_family, current_size)
        font, ok = QFontDialog.getFont(initial_font, self, "Choose font")
        if ok:
            self.btn_font.setText(font.family())

    def on_delete_data(self):
        reply = QMessageBox.question(
            self,
            "Clear Data",
            "Do you really want to delete all cookies and site data?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.parent_win.clear_browser_data_manually()
            QMessageBox.information(self, "Clear", "Data successfully cleared!")

    def on_ok(self):
        new_engine = self.cmb_engine.currentText()
        new_home = self.le_home.text()
        new_lang = self.cmb_lang.currentText()
        new_font_family = self.btn_font.text()
        idx_dl = self.cmb_dl.currentIndex()
        dl_map = {0: "ask", 1: "default", 2: "custom"}
        new_dl_mode = dl_map.get(idx_dl, "ask")
        new_dl_path = self.le_path.text()

        # Принудительно устанавливаем путь к index.html, даже если пользователь менял вручную
        base_dir = os.path.dirname(os.path.abspath(__file__))
        homepage_path = os.path.join(base_dir, "site", "global", "index.html")
        homepage_url = f"file:///{homepage_path.replace(os.sep, '/')}"

        self.parent_win.settings["search_engine"] = new_engine
        self.parent_win.settings["homepage"] = homepage_url  # Принудительно заменяем
        self.parent_win.settings["language"] = new_lang
        self.parent_win.settings["font_family"] = new_font_family
        self.parent_win.settings["download_mode"] = new_dl_mode
        self.parent_win.settings["download_path"] = new_dl_path
        self.parent_win.settings["delete_on_close"] = self.chk_delete_on_close.isChecked()

        self.parent_win.apply_settings()
        save_settings(self.parent_win.settings)
        self.close()

    def on_cancel(self):
        self.close()

class FirstLaunchDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_win = parent
        # Если язык не задан, устанавливаем дефолтный английский
        if "language" not in self.parent_win.settings:
            self.parent_win.settings["language"] = "en"

        # Окно без рамки для стильного оформления
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setStyleSheet("""
            QDialog {
                background-color: #2e2e2e;
                border: 2px solid #555;
                border-radius: 10px;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 18px;
                margin: 10px;
            }
            QPushButton {
                background-color: #5a5a5a;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                color: #ffffff;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #707070;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Make browser default?")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        btn_layout = QHBoxLayout()
        btn_yes = QPushButton("Yes")
        btn_skip = QPushButton("Skip")
        btn_layout.addWidget(btn_yes)
        btn_layout.addWidget(btn_skip)
        layout.addLayout(btn_layout)

        btn_yes.clicked.connect(self.set_default_browser)
        btn_skip.clicked.connect(self.open_language_dialog)
        self.setLayout(layout)

    def set_default_browser(self):
        # Открываем настройки стандартных приложений (только для Windows)
        try:
            os.startfile("ms-settings:defaultapps")
        except Exception as e:
            print("Failed to open default apps settings:", e)
        # Закрываем текущее окно и переходим к выбору языка
        self.close()
        lang_dialog = LanguageSelectionDialog(self.parent_win)
        lang_dialog.exec()

    def open_language_dialog(self):
        # Закрываем текущее окно и открываем диалог выбора языка
        self.close()
        lang_dialog = LanguageSelectionDialog(self.parent_win)
        lang_dialog.exec()

    def showEvent(self, event):
        dialog_width = 400
        dialog_height = 200
        # Если родительское окно видно, центрируем относительно него, иначе по экрану
        if self.parent_win and self.parent_win.isVisible():
            parent_geom = self.parent_win.geometry()
        else:
            parent_geom = QGuiApplication.primaryScreen().availableGeometry()
        x = parent_geom.x() + (parent_geom.width() - dialog_width) // 2
        y = parent_geom.y() + (parent_geom.height() - dialog_height) // 2
        self.setGeometry(x, y, dialog_width, dialog_height)
        # Плавное появление (fade‑in)
        self.setWindowOpacity(0)
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_animation.start()
        super().showEvent(event)


class LanguageSelectionDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_win = parent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setStyleSheet("""
            QDialog {
                background-color: #2e2e2e;
                border: 2px solid #555;
                border-radius: 10px;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 18px;
                margin: 10px;
            }
            QPushButton {
                background-color: #5a5a5a;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                color: #ffffff;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #707070;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Select Language")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        btn_layout = QHBoxLayout()
        btn_russian = QPushButton("Русский")
        btn_english = QPushButton("English")
        btn_layout.addWidget(btn_russian)
        btn_layout.addWidget(btn_english)
        layout.addLayout(btn_layout)

        btn_russian.clicked.connect(lambda: self.set_language("ru"))
        btn_english.clicked.connect(lambda: self.set_language("en"))
        self.setLayout(layout)

    def set_language(self, lang):
        # Обновляем настройки родительского окна
        self.parent_win.settings["language"] = lang
        if hasattr(self.parent_win, "update_language"):
            self.parent_win.update_language(lang)
        self.close()

    def showEvent(self, event):
        dialog_width = 400
        dialog_height = 200
        # Центрируем окно относительно родительского окна, либо экрана
        if self.parent_win and self.parent_win.isVisible():
            parent_geom = self.parent_win.geometry()
        else:
            parent_geom = QGuiApplication.primaryScreen().availableGeometry()
        x = parent_geom.x() + (parent_geom.width() - dialog_width) // 2
        y = parent_geom.y() + (parent_geom.height() - dialog_height) // 2
        self.setGeometry(x, y, dialog_width, dialog_height)
        # Плавное появление (fade‑in)
        self.setWindowOpacity(0)
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_animation.start()
        super().showEvent(event)



# -------------------- MainWindow --------------------
class MainWindow(QMainWindow):
    def __init__(self, settings=None):
        super().__init__()
        if settings is None:
            settings = load_settings()
        self.settings = settings
        self.is_private = self.settings["is_private"]
        self.dev_tools_window = None
        self.chatgpt_dock = None
        self.download_animations = []
        if self.is_private and os.path.exists(os.path.join(ICONS_DIR, "icoprivate.png")):
            self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "icoprivate.png")))
        else:
            self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "ico.png")))
        self.setWindowTitle(self.tr_str("browser_title"))
        self.setGeometry(100, 100, 1280, 720)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().hide()
        self.animations = []
        self.history_windows = []
        self.child_windows = []
        self.cache_path = os.path.abspath("cache")
        self.storage_path = os.path.abspath("storage")
        self.custom_extension_scripts = []
        self.apply_settings()
        self.initUI()
        profile = QWebEngineProfile.defaultProfile()
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.init_shortcuts()
        self.update_extensions()
        if self.settings.get("first_launch", True):
            self.show_first_launch_dialog()
            self.settings["first_launch"] = False
            save_settings(self.settings)


    def load_custom_extensions(self):
        ext_list = load_extensions()
        # Добавляем встроенное расширение Google Dark, если его ещё нет
        if not any(ext.get("name", "").lower() == "google dark" for ext in ext_list):
            ext_list.append({
                "name": "Google Dark",
                "code": GOOGLE_DARK_EXTENSION,
                "enabled": True,
                "description": "Google dark theme built-in extension."
            })
            save_extensions(ext_list)
        # Загружаем все включённые расширения как скрипты
        for ext in ext_list:
            if ext.get("enabled", True):
                script = QWebEngineScript()
                script.setName(ext.get("name", "UserExtension"))
                script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
                script.setRunsOnSubFrames(True)
                script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
                script.setSourceCode(ext.get("code", ""))
                self.profile.scripts().insert(script)
                self.custom_extension_scripts.append(script)
    
    def save_current_history(self):
        self.progress.hide()
        webview = self.current_webview()
        if webview:
            url = webview.url().toString()
            title = webview.page().title()
            if not self.is_private:
                history = load_history_from_file()
                history.append({
                    "url": url,
                    "title": title,
                    "timestamp": datetime.datetime.now().isoformat()
                })
                save_history_to_file(history)

    def load_custom_extensions(self):
        for script in self.custom_extension_scripts:
            self.profile.scripts().remove(script)
        self.custom_extension_scripts.clear()
        ext_list = load_extensions_from_file()
        if not any(ext.get("name", "").lower() == "miblock" for ext in ext_list):
            if os.path.exists(USER_SCRIPT_FILE):
                with open(USER_SCRIPT_FILE, "r", encoding="utf-8") as f:
                    code = f.read()
            else:
                code = "console.log('MiBlock is running!');"
            ext_list.append({
                "name": "miblock",
                "code": code,
                "enabled": True,
                "description": TRANSLATIONS[self.settings["language"]].get("default_extension_description", "")
            })
            save_extensions_to_file(ext_list)
        if not any(ext.get("name", "").lower() == "darkmode" for ext in ext_list):
            if os.path.exists(DARKREADER_FILE):
                with open(DARKREADER_FILE, "r", encoding="utf-8") as f:
                    code = f.read()
            else:
                code = "console.log('Dark Mode is running!');"
            darkmode_desc = "Dark Mode расширение, которое меняет цветовую схему сайтов на тёмную, разработано MiHaTsKiYi специально для MiHa Browser"
            ext_list.append({
                "name": "darkmode",
                "code": code,
                "enabled": True,
                "description": darkmode_desc
            })
            save_extensions_to_file(ext_list)
        for ext in ext_list:
            if ext.get("enabled", True):
                script = QWebEngineScript()
                script.setName(ext.get("name", "UserExtension"))
                script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
                script.setRunsOnSubFrames(True)
                script.setSourceCode(ext.get("code", ""))
                self.profile.scripts().insert(script)
                self.custom_extension_scripts.append(script)
        save_extensions_to_file(ext_list)

    def set_default_browser(self):
        QDesktopServices.openUrl(QUrl("ms-settings:defaultapps"))

    def tr_str(self, key: str) -> str:
        lang = self.settings["language"]
        return TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, key)

    def apply_settings(self):
        # Применяем настройки шрифта
        font_family = self.settings["font_family"]
        font_size = self.settings["font_size"]
        self.setFont(QFont(font_family, font_size))

        # Получаем базовую директорию (папка, где находится main.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Задаем путь домашней страницы в зависимости от режима
        if self.is_private:
            # Приватный режим – домашняя страница из папки site/private
            homepage_path = os.path.join(base_dir, "site", "private", "index.html")
        else:
            # Обычный режим – домашняя страница из папки site/global
            homepage_path = os.path.join(base_dir, "site", "global", "index.html")

        # Преобразуем путь в URL формата file:// и устанавливаем его
        self.homepage = QUrl.fromLocalFile(homepage_path).toString()
        print("Домашняя страница:", self.homepage)

    def initUI(self):
        os.makedirs(self.cache_path, exist_ok=True)
        os.makedirs(self.storage_path, exist_ok=True)
        if self.is_private:
            self.profile = QWebEngineProfile(self)
        else:
            self.profile = QWebEngineProfile("persistent_profile", self)
            self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
            self.profile.setCachePath(self.cache_path)
            self.profile.setPersistentStoragePath(self.storage_path)
        self.profile.downloadRequested.connect(self.handle_download)
        self.adblocker = AdBlockInterceptor(self)
        self.profile.setUrlRequestInterceptor(self.adblocker)
        if os.path.exists(USER_SCRIPT_FILE):
            with open(USER_SCRIPT_FILE, "r", encoding="utf-8") as f:
                code = f.read()
            script = QWebEngineScript()
            script.setName("LocalUserScript")
            script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
            script.setRunsOnSubFrames(True)
            script.setSourceCode(code)
            self.profile.scripts().insert(script)
        if os.path.exists(DARKREADER_FILE):
            with open(DARKREADER_FILE, "r", encoding="utf-8") as f:
                code = f.read()
            dark_script = QWebEngineScript()
            dark_script.setName("DarkReaderScript")
            dark_script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
            dark_script.setRunsOnSubFrames(True)
            dark_script.setSourceCode(code)
            self.profile.scripts().insert(dark_script)
        self.inject_allowfullscreen_script()



        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(18, 18))
        navtb.setStyleSheet("""
            QToolBar {
                background-color: #333333;
                border-bottom: 1px solid #444;
                spacing: 8px;
                padding: 6px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                color: #e0e0e0;
            }
            QToolButton:hover {
                background-color: #555555;
                border-radius: 4px;
            }
            QLineEdit {
                background-color: #2b2b2b;
                border: 1px solid #666;
                color: #e0e0e0;
                padding: 4px;
                border-radius: 4px;
            }
        """)
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join(ICONS_DIR, "leftico.png")), "Назад", self)
        back_btn.triggered.connect(self.navigate_back)
        navtb.addAction(back_btn)
        forward_btn = QAction(QIcon(os.path.join(ICONS_DIR, "rightico.png")), "Вперёд", self)
        forward_btn.triggered.connect(self.navigate_forward)
        navtb.addAction(forward_btn)
        reload_btn = QAction(QIcon(os.path.join(ICONS_DIR, "refresh.png")), "Обновить", self)
        reload_btn.triggered.connect(self.navigate_refresh)
        navtb.addAction(reload_btn)
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(5)
# Создание адресной строки с запретом на автоматический фокус
        self.urlbar = QLineEdit(self)
        self.urlbar.setFocusPolicy(Qt.FocusPolicy.NoFocus)  
        self.urlbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        search_layout.addWidget(self.urlbar)
        navtb.addWidget(search_widget)
        self.bookmark_button = QToolButton()
        self.bookmark_button.clicked.connect(self.toggle_bookmark)
        navtb.addWidget(self.bookmark_button)
        self.update_bookmark_icon()
        self.extensions_btn = QToolButton()
        self.extensions_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "extensions.png")))
        self.extensions_btn.clicked.connect(self.show_extensions_dialog)
        navtb.addWidget(self.extensions_btn)
        self.download_manager = DownloadManagerWindow(self)
        self.download_btn = QToolButton()
        self.download_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "download.png")))
        self.download_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.download_btn.setStyleSheet("""
            QToolButton::menu-indicator {
                image: none;
                width: 0;
            }
        """)
        self.download_btn.clicked.connect(self.show_downloads_menu)
        navtb.addWidget(self.download_btn)
        self.chatgpt_btn = QToolButton()
        self.chatgpt_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "chatgpt.png")))
        self.chatgpt_btn.setToolTip("Open ChatGPT Sidebar")
        self.chatgpt_btn.clicked.connect(self.open_chatgpt_sidebar)
        navtb.addWidget(self.chatgpt_btn)
        menu_button = QToolButton()
        menu_button.setIcon(QIcon(os.path.join(ICONS_DIR, "settings.png")))
        menu_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")
        main_menu = QMenu()
        main_menu.setStyleSheet("""
            QMenu {
                background-color: #2e2e2e;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #505050;
                border-radius: 4px;
            }
        """)
        new_tab_action = QAction(self.tr_str("new_tab"), self)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        main_menu.addAction(new_tab_action)
        new_window_action = QAction(self.tr_str("new_window"), self)
        new_window_action.setShortcut(QKeySequence("Ctrl+N"))
        new_window_action.triggered.connect(self.open_new_window)
        main_menu.addAction(new_window_action)
        self.toggle_private_action = QAction("", self)
        self.toggle_private_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        self.toggle_private_action.triggered.connect(self.toggle_mode)
        main_menu.addAction(self.toggle_private_action)
        if self.is_private:
            self.toggle_private_action.setText(self.tr_str("private_off"))
        else:
            self.toggle_private_action.setText(self.tr_str("private_on"))
        history_action = QAction(self.tr_str("history"), self)
        history_action.triggered.connect(self.show_history)
        main_menu.addAction(history_action)
        downloads_action = QAction(self.tr_str("downloads"), self)
        downloads_action.triggered.connect(self.show_download_manager)
        main_menu.addAction(downloads_action)
        bookmarks_action = QAction(self.tr_str("bookmarks"), self)
        bookmarks_action.triggered.connect(self.show_bookmarks_window)
        main_menu.addAction(bookmarks_action)
        main_menu.addSeparator()
        extensions_action = QAction(self.tr_str("extensions"), self)
        extensions_action.triggered.connect(self.show_extensions_dialog)
        main_menu.addAction(extensions_action)
        settings_action = QAction(self.tr_str("settings"), self)
        settings_action.triggered.connect(self.open_settings_dialog)
        main_menu.addAction(settings_action)
        exit_action = QAction(self.tr_str("exit"), self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        main_menu.addAction(exit_action)
        menu_button.setMenu(main_menu)
        menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        navtb.addWidget(menu_button)
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(120)
        self.progress.setTextVisible(False)
        self.progress.hide()
        navtb.addWidget(self.progress)
        self.download_manager.setParent(self)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                background: qlineargradient(x1:0, y:0, x2:1, y:1,
                    stop:0 rgba(30,30,30,0.7), stop:1 rgba(60,60,60,0.7));
                border: none;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: rgba(40,40,40,0.8);
                color: #e0e0e0;
                padding: 5px;
                border: none;
                border-radius: 6px;
                min-width: 100px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: rgba(50,50,50,0.8);
            }
        """)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_urlbar)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.setCentralWidget(self.tabs)
        addTabButton = QToolButton(self)
        addTabButton.setIcon(QIcon(os.path.join(ICONS_DIR, "add.png")))
        addTabButton.setAutoRaise(True)
        addTabButton.clicked.connect(lambda: self.add_new_tab())
        self.tabs.setCornerWidget(addTabButton, Qt.Corner.TopRightCorner)
        # Получаем базовую директорию, где находится main.py
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Определяем путь к домашней странице в зависимости от режима
        if self.is_private:
            homepage_path = os.path.join(base_dir, "site", "private", "index.html")
        else:
            homepage_path = os.path.join(base_dir, "site", "global", "index.html")

        # Преобразуем путь в URL формата file://
        homepage_url = QUrl.fromLocalFile(homepage_path)

        # Открываем новую вкладку с домашней страницей
        self.add_new_tab(homepage_url, "Homepage")


    def consoleMessage(self, level, message, line, sourceID):
        if "Dev Tools is now avalible in russian" in message:
            return
        super().consoleMessage(level, message, line, sourceID)

    def show_dev_tools(self):
        current_page = self.current_webview().page()
        if not hasattr(self, "dev_tools_window") or self.dev_tools_window is None:
            self.dev_tools_window = QWebEngineView()
            self.dev_tools_page = QWebEnginePage(self.profile, self.dev_tools_window)
            self.dev_tools_window.setPage(self.dev_tools_page)
            self.dev_tools_page.setInspectedPage(current_page)
            self.dev_tools_window.setWindowTitle("Developer Tools")
            self.dev_tools_window.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "ico.png")))
            self.dev_tools_window.resize(800, 600)
            self.dev_tools_window.show()
        else:
            self.dev_tools_page.setInspectedPage(current_page)
            self.dev_tools_window.show()
            self.dev_tools_window.raise_()

    def init_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+W"), self, activated=self.close_current_tab_action)
        QShortcut(QKeySequence("Ctrl+Tab"), self, activated=self.switch_next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, activated=self.switch_prev_tab)
        QShortcut(QKeySequence("F12"), self, activated=self.show_dev_tools)
        QShortcut(QKeySequence("Ctrl+Shift+C"), self, activated=self.open_chatgpt_sidebar)

    def handle_download(self, download_item: QWebEngineDownloadRequest):
        mode = self.settings.get("download_mode", "ask")
        if mode == "ask":
            # Запрос у пользователя папки для загрузок
            path = QFileDialog.getExistingDirectory(self, "Выберите папку для загрузок")
            if path:
                download_item.setDownloadDirectory(path)
            else:
                download_item.cancel()
                return
        elif mode == "custom":
            # Используем кастомный путь, если он задан и существует
            custom_path = self.settings.get("download_path", "")
            if custom_path and os.path.exists(custom_path):
                download_item.setDownloadDirectory(custom_path)
            else:
                # Если кастомный путь не указан или не существует, используем папку по умолчанию
                download_item.setDownloadDirectory(
                    QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
                )
        else:  # Режим "default"
            download_item.setDownloadDirectory(
                QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
            )
        self.download_manager.add_download(download_item)
        download_item.accept()
        self.animate_download()

    def animate_download(self):
        final_size = QSize(30, 30)
        icon_path = os.path.join(ICONS_DIR, "install.png")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(ICONS_DIR, "ico.png")
        pix = QPixmap(icon_path)
        pix = pix.scaled(final_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        rounded = QPixmap(final_size)
        rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, final_size.width(), final_size.height()), 6, 6)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pix)
        painter.end()
        pix = rounded
        label = QLabel(self)
        label.setPixmap(pix)
        label.setStyleSheet("background: transparent; border: none;")
        opacity_effect = QGraphicsOpacityEffect(label)
        label.setGraphicsEffect(opacity_effect)
        opacity_effect.setOpacity(1.0)
        start_factor = 1.3
        start_size = QSize(int(final_size.width() * start_factor),
                           int(final_size.height() * start_factor))
        label.resize(start_size)
        label.show()
        center = self.rect().center()
        label.move(center.x() - start_size.width() // 2, center.y() - start_size.height() // 2)
        anim_group = QSequentialAnimationGroup(self)
        first_pos_anim = QPropertyAnimation(label, b"pos")
        first_pos_anim.setDuration(500)
        first_pos_anim.setStartValue(label.pos())
        first_pos_anim.setEndValue(QPoint(label.x(), label.y() + 50))
        first_pos_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        final_btn_pos = self.download_btn.mapToGlobal(self.download_btn.rect().center())
        final_btn_pos = self.mapFromGlobal(final_btn_pos)
        second_pos_anim = QPropertyAnimation(label, b"pos")
        second_pos_anim.setDuration(700)
        second_pos_anim.setStartValue(QPoint(label.x(), label.y() + 50))
        second_pos_anim.setEndValue(QPoint(final_btn_pos.x() - final_size.width() // 2,
                                           final_btn_pos.y() - final_size.height() // 2))
        second_pos_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        size_anim = QPropertyAnimation(label, b"size")
        size_anim.setDuration(700)
        size_anim.setStartValue(start_size)
        size_anim.setEndValue(final_size)
        size_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(700)
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.0)
        opacity_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        parallel_group = QParallelAnimationGroup()
        parallel_group.addAnimation(second_pos_anim)
        parallel_group.addAnimation(size_anim)
        parallel_group.addAnimation(opacity_anim)
        anim_group.addAnimation(first_pos_anim)
        anim_group.addAnimation(parallel_group)
        def on_finished():
            label.hide()
            label.deleteLater()
        anim_group.finished.connect(on_finished)
        anim_group.start()
        self.download_animations.append(anim_group)

    def add_new_tab(self, qurl: QUrl = None, label="Новая вкладка"):
        # Если URL не передан, подставляем локальный index.html
        if qurl is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            if self.is_private:
                # Приватный режим
                homepage_path = os.path.join(base_dir, "site", "private", "index.html")
            else:
                # Обычный режим
                homepage_path = os.path.join(base_dir, "site", "global", "index.html")

            # Преобразуем путь к файлу в формат file://
            qurl = QUrl.fromLocalFile(homepage_path)

        # Создаём новый QWebEngineView
        browser = QWebEngineView()

        # Добавляем вкладку (просто создаём, но не отображаем)
        index = self.tabs.addTab(browser, label)

        # Устанавливаем кастомную страницу (если нужно)
        browser.setPage(CustomWebEnginePage(self.profile, browser, self))

        # Загружаем URL
        browser.setUrl(qurl)

        # Подключаем сигналы (иконка, заголовок, история)
        browser.urlChanged.connect(lambda url, b=browser: self.update_tab_title(b, url))
        browser.iconChanged.connect(lambda icon, b=browser: self.update_tab_icon(b, icon))
        browser.loadFinished.connect(lambda _: self.save_current_history())

        # Делаем вкладку активной
        self.tabs.setCurrentIndex(index)

        # При изменении заголовка меняем название вкладки
        browser.page().titleChanged.connect(
            lambda title, idx=index: self.tabs.setTabText(idx, title)
        )

        return browser
    # Исправленная функция: первым параметром – браузер (QWebEngineView), вторым – URL (QUrl)
    def update_tab_title(self, browser, url):
        index = self.tabs.indexOf(browser)
        if index != -1:
            title = browser.title()
            self.tabs.setTabText(index, title)
            self.tabs.setTabToolTip(index, url.toString())

    def update_tab_icon(self, browser, icon):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabIcon(index, icon)

    def navigate_back(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.back()

    def navigate_forward(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.forward()

    def navigate_refresh(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.reload()

    def navigate_to_url(self):
        text = self.urlbar.text().strip()
        if not text:
            return
        if "." not in text and " " in text:
            query = urllib.parse.quote_plus(text)
            if self.is_private:
                url = "https://duckduckgo.com/?q=" + query
            else:
                engine = self.settings["search_engine"]
                base = ENGINE_URLS.get(engine, ENGINE_URLS["google"])
                url = base + query
        elif "." not in text and not text.startswith("http"):
            query = urllib.parse.quote_plus(text)
            if self.is_private:
                url = "https://duckduckgo.com/?q=" + query
            else:
                engine = self.settings["search_engine"]
                base = ENGINE_URLS.get(engine, ENGINE_URLS["google"])
                url = base + query
        elif not text.startswith("http://") and not text.startswith("https://"):
            url = "http://" + text
        else:
            url = text
        if self.current_webview():
            self.current_webview().load(QUrl(url))
            
            

    def update_urlbar(self, index):
        webview = self.tabs.widget(index)
        if not webview:
            return

        # Получаем URL стандартным способом
        qurl = webview.page().url()  # Используем page().url(), а не webview.url()
        url_str = qurl.toString()

    # Обновляем адресную строку
        if url_str:
            if url_str.startswith("file://"):
                self.urlbar.setText("Файл")
            else:
                self.urlbar.setText(url_str)
        else:
            self.urlbar.setText("Загрузка...")  # Временно ставим "Загрузка..."

    # Функция для обновления после загрузки страницы
    # Обработчик загрузки страницы
    def on_load_finished():
        update_url()  # Обновляем URL после загрузки страницы

    # Функция обновления URL
    def update_url():
        qurl = webview.page().url().toString()
        if qurl:
            if qurl.startswith("file://"):
                self.urlbar.setText("Файл")
            else:
                self.urlbar.setText(qurl)
        else:
            self.urlbar.setText("Ошибка загрузки")
            
        # Обработчик изменения URL (например, если сайт делает редирект)
        def on_url_changed():
            update_url()  # Обновляем URL при изменении адреса

    # Подключаем сигналы
        webview.loadFinished.connect(on_load_finished)
        webview.urlChanged.connect(on_url_changed)

        # Первичное обновление (без него строка будет пустая, пока не загрузится страница)
        update_url()



    def close_current_tab(self, index):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(index)

    def close_current_tab_action(self):
        self.close_current_tab(self.tabs.currentIndex())

    def switch_next_tab(self):
        current = self.tabs.currentIndex()
        total = self.tabs.count()
        self.tabs.setCurrentIndex((current + 1) % total)

    def switch_prev_tab(self):
        current = self.tabs.currentIndex()
        total = self.tabs.count()
        self.tabs.setCurrentIndex((current - 1) % total)

    def update_bookmark_icon(self):
        self.bookmark_button.setIcon(QIcon(os.path.join(ICONS_DIR, "star.png")))

    def toggle_bookmark(self):
        view = self.current_webview()
        if not view:
            return
        url = view.url().toString()
        if not url:
            return
        bookmarks = load_bookmarks()
        for bm in bookmarks:
            if bm.get("url") == url:
                bookmarks.remove(bm)
                save_bookmarks(bookmarks)
                QMessageBox.information(self, "Закладки", "Страница удалена из закладок.")
                self.update_star_icon(url)
                return
        title = view.page().title()
        bookmarks.append({"title": title, "url": url})
        save_bookmarks(bookmarks)
        QMessageBox.information(self, "Закладки", f"Страница '{title}' добавлена в закладки.")
        self.update_star_icon(url)

    def show_history(self):
        if self.is_private:
            QMessageBox.information(self, "История", "В приватном режиме история не сохраняется.")
            return
        history_items = load_history_from_file()
        if not history_items:
            QMessageBox.information(self, "История", "История пуста.")
            return
        hist_win = HistoryWindow(history_items, self.load_url_from_history, self)
        hist_win.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        hist_win.show()

    def show_download_manager(self):
        if self.download_manager.isVisible():
            self.download_manager.hide()
        else:
            self.download_manager.show()

    def show_bookmarks_window(self):
        bookmarks = load_bookmarks()
        if not bookmarks:
            QMessageBox.information(self, "Закладки", "Нет сохранённых закладок.")
            return
        bm_win = BookmarksWindow(bookmarks, self.load_url_from_history, parent=self)
        bm_win.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        bm_win.show()


    def show_extensions_dialog(self):
        dlg = ExtensionsDialog(self)
        dlg.exec()

    def open_settings_dialog(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def show_first_launch_dialog(self):
        dlg = FirstLaunchDialog(self)
        dlg.exec()

    def update_extensions(self):
        self.load_custom_extensions()
    def tab_open_doubleclick(self, index):
        if index == -1:
            self.add_new_tab()

    def clear_browser_data_manually(self):
        clear_browser_data(self.profile, self.cache_path, self.storage_path)

    def inject_allowfullscreen_script(self):
        js_code = """
        document.addEventListener('webkitfullscreenchange', function(e) {
            if (!document.webkitIsFullScreen) {
                document.webkitExitFullscreen();
            }
        }, false);
        """
        script = QWebEngineScript()
        script.setName("AllowFullscreenScript")
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setRunsOnSubFrames(True)
        script.setSourceCode(js_code)
        self.profile.scripts().insert(script)
    def open_new_window(self):
        new_win = MainWindow(settings=self.settings)
        new_win.show()
        self.child_windows.append(new_win)

    def toggle_mode(self):
        new_mode = not self.is_private
        self.settings["is_private"] = new_mode
        save_settings(self.settings)
        new_win = MainWindow(settings=self.settings)
        new_win.show()
        self.close()

    def show_downloads_menu(self):
        menu = self.create_downloads_menu()
        global_pos = self.download_btn.mapToGlobal(self.download_btn.rect().bottomLeft())
        menu_width = menu.sizeHint().width()
        menu.exec(QPoint(global_pos.x() - menu_width, global_pos.y()))

    def inject_chatgpt_js(self, ok):
        if ok:
            js = """
            (function(){
                document.body.style.backgroundColor = "#1e1e1e";
                document.body.style.color = "#e0e0e0";
                var header = document.querySelector("header");
                if(header) { header.style.display = "none"; }
                var chatContainer = document.querySelector(".overflow-y-auto");
                if(chatContainer){
                    chatContainer.style.padding = "20px";
                    chatContainer.style.maxWidth = "800px";
                    chatContainer.style.margin = "0 auto";
                }
            })();
            """
            self.chatgpt_view.page().runJavaScript(js)

    def load_url_from_history(self, qurl):
        self.current_webview().load(qurl)

    def current_webview(self):
        return self.tabs.currentWidget()

    def update_star_icon(self, url: str):
        if self.is_url_bookmarked(url):
            self.bookmark_button.setIcon(QIcon(os.path.join(ICONS_DIR, "starfilled.png")))
        else:
            self.bookmark_button.setIcon(QIcon(os.path.join(ICONS_DIR, "star.png")))

    def is_url_bookmarked(self, url: str) -> bool:
        bookmarks = load_bookmarks()
        for bm in bookmarks:
            if bm.get("url") == url:
                return True
        return False

    def create_downloads_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2e2e2e;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #505050;
                color: #ffffff;
            }
        """)

        if self.download_manager.tree.topLevelItemCount() == 0:
            dummy_action = QAction("Нет загрузок", menu)
            dummy_action.setEnabled(False)
            menu.addAction(dummy_action)
        else:
            for i in range(self.download_manager.tree.topLevelItemCount()):
                item = self.download_manager.tree.topLevelItem(i)
                file_name = item.text(0)
                file_path = item.data(0, Qt.ItemDataRole.UserRole)

                widget = QWidget()
                hlayout = QHBoxLayout(widget)
                hlayout.setContentsMargins(5, 5, 5, 5)
                hlayout.setSpacing(10)

                # Метка с именем файла (с эффектом наведения)
                label = QLabel(file_name)
                label.setStyleSheet("""
                    QLabel {
                        color: #e0e0e0;
                        padding: 4px;
                        border-radius: 4px;
                    }
                    QLabel:hover {
                        background-color: #3a3a3a;
                        color: #ffffff;
                    }
                """)

                def make_label_click(item=item):
                    def on_click(event):
                        self.download_manager.open_downloaded_file(item, 0)

                    return on_click

                label.mousePressEvent = make_label_click()
                hlayout.addWidget(label)

                # Кнопка "Проводник" (с эффектом наведения)
                btn_explorer = QPushButton()
                btn_explorer.setIcon(QIcon(os.path.join(ICONS_DIR, "explorer.png")))
                btn_explorer.setFixedSize(24, 24)
                btn_explorer.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background-color: transparent;
                    }
                    QPushButton:hover {
                        background-color: #505050;
                        border-radius: 4px;
                    }
                """)

                def make_explorer_click(item=item):
                    def on_clicked():
                        path = item.data(0, Qt.ItemDataRole.UserRole)
                        if path and os.path.exists(path):
                            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(path)))

                    return on_clicked

                btn_explorer.clicked.connect(make_explorer_click())
                hlayout.addWidget(btn_explorer)

                act = QWidgetAction(menu)
                act.setDefaultWidget(widget)
                menu.addAction(act)

            menu.addSeparator()

            # Кнопка "Показать все загрузки"
            show_all_action = QAction(QIcon(os.path.join(ICONS_DIR, "download.png")), "Показать все загрузки", menu)
            show_all_action.triggered.connect(self.show_download_manager)
            menu.addAction(show_all_action)

        return menu

    def open_chatgpt_sidebar(self):
        if self.chatgpt_dock is not None:
            if self.chatgpt_dock.isVisible():
                self.chatgpt_dock.hide()
            else:
                self.chatgpt_dock.show()
            return
        self.chatgpt_dock = QDockWidget("ChatGPT", self)
        self.chatgpt_dock.setMinimumSize(QSize(300, 200))
        self.chatgpt_dock.resize(300, 200)
        self.chatgpt_view = QWebEngineView(self.chatgpt_dock)
        page = CustomWebEnginePage(self.profile, self.chatgpt_view, self)
        self.chatgpt_view.setPage(page)
        self.chatgpt_view.load(QUrl("https://chat.openai.com/chat"))
        self.chatgpt_dock.setWidget(self.chatgpt_view)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.chatgpt_dock)
        self.chatgpt_view.loadFinished.connect(self.inject_chatgpt_js)

def set_dark_palette(app):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    app.setPalette(dark_palette)

# -------------------- Main --------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Загрузка настроек
    settings = load_settings()
    
    # Глобально задаём шрифт
    app.setFont(QFont(settings["font_family"], settings["font_size"]))
    
    # Применяем тёмную палитру
    set_dark_palette(app)
    
    # Если есть файл QSS для тёмной темы, загружаем его
    qss_path = os.path.join(BASE_DIR, "dark_theme.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    
    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec())
