#!/usr/bin/env python3
import sys, os, json, datetime, time, urllib.parse, shutil
from pathlib import Path

from PyQt6.QtCore import (
    QUrl, QSize, Qt, QTimer, QPropertyAnimation, QEasingCurve,
    QSequentialAnimationGroup, QParallelAnimationGroup, QPoint, QStandardPaths
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QTabWidget, QLineEdit, QProgressBar, QDialog,
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QToolButton, QTreeWidget, QTreeWidgetItem,
    QFileDialog, QMessageBox, QPushButton, QStatusBar, QGraphicsOpacityEffect, QMenu,
    QSizePolicy, QFontDialog, QComboBox, QCheckBox, QInputDialog, QTextEdit
)
from PyQt6.QtGui import (
    QIcon, QAction, QDesktopServices, QFont, QPixmap, QShortcut, QKeySequence
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile, QWebEnginePage, QWebEngineScript, QWebEngineDownloadRequest,
    QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo, QWebEngineCookieStore
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

USER_SCRIPT_FILE = os.path.join(BASE_DIR, "adblock.js")       # стандартное расширение "miblock"
DARKREADER_FILE = os.path.join(BASE_DIR, "darkreader.js")     # скрипт "dark reader"

ENGINE_URLS = {
    "google": "https://www.google.com/search?q=",
    "yandex": "https://yandex.ru/search/?text=",
    "bing": "https://www.bing.com/search?q="
}

LANGS = ["ru", "en"]
TRANSLATIONS = {
    "ru": {
        "new_tab": "Новая вкладка",
        "new_window": "Новое окно",
        "private_on": "Новое приватное окно",
        "private_off": "Вернуться в обычный режим",
        "history": "Журнал (история)",
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
        "default_extension_description": "адблок разработан MiHaTsKiYi специально для MiHa Browser",
        "bookmarks": "Закладки",
        "add_bookmark": "Добавить закладку",
        "manage_bookmarks": "Управлять закладками",
        "bookmarks_title": "Мои закладки"
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
        "default_extension_description": "MiBlock is an adblock developed by MiHaTsKiYi specifically for MiHa Browser",
        "bookmarks": "Bookmarks",
        "add_bookmark": "Add Bookmark",
        "manage_bookmarks": "Manage Bookmarks",
        "bookmarks_title": "My Bookmarks"
    }
}

# -------------------- Loading and Saving Configurations --------------------
def load_settings():
    default_settings = {
        "is_private": False,
        "search_engine": "google",
        "language": "ru",
        "font_family": "Fira Code Mono",
        "font_size": 10,
        "homepage": "https://www.google.com",
        "download_mode": "ask",
        "download_path": "",
        "delete_on_close": False
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in default_settings.items():
                if k not in data:
                    data[k] = v
            return data
        except:
            return default_settings
    else:
        return default_settings

def save_settings(settings: dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

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

# -------------------- Cache and Data Clearing --------------------
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
    return total_bytes // (1024*1024)

def clear_browser_data(profile: QWebEngineProfile, cache_path: str, storage_path: str):
    cookie_store: QWebEngineCookieStore = profile.cookieStore()
    cookie_store.deleteAllCookies()
    shutil.rmtree(cache_path, ignore_errors=True)
    shutil.rmtree(storage_path, ignore_errors=True)
    os.makedirs(cache_path, exist_ok=True)
    os.makedirs(storage_path, exist_ok=True)

# -------------------- AdBlockInterceptor --------------------
class AdBlockInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Обновлённый список рекламных паттернов – включаем и блокировку по названию в YouTube
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
        host = url.host().lower()
        full_url = url.toString().lower()
        # Белый список для Google Maps
        if "maps.google.com" in host or "googleapis.com/maps" in full_url:
            return
        for pattern in self.ad_hosts:
            if pattern in full_url:
                info.block(True)
                return
        for w in self.big_filters:
            if w in full_url:
                info.block(True)
                return

# -------------------- CustomWebEnginePage --------------------
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

# -------------------- ManageDataDialog --------------------
class ManageDataDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Управление данными")
        self.setStyleSheet("""
            QDialog { 
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
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

# -------------------- ManageExceptionsDialog --------------------
class ManageExceptionsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Управление исключениями")
        self.setStyleSheet("""
            QDialog { 
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
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

# -------------------- DownloadManagerWindow --------------------
class DownloadManagerWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Загрузки")
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "download.png")))
        self.resize(700, 500)
        self.setStyleSheet("""
            QDialog { 
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
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
        self.timer.start(200)
        self.speed_smoothing = 0.1
        if not self.parent().is_private:
            self.load_persistent_downloads()
        self.setLayout(layout)

    def load_persistent_downloads(self):
        persistent_downloads = load_downloads_from_file()
        for d in persistent_downloads:
            tree_item = QTreeWidgetItem([
                d.get("file_name", ""), "100%", "0 B/s", d.get("status", "Завершено"), ""
            ])
            tree_item.setData(0, Qt.ItemDataRole.UserRole, d.get("file_path", ""))
            self.tree.addTopLevelItem(tree_item)

    def update_persistent_downloads(self):
        if self.parent().is_private:
            return
        downloads_list = []
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            downloads_list.append({
                "file_name": item.text(0),
                "file_path": item.data(0, Qt.ItemDataRole.UserRole),
                "status": item.text(3)
            })
        save_downloads_to_file(downloads_list)

    def format_speed(self, speed):
        if speed < 1024:
            return f"{speed:.0f} B/s"
        elif speed < 1024*1024:
            return f"{speed/1024:.1f} KB/s"
        else:
            return f"{speed/(1024*1024):.1f} MB/s"

    def add_download(self, download_item):
        tree_item = QTreeWidgetItem([
            download_item.downloadFileName(), "0%", "0 B/s", "Загрузка", ""
        ])
        full_path = os.path.join(download_item.downloadDirectory(), download_item.downloadFileName())
        tree_item.setData(0, Qt.ItemDataRole.UserRole, full_path)
        self.tree.addTopLevelItem(tree_item)
        self.downloads[id(download_item)] = (download_item, tree_item)
        self.speed_info[id(download_item)] = (download_item.receivedBytes(), time.time(), 0.0)

        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        control_layout.setContentsMargins(0,0,0,0)
        control_layout.setSpacing(5)
        pause_btn = QPushButton("Пауза")
        pause_btn.setMinimumWidth(80)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setMinimumWidth(80)
        control_layout.addWidget(pause_btn)
        control_layout.addWidget(cancel_btn)
        self.tree.setItemWidget(tree_item, 4, control_widget)

        pause_btn.clicked.connect(
            lambda _, d=download_item, ti=tree_item, btn=pause_btn: self.toggle_pause(d, ti, btn)
        )
        cancel_btn.clicked.connect(
            lambda _, d=download_item, ti=tree_item: self.cancel_download(d, ti)
        )

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

    def update_all_downloads(self):
        current_time = time.time()
        for key, (download_item, tree_item) in list(self.downloads.items()):
            total = download_item.totalBytes()
            received = download_item.receivedBytes()
            if total > 0:
                tree_item.setText(1, f"{int(received/total*100)}%")
            else:
                tree_item.setText(1, "0%")
            if download_item.isPaused():
                tree_item.setText(2, "0 B/s")
                smoothed_speed = 0.0
            else:
                prev_received, prev_time, prev_smoothed_speed = self.speed_info.get(key, (0, current_time, 0.0))
                delta_time = current_time - prev_time
                if delta_time > 0:
                    instantaneous_speed = (received - prev_received) / delta_time
                    smoothed_speed = (self.speed_smoothing * instantaneous_speed +
                                      (1 - self.speed_smoothing) * prev_smoothed_speed)
                    tree_item.setText(2, self.format_speed(smoothed_speed))
                else:
                    smoothed_speed = prev_smoothed_speed
                    tree_item.setText(2, "0 B/s")
            self.speed_info[key] = (received, current_time, smoothed_speed)
            if download_item.isFinished():
                tree_item.setText(3, "Завершено")
                self.tree.setItemWidget(tree_item, 4, None)
                if key not in self.finished_downloads:
                    finished_info = {
                        "file_name": download_item.downloadFileName(),
                        "file_path": os.path.join(
                            download_item.downloadDirectory(),
                            download_item.downloadFileName()
                        ),
                        "timestamp": datetime.datetime.now().isoformat(),
                        "status": "Завершено"
                    }
                    if not self.parent().is_private:
                        downloads_list = load_downloads_from_file()
                        downloads_list.append(finished_info)
                        save_downloads_to_file(downloads_list)
                    self.finished_downloads.add(key)
            elif download_item.isPaused():
                tree_item.setText(3, "Пауза")
            else:
                tree_item.setText(3, "Загрузка")

    def open_downloaded_file(self, item, column):
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and os.path.exists(file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        else:
            QMessageBox.warning(self, "Файл не найден", "Такого файла не существует!")
            f = item.font(0)
            f.setStrikeOut(True)
            item.setFont(0, f)
            QTimer.singleShot(1000, lambda: self.remove_download_item(item))

    def remove_download_item(self, item):
        idx = self.tree.indexOfTopLevelItem(item)
        if idx != -1:
            self.tree.takeTopLevelItem(idx)
            self.update_persistent_downloads()

# -------------------- HistoryWindow --------------------
class HistoryWindow(QDialog):
    def __init__(self, history_items, load_callback, parent=None):
        super().__init__(parent)
        self.setWindowTitle("История")
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "history.png")))
        self.load_callback = load_callback
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
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
        self.resize(300,600)

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

# -------------------- BookmarksWindow --------------------
class BookmarksWindow(QDialog):
    def __init__(self, bookmarks, load_callback, parent=None):
        super().__init__(parent)
        self.parent_win = parent
        self.load_callback = load_callback
        self.bookmarks = bookmarks[:]  # копия списка
        self.setWindowTitle(self.parent_win.tr_str("bookmarks_title"))
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "star.png")))
        self.resize(400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
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

# -------------------- ExtensionsDialog --------------------
class ExtensionsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_win = parent
        self.setModal(True)
        self.setWindowTitle(self.tr_str("extensions_title"))
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
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
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        btn_layout.addWidget(self.btn_toggle)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        self.btn_add.clicked.connect(self.add_extension)
        self.btn_remove.clicked.connect(self.remove_extension)
        self.btn_toggle.clicked.connect(self.toggle_selected_extension)
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
        self.refresh_tree()
        self.setLayout(layout)

    def tr_str(self, key: str) -> str:
        lang = self.parent_win.settings["language"]
        return TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, key)

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

# -------------------- SettingsDialog --------------------
class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_win = parent
        self.setModal(True)
        self.setWindowTitle(self.tr_str("settings_title"))
        self.setWindowOpacity(0.0)
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.fade_animation.start()
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3c3c3c, stop:1 #2a2a2a
                );
                border: 2px solid #555;
                border-radius: 10px;
            }
            QLabel, QComboBox, QLineEdit, QPushButton, QCheckBox {
                font-size: 14px;
                color: #e0e0e0;
            }
            QComboBox, QLineEdit {
                background-color: #4a4a4a;
                border: 1px solid #777;
                padding: 4px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #5a5a5a;
                border: 1px solid #666;
                padding: 6px 12px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #6a6a6a; }
        """)
        self.resize(480, 420)
        self.init_ui()

    def tr_str(self, key: str) -> str:
        lang = self.parent_win.settings["language"]
        return TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, key)

    def init_ui(self):
        layout = QVBoxLayout(self)
        hl_engine = QHBoxLayout()
        lbl_engine = QLabel(self.tr_str("search_engine") + ":")
        self.cmb_engine = QComboBox()
        self.cmb_engine.addItems(["google", "yandex", "bing"])
        self.cmb_engine.setCurrentText(self.parent_win.settings["search_engine"])
        if self.parent_win.is_private:
            self.cmb_engine.setEnabled(False)
        hl_engine.addWidget(lbl_engine)
        hl_engine.addWidget(self.cmb_engine)
        layout.addLayout(hl_engine)
        hl_home = QHBoxLayout()
        lbl_home = QLabel(self.tr_str("homepage") + ":")
        self.le_home = QLineEdit()
        self.le_home.setText(self.parent_win.settings["homepage"])
        if self.parent_win.is_private:
            self.le_home.setEnabled(False)
        hl_home.addWidget(lbl_home)
        hl_home.addWidget(self.le_home)
        layout.addLayout(hl_home)
        hl_dl = QHBoxLayout()
        lbl_dl = QLabel(self.tr_str("download_mode") + ":")
        self.cmb_dl = QComboBox()
        self.cmb_dl.addItems([self.tr_str("ask"), self.tr_str("default"), self.tr_str("custom")])
        self.cmb_dl.setCurrentIndex({"ask":0, "default":1, "custom":2}.get(
            self.parent_win.settings.get("download_mode", "ask"), 0
        ))
        hl_dl.addWidget(lbl_dl)
        hl_dl.addWidget(self.cmb_dl)
        layout.addLayout(hl_dl)
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
        hl_lang = QHBoxLayout()
        lbl_lang = QLabel(self.tr_str("language") + ":")
        self.cmb_lang = QComboBox()
        self.cmb_lang.addItems(LANGS)
        self.cmb_lang.setCurrentText(self.parent_win.settings["language"])
        hl_lang.addWidget(lbl_lang)
        hl_lang.addWidget(self.cmb_lang)
        layout.addLayout(hl_lang)
        hl_font = QHBoxLayout()
        lbl_font = QLabel(self.tr_str("font") + ":")
        self.btn_font = QPushButton(self.parent_win.settings["font_family"])
        self.btn_font.clicked.connect(self.choose_font)
        hl_font.addWidget(lbl_font)
        hl_font.addWidget(self.btn_font)
        layout.addLayout(hl_font)
        layout.addSpacing(10)
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
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancel")
        btn_exit = QPushButton(self.tr_str("exit"))
        btn_ok.clicked.connect(self.on_ok)
        btn_cancel.clicked.connect(self.on_cancel)
        btn_exit.clicked.connect(self.parent_win.close)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_exit)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def choose_download_path(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите папку для загрузок")
        if path:
            self.le_path.setText(path)

    def update_dl_mode(self, idx):
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
        font, ok = QFontDialog.getFont(initial_font, self, "Выберите шрифт")
        if ok:
            self.btn_font.setText(font.family())

    def on_delete_data(self):
        reply = QMessageBox.question(
            self, "Очистить данные",
            "Вы действительно хотите удалить все куки и данные сайтов?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.parent_win.clear_browser_data_manually()
            QMessageBox.information(self, "Очистка", "Данные успешно удалены!")

    def on_ok(self):
        new_engine = self.cmb_engine.currentText()
        new_home = self.le_home.text()
        new_lang = self.cmb_lang.currentText()
        new_font_family = self.btn_font.text()
        idx_dl = self.cmb_dl.currentIndex()
        dl_map = {0: "ask", 1: "default", 2: "custom"}
        new_dl_mode = dl_map.get(idx_dl, "ask")
        new_dl_path = self.le_path.text()
        self.parent_win.settings["search_engine"] = new_engine
        self.parent_win.settings["homepage"] = new_home
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

# -------------------- MainWindow --------------------
class MainWindow(QMainWindow):
    def __init__(self, settings=None):
        super().__init__()
        if settings is None:
            settings = load_settings()
        self.settings = settings
        self.is_private = self.settings["is_private"]
        self.dev_tools_window = None
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
        self.init_shortcuts()
        self.update_extensions()

    def closeEvent(self, event):
        if self.settings.get("delete_on_close", False):
            self.clear_browser_data_manually()
        event.accept()

    def tr_str(self, key: str) -> str:
        lang = self.settings["language"]
        return TRANSLATIONS.get(lang, TRANSLATIONS["ru"]).get(key, key)

    def apply_settings(self):
        font_family = self.settings["font_family"]
        font_size = self.settings["font_size"]
        self.setFont(QFont(font_family, font_size))

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
            script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
            script.setSourceCode(code)
            self.profile.scripts().insert(script)
        if os.path.exists(DARKREADER_FILE):
            with open(DARKREADER_FILE, "r", encoding="utf-8") as f:
                code = f.read()
            dark_script = QWebEngineScript()
            dark_script.setName("DarkReaderScript")
            dark_script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
            dark_script.setRunsOnSubFrames(True)
            dark_script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
            dark_script.setSourceCode(code)
            self.profile.scripts().insert(dark_script)
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16,16))
        navtb.setStyleSheet("""
            QToolBar {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e1e1e, stop:1 #252525);
                border-bottom: 1px solid #444; 
                spacing: 10px; 
                padding: 5px; 
            }
            QToolButton {
                background-color: transparent;
                border: none;
                color: #e0e0e0;
            }
            QToolButton:hover {
                background-color: #323232;
            }
            QLineEdit {
                background-color: #2b2b2b;
                border: 1px solid #555;
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
        search_layout.setContentsMargins(0,0,0,0)
        search_layout.setSpacing(5)
        self.urlbar = QLineEdit()
        self.urlbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        search_layout.addWidget(self.urlbar)
        navtb.addWidget(search_widget)
        self.bookmark_button = QToolButton()
        self.bookmark_button.setIcon(QIcon(os.path.join(ICONS_DIR, "star.png")))
        self.bookmark_button.clicked.connect(self.toggle_bookmark)
        navtb.addWidget(self.bookmark_button)
        self.history_btn = QToolButton()
        self.history_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "history.png")))
        self.history_btn.clicked.connect(self.show_history)
        if not self.is_private:
            navtb.addWidget(self.history_btn)
        download_btn = QToolButton()
        download_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "download.png")))
        download_btn.clicked.connect(self.show_download_manager)
        navtb.addWidget(download_btn)
        self.download_button = download_btn
        menu_button = QToolButton()
        menu_button.setIcon(QIcon(os.path.join(ICONS_DIR, "settings.png")))
        menu_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #2e2e2e;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 10px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #505050;
                border-radius: 5px;
            }
        """)
        new_tab_action = QAction(self.tr_str("new_tab"), self)
        new_tab_action.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_action.triggered.connect(lambda: self.add_new_tab())
        menu.addAction(new_tab_action)
        new_window_action = QAction(self.tr_str("new_window"), self)
        new_window_action.setShortcut(QKeySequence("Ctrl+N"))
        new_window_action.triggered.connect(self.open_new_window)
        menu.addAction(new_window_action)
        self.toggle_private_action = QAction("", self)
        self.toggle_private_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        self.toggle_private_action.triggered.connect(self.toggle_mode)
        menu.addAction(self.toggle_private_action)
        if self.is_private:
            self.toggle_private_action.setText(self.tr_str("private_off"))
        else:
            self.toggle_private_action.setText(self.tr_str("private_on"))
        history_action = QAction(self.tr_str("history"), self)
        history_action.triggered.connect(self.show_history)
        menu.addAction(history_action)
        downloads_action = QAction(self.tr_str("downloads"), self)
        downloads_action.triggered.connect(self.show_download_manager)
        menu.addAction(downloads_action)
        bookmarks_action = QAction(self.tr_str("bookmarks"), self)
        bookmarks_action.triggered.connect(self.show_bookmarks_window)
        menu.addAction(bookmarks_action)
        menu.addSeparator()
        extensions_action = QAction(self.tr_str("extensions"), self)
        extensions_action.triggered.connect(self.show_extensions_dialog)
        menu.addAction(extensions_action)
        settings_action = QAction(self.tr_str("settings"), self)
        settings_action.triggered.connect(self.open_settings_dialog)
        menu.addAction(settings_action)
        exit_action = QAction(self.tr_str("exit"), self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        menu.addAction(exit_action)
        menu_button.setMenu(menu)
        menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        navtb.addWidget(menu_button)
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(120)
        self.progress.setTextVisible(False)
        self.progress.hide()
        navtb.addWidget(self.progress)
        self.download_manager = DownloadManagerWindow(self)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
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
        if self.is_private:
            self.add_new_tab(QUrl("https://duckduckgo.com"), "DuckDuckGo")
        else:
            homepage = self.settings.get("homepage", "https://www.google.com")
            self.add_new_tab(QUrl(homepage), "Home")

    def init_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+W"), self, activated=self.close_current_tab_action)
        QShortcut(QKeySequence("Ctrl+Tab"), self, activated=self.switch_next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, activated=self.switch_prev_tab)
        QShortcut(QKeySequence("F12"), self, activated=self.show_dev_tools)

    # Добавлена функция show_dev_tools для устранения ошибки AttributeError
    def show_dev_tools(self):
        QMessageBox.information(self, "Dev Tools", "Developer Tools are not implemented yet.")

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
        save_extensions_to_file(ext_list)

    def update_extensions(self):
        self.load_custom_extensions()

    def clear_browser_data_manually(self):
        clear_browser_data(self.profile, self.cache_path, self.storage_path)

    def toggle_mode(self):
        new_mode = not self.is_private
        self.settings["is_private"] = new_mode
        save_settings(self.settings)
        new_win = MainWindow(settings=self.settings)
        new_win.show()
        self.close()

    def open_settings_dialog(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def show_extensions_dialog(self):
        dlg = ExtensionsDialog(self)
        dlg.exec()

    def open_new_window(self):
        new_win = MainWindow(settings=self.settings)
        new_win.show()
        self.child_windows.append(new_win)

    def switch_next_tab(self):
        if self.tabs.count() > 1:
            self.tabs.setCurrentIndex((self.tabs.currentIndex() + 1) % self.tabs.count())

    def switch_prev_tab(self):
        if self.tabs.count() > 1:
            self.tabs.setCurrentIndex((self.tabs.currentIndex() - 1) % self.tabs.count())

    def close_current_tab_action(self):
        if self.tabs.count() > 1:
            self.close_current_tab(self.tabs.currentIndex())

    def close_current_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def tab_open_doubleclick(self, index):
        if index == -1:
            self.add_new_tab()

    def navigate_back(self):
        self.current_webview().back()

    def navigate_forward(self):
        self.current_webview().forward()

    def navigate_refresh(self):
        self.current_webview().reload()

    def current_webview(self):
        return self.tabs.currentWidget()

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
        elif not (text.startswith("http://") or text.startswith("https://")):
            url = "http://" + text
        else:
            url = text
        q = QUrl(url)
        if q.isValid():
            self.current_webview().load(q)

    def update_urlbar(self, index):
        if self.tabs.widget(index):
            w = self.tabs.widget(index)
            new_url = w.url().toString()
            self.urlbar.setText(new_url)
            self.update_star_icon(new_url)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            if self.is_private:
                qurl = QUrl("https://duckduckgo.com")
                label = "DuckDuckGo"
            else:
                engine = self.settings["search_engine"]
                base = ENGINE_URLS.get(engine, ENGINE_URLS["google"])
                label = engine.capitalize()
                qurl = QUrl(base)
        browser = QWebEngineView()
        page = CustomWebEnginePage(self.profile, browser, self)
        browser.setPage(page)
        browser.page().fullScreenRequested.connect(self.handleFullScreenRequested)
        browser.load(qurl)
        idx = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(idx)
        browser.urlChanged.connect(lambda url, b=browser: self.update_tab_url(b, url))
        browser.loadFinished.connect(lambda ok, b=browser: self.on_load_finished(b))
        browser.loadProgress.connect(lambda prog, b=browser: self.update_progress(prog, b))
        self.animate_tab_open(browser)
        return browser

    def handleFullScreenRequested(self, request):
        request.accept()
        if request.toggleOn():
            self.showFullScreen()
        else:
            self.showNormal()

    def update_tab_url(self, browser, url):
        if self.tabs.currentWidget() == browser:
            self.urlbar.setText(url.toString())
            self.update_star_icon(url.toString())

    def update_tab_title(self, browser):
        idx = self.tabs.indexOf(browser)
        if idx != -1:
            title = browser.page().title()
            self.tabs.setTabText(idx, title)
            return title
        return ""

    def update_progress(self, progress, browser):
        if self.current_webview() == browser:
            self.progress.setValue(progress)
            if progress < 100:
                self.progress.show()
            else:
                self.progress.hide()

    def on_load_finished(self, browser):
        title = self.update_tab_title(browser)
        url = browser.page().url().toString()
        if not self.is_private and title and url:
            history = load_history_from_file()
            history.append({
                "url": url,
                "title": title,
                "timestamp": datetime.datetime.now().isoformat()
            })
            save_history_to_file(history)
        effect = QGraphicsOpacityEffect(browser)
        browser.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(300)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()
        self.animations.append(animation)
        animation.finished.connect(lambda: self.animations.remove(animation))
        if self.tabs.currentWidget() == browser:
            self.update_star_icon(url)

    def is_url_bookmarked(self, url: str) -> bool:
        bookmarks = load_bookmarks()
        for bm in bookmarks:
            if bm.get("url") == url:
                return True
        return False

    def update_star_icon(self, url: str):
        if self.is_url_bookmarked(url):
            self.bookmark_button.setIcon(QIcon(os.path.join(ICONS_DIR, "starfilled.png")))
        else:
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

    def show_bookmarks_window(self):
        bookmarks = load_bookmarks()
        bm_win = BookmarksWindow(bookmarks, self.load_url_from_history, self)
        bm_win.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        bm_win.show()

    def show_history(self):
        if self.is_private:
            return
        items = load_history_from_file()
        if not items:
            return
        hist_win = HistoryWindow(items, self.load_url_from_history, parent=self)
        self.history_windows.append(hist_win)
        hist_win.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        geom = self.geometry()
        hist_win.setGeometry(geom.x() + geom.width() - 300, geom.y(), 300, geom.height())
        hist_win.show()

    def load_url_from_history(self, url):
        self.current_webview().load(url)

    def show_download_manager(self):
        self.download_manager.show()
        self.download_manager.raise_()

    def handle_download(self, download_item: QWebEngineDownloadRequest):
        mode = self.settings.get("download_mode", "ask")
        if mode == "ask":
            dlg = QFileDialog(self, "Сохранить файл", download_item.downloadFileName())
            dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            dlg.setFileMode(QFileDialog.FileMode.AnyFile)
            dlg.setOption(QFileDialog.Option.DontUseNativeDialog, True)
            dlg.setStyleSheet("""
                QFileDialog {
                    background-color: #2b2b2b;
                    color: #e0e0e0;
                }
                QLineEdit {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QPushButton {
                    background-color: #808080;
                    border: none;
                    padding: 6px 12px;
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #707070;
                }
            """)
            if dlg.exec():
                filename = dlg.selectedFiles()[0]
            else:
                download_item.cancel()
                return
        elif mode == "default":
            filename = os.path.join(
                QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation),
                download_item.downloadFileName()
            )
        elif mode == "custom":
            path = self.settings.get("download_path", "")
            if not path:
                path = QFileDialog.getExistingDirectory(self, "Выберите папку для загрузок")
                if not path:
                    download_item.cancel()
                    return
            filename = os.path.join(path, download_item.downloadFileName())
        else:
            dlg = QFileDialog(self, "Сохранить файл", download_item.downloadFileName())
            dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            dlg.setFileMode(QFileDialog.FileMode.AnyFile)
            if dlg.exec():
                filename = dlg.selectedFiles()[0]
            else:
                download_item.cancel()
                return
        directory = os.path.dirname(filename)
        file_name = os.path.basename(filename)
        download_item.setDownloadDirectory(directory)
        download_item.setDownloadFileName(file_name)
        download_item.accept()
        self.download_manager.add_download(download_item)
        self.animate_download()

    def animate_tab_open(self, widget):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.start()
        self.animations.append(anim)
        anim.finished.connect(lambda: self.animations.remove(anim))

    def animate_download(self):
        if self.current_webview():
            center = self.current_webview().mapTo(self, self.current_webview().rect().center())
        else:
            center = self.rect().center()
        up_left = QPoint(center.x()-40, center.y()-30)
        down_right = QPoint(up_left.x()+80, up_left.y()+60)
        if hasattr(self, "download_button"):
            target = self.mapFromGlobal(self.download_button.mapToGlobal(self.download_button.rect().center()))
        else:
            target = self.rect().center()
        label = QLabel(self)
        icon = QIcon(os.path.join(ICONS_DIR, "install.png"))
        label.setPixmap(icon.pixmap(64,64))
        label.setFixedSize(64,64)
        label.move(center)
        label.show()
        opacity_effect = QGraphicsOpacityEffect(label)
        label.setGraphicsEffect(opacity_effect)
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(2000)
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.0)
        opacity_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        pos1 = QPropertyAnimation(label, b"pos")
        pos1.setDuration(500)
        pos1.setStartValue(center)
        pos1.setEndValue(up_left)
        pos1.setEasingCurve(QEasingCurve.Type.OutCubic)
        pos2 = QPropertyAnimation(label, b"pos")
        pos2.setDuration(600)
        pos2.setStartValue(up_left)
        pos2.setEndValue(down_right)
        pos2.setEasingCurve(QEasingCurve.Type.InOutCubic)
        pos3 = QPropertyAnimation(label, b"pos")
        pos3.setDuration(900)
        pos3.setStartValue(down_right)
        pos3.setEndValue(target)
        pos3.setEasingCurve(QEasingCurve.Type.InOutCubic)
        seq = QSequentialAnimationGroup()
        seq.addAnimation(pos1)
        seq.addAnimation(pos2)
        seq.addAnimation(pos3)
        group = QParallelAnimationGroup(self)
        group.addAnimation(seq)
        group.addAnimation(opacity_anim)
        group.start()
        self.animations.append(group)
        group.finished.connect(lambda: (label.deleteLater(), self.animations.remove(group), self.bounce_download_icon()))

    def bounce_download_icon(self):
        if not hasattr(self, "download_button"):
            return
        orig = self.download_button.iconSize()
        bounce = QPropertyAnimation(self.download_button, b"iconSize")
        bounce.setDuration(300)
        bounce.setKeyValueAt(0, orig)
        enlarged = QSize(orig.width()+6, orig.height()+6)
        bounce.setKeyValueAt(0.5, enlarged)
        bounce.setKeyValueAt(1, orig)
        bounce.setEasingCurve(QEasingCurve.Type.OutBounce)
        bounce.start()
        self.animations.append(bounce)
        bounce.finished.connect(lambda: self.animations.remove(bounce))

    def update_tab_url(self, browser, url):
        if self.tabs.currentWidget() == browser:
            self.urlbar.setText(url.toString())
            self.update_star_icon(url.toString())

# -------------------- Main Application --------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
