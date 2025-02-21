
<div align="center">
  <h1>MiHa Browser</h1>
  <p>Простой, современный и экспериментальный браузер на базе <strong>PyQt6 WebEngine</strong></p>
</div>

---

<div align="center">
  <h2>Наши логотипы</h2>
  <img src="https://github.com/user-attachments/assets/157e5338-114e-4f35-b72d-90637e0d60a5" alt="Логотип 1" width="150" style="margin: 0 20px;">
  <img src="https://github.com/user-attachments/assets/e1067a16-0b44-435c-a53d-ccfe4917a79d" alt="Логотип 2" width="150" style="margin: 0 20px;">
</div>

---

## Содержание

- [Описание](#описание)
- [Скриншоты](#скриншоты)
- [Установка](#установка)
- [Запуск](#запуск)
- [Основные возможности](#основные-возможности)
- [Структура проекта](#структура-проекта)
- [Известные проблемы](#известные-проблемы)
- [Лицензия](#лицензия)
- [Git: Клонирование репозитория и устранение ошибок](#git-клонирование-репозитория-и-устранение-ошибок)

---

## Описание

**MiHa Browser** создан для тех, кто ценит простоту и функциональность. Этот браузер предлагает:
- **Многовкладочный режим:** Легкое переключение между сайтами.
- **Приватный режим:** Исключает сохранение истории, куки и кэша для обеспечения конфиденциальности.
- **AdBlock:** Встроенная блокировка рекламы.
- **Dark Reader:** Опциональная тёмная тема для комфортного просмотра в условиях низкой освещённости.
- **Поддержка расширений:** Вы можете подключать пользовательские JS-скрипты для расширения функционала.  
  Готовые скрипты можно найти на [Greasy Fork](https://greasyfork.org/ru/scripts).  
- **Управление загрузками:** Отслеживание прогресса загрузок с возможностью приостановки и отмены.
- **Закладки и история:** Удобное сохранение избранных сайтов и просмотр истории посещений.
- **Выбор поисковой системы:** Возможность работы с Google, Яндекс, Bing и DuckDuckGo.

---

## Скриншоты

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/7bd10a7a-202c-44a6-9aa8-b1b1aff65075" alt="Скриншот 1" width="200">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/78238618-cad3-47ac-9044-da254d39a3fa" alt="Скриншот 2" width="200">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/8d15212e-79fb-4e68-ad27-7cc9064fc1aa" alt="Скриншот 3" width="200">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/4569f0ea-8648-4667-a25e-b3f1b82c058d" alt="Скриншот 4" width="200">
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/ecd72be9-97ab-495e-aeee-1d901aa3f9bb" alt="Скриншот 5" width="200">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/f90bd0ef-8cba-462e-a457-cd0fff2007f3" alt="Скриншот 6" width="200">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/9c40ca2e-e400-42d1-8991-33acdef7bec0" alt="Скриншот 7" width="200">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/b90d0cc3-9ad0-4dfb-8281-98b23d0d6ecb" alt="Скриншот 8" width="200">
    </td>
  </tr>
</table>

---

## Установка

1. **Требования:**  
   Убедитесь, что у вас установлен Python 3.9 или выше (рекомендуется Python 3.10+).

2. **Установка зависимостей:**  
   Откройте терминал и выполните:
   ```bash
   pip install PyQt6 PyQt6-WebEngine
   ```

3. **Загрузка проекта:**  
   Склонируйте или скачайте репозиторий в удобную папку:
   ```bash
   git clone https://github.com/MiHaTsKiYi13/MiHa-Browser.git
   ```
   Как скачать git? - 
   - [Git](#git)

4. **Проверка структуры файлов:**  
   В корневой папке должны находиться:
   - `main.pyw` (или `main.py`)
   - Папка `icons` с иконками
   - Скрипты `adblock.js` и `darkreader.js` (при необходимости)
   - Папка `configs` (создаётся автоматически для хранения настроек и истории)

---

## Запуск

Чтобы запустить проект, перейдите в каталог с проектом и выполните:

```bash
python main.py
```

Или дважды кликните по файлу `main.pyw`.

> **Совет:**  
> Если вам необходимо видеть сообщения об ошибках в консоли, переименуйте `main.pyw` в `main.py` или запустите файл `main.py`.

После запуска откроется окно **MiHa Browser**.  
*Пользователи Windows:* Можно запустить приложение двойным щелчком по файлу `main.pyw`.

---

## Основные возможности

- **Поисковые системы:**  
  Выбор между Google, Яндекс, Bing и DuckDuckGo.

- **Приватный режим:**  
  - Отсутствие сохранения истории и куки.
  - По умолчанию используется DuckDuckGo для поиска.

- **Многовкладочный режим:**  
  Возможность открытия нескольких сайтов в одном окне.

- **Управление загрузками:**  
  - Отображение прогресса загрузок.
  - Возможность приостановки и возобновления загрузок.
  - Настройка пути сохранения (запрос, путь по умолчанию или пользовательский).

- **Закладки:**  
  Быстрое добавление и управление избранными сайтами.

- **История посещений:**  
  Ведение журнала посещённых сайтов (отключается в приватном режиме).

- **Расширения:**  
  Подключение пользовательских JS-скриптов (например, AdBlock или Dark Reader).

- **Очистка данных:**  
  Удобное удаление куки и кэша через интерфейс приложения.

- **Настройки:**  
  Выбор языка (русский/английский), настройка шрифта, стартовой страницы и других параметров.

---

## Структура проекта

```bash
MiHa-Browser/
├── icons/                # Иконки приложения
├── configs/              # Папка для хранения настроек, истории и других данных (создаётся автоматически)
├── extensions/           # Папка с расширениями для браузера
├── main.pyw (или main.py)# Основной файл запуска приложения
└── README.md             # Этот файл
```

---

## Известные проблемы

- **DevTools:**  
  Полноценный набор инструментов разработчика отсутствует – при нажатии F12 выводится только сообщение.

- **Ошибки в Windows:**  
  При запуске файла с расширением `.pyw` ошибки не отображаются в консоли (для отладки переименуйте в `.py`).

- **Расположение папки `icons`:**  
  Папка должна находиться в одной директории с `main.pyw`, иначе некоторые иконки могут не загрузиться.

---

## Лицензия

Проект распространяется под свободной лицензией по вашему выбору. Вы можете модифицировать, распространять и использовать данный код в своих проектах.

---

<div align="center">
  <em>MiHa Browser – экспериментальный проект, который может стать отличной основой для создания собственного браузера на базе PyQt6-WebEngine.</em>
</div>

---

## Git: Клонирование репозитория и устранение ошибок

1. **Проверка установки Git:**  
   Откройте терминал и выполните:
   ```bash
   git --version
   ```
   - Если Git установлен, вы увидите версию, например:
     ```
     git version 2.x.x
     ```
   - Если Git не установлен, появится сообщение об ошибке:
     ```
     'git' is not recognized as an internal or external command, operable program or batch file.
     ```
     В этом случае установите Git, следуя инструкциям ниже.

2. **Клонирование репозитория:**  
   Для клонирования репозитория выполните:
   ```bash
   git clone https://github.com/MiHaTsKiYi13/MiHa-Browser.git
   ```

3. **Распространённые ошибки и их решения:**
   - **Git не найден:**  
     Убедитесь, что Git установлен, и проверьте версию командой `git --version`.
   - **Проблемы с доступом:**  
     Если получаете ошибку:
     ```
     fatal: repository 'https://github.com/MiHaTsKiYi13/MiHa-Browser.git/' not found
     ```
     Проверьте правильность URL и наличие прав доступа (репозиторий может быть приватным).
   - **Сетевые ошибки:**  
     Убедитесь, что у вас стабильное интернет-соединение и что файрвол или антивирус не блокирует соединение.

---

### Установка Git (если необходимо)

#### Windows

1. Перейдите на [официальный сайт Git для Windows](https://git-scm.com/download/win) и скачайте установочный файл.
2. Запустите установщик и следуйте инструкциям.
3. После установки проверьте версию:
   ```bash
   git --version
   ```

#### macOS

1. Перейдите на [официальный сайт Git для macOS](https://git-scm.com/download/mac) или установите Git через Homebrew:
   ```bash
   brew install git
   ```
2. Проверьте установку:
   ```bash
   git --version
   ```

#### Linux (Ubuntu/Debian)

1. Откройте терминал.
2. Выполните:
   ```bash
   sudo apt-get update
   sudo apt-get install git
   ```
3. Проверьте установку:
   ```bash
   git --version
   ```
```
