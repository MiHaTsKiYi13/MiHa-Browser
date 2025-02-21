# MiHa Browser

Простой и современный браузер на базе PyQt6 WebEngine с поддержкой:
- **Вкладок** и гибкой навигации.
- **Приватного режима** (отключает историю, куки, кэш).
- **AdBlock** для блокировки рекламы.
- **Dark Reader** (опциональная тёмная тема для сайтов).
- **Расширений** (JS-скрипты).
- **Управления загрузками** (прогресс, пауза/отмена).
- **Закладок** и журнала истории.
- **Выбора поисковой системы** (Google, Яндекс, Bing, DuckDuckGo).

## Скриншоты

<p align="center">
  <img src="![изображение](https://github.com/user-attachments/assets/c9bb0ddd-71b7-4852-8cce-68592ce79d0b)" alt="Главное окно" width="600"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/19a5063d-7ef2-46d6-97a3-866f9a40e3af" alt="Загрузки" width="600"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/d203faad-9411-422a-9db9-d33afda8e022" alt="Настройки" width="600"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/549ef7f9-b37e-4683-bca0-886c794dc996" alt="Журнал (История)" width="600"/>
</p>

## Установка

1. Убедитесь, что у вас установлен Python 3.9+ (рекомендуется 3.10 и выше).
2. Установите необходимые библиотеки:
   ```bash
   pip install PyQt6 PyQt6-WebEngine
   ```
3. Склонируйте (или скачайте) данный репозиторий в любую папку.
4. Убедитесь, что в папке есть файлы:
   - `main.pyw` (или `main.py`)
   - Папка `icons` (иконки)
   - Файлы `adblock.js`, `darkreader.js` (при необходимости)
   - Папка `configs` (автоматически создаётся для хранения настроек и истории)

## Запуск

Перейдите в каталог с браузером и выполните:

```bash
python main.pyw
```

> **Совет**: если вы хотите видеть сообщения об ошибках в консоли, переименуйте `main.pyw` в `main.py`.

После запуска откроется окно **MiHA Browser**.  
Если вы используете **Windows**, вы также можете запустить его двойным щелчком по файлу `main.pyw`.

## Основные возможности

- **Выбор поисковой системы** в обычном режиме: Google, Яндекс, Bing или DuckDuckGo.
- **Приватный режим**:
  - Не сохраняет историю и куки.
  - Автоматически использует DuckDuckGo для поиска.
- **Система вкладок**: открывайте несколько сайтов в одном окне.
- **Загрузки**:
  - Отображение прогресса.
  - Пауза/возобновление.
  - Настройка пути сохранения (спрашивать/по умолчанию/кастомный).
- **Закладки**: быстро добавляйте сайты в закладки и управляйте ими.
- **Журнал** (история посещений) — отключён в приватном режиме.
- **Расширения** (JS-скрипты): можно подключать пользовательские скрипты (адблок, тёмная тема и т.п.).
- **Удаление данных**: очистка куки и кэша из интерфейса.
- **Настройки**: выбор языка интерфейса (русский или английский), изменение шрифта, стартовой страницы, прочие параметры.

## Структура проекта

```bash
MiHa-Browser/
├── icons/                # Папка с иконками
├── configs/              # Автоматически создаётся при запуске (хранит json-файлы настроек, истории и т.д.)
├── adblock.js            # Скрипт блокировки рекламы
├── darkreader.js         # Скрипт тёмной темы (Dark Reader)
├── main.pyw (или main.py)# Основной файл приложения
└── README.md             # Этот файл
```

## Известные проблемы

- Отсутствует полноценный DevTools. При нажатии F12 выводится только сообщение.
- В Windows при запуске `.pyw` ошибки не отображаются в консоли (можно переименовать в `.py`).
- Папка `icons` должна находиться в одной директории с `main.pyw`, иначе некоторые иконки не загрузятся.

## Лицензия

Проект распространяется на условиях свободной лицензии по вашему выбору.  
Вы можете модифицировать, распространять и использовать этот код по своему усмотрению.

---

**MiHA Browser** — это небольшой экспериментальный проект, который можно использовать как основу для собственного браузера на базе PyQt6-WebEngine. Приятного пользования!
