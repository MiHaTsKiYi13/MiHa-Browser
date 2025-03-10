<div align="center">
  <h1>MiHa Browser</h1>
  <p>Простой, современный и экспериментальный браузер на Python с использованием <strong>PyQt6 WebEngine</strong></p>
</div>

<div align="center">
  <h2>Наши логотипы</h2>
  <img src="https://github.com/user-attachments/assets/157e5338-114e-4f35-b72d-90637e0d60a5" alt="Логотип 1" width="150" style="margin: 0 20px;">
  <img src="https://github.com/user-attachments/assets/e1067a16-0b44-435c-a53d-ccfe4917a79d" alt="Логотип 2" width="150" style="margin: 0 20px;">
</div>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/MiHaTsKiYi13/MiHa-Browser.svg?style=social)](https://github.com/MiHaTsKiYi13/MiHa-Browser/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/MiHaTsKiYi13/MiHa-Browser.svg?style=social)](https://github.com/MiHaTsKiYi13/MiHa-Browser/network)

---

## Оглавление

- [Описание](#описание)
- [Особенности](#особенности)
- [Скриншоты и демо](#скриншоты-и-демо)
- [Установка и запуск](#установка-и-запуск)
- [Настройка и расширения](#настройка-и-расширения)
- [Git: клонирование и устранение ошибок](#git-клонирование-и-устранение-ошибок)
- [Планы развития и Roadmap](#планы-развития-и-roadmap)
- [Лицензия](#лицензия)
- [Контакты и сообщество](#контакты-и-сообщество)

---

## Описание

**MiHa Browser** — экспериментальный браузер, разработанный на Python с использованием [PyQt6 WebEngine](https://pypi.org/project/PyQt6-WebEngine/). Проект создан для тех, кто ценит минимализм, удобство и гибкость настройки. Браузер сочетает в себе простоту использования и современные возможности, позволяющие адаптировать его под индивидуальные потребности.

Основные возможности:
- **Многовкладочный режим** для комфортного серфинга.
- **Приватный режим** — просмотр без сохранения истории, куки и кеша.
- Встроенные инструменты: **AdBlock** и **Dark Reader**.
- Поддержка пользовательских JavaScript-расширений.
- Менеджер загрузок, история посещений, закладки и удобное управление данными.

---

## Особенности

- **Многовкладочный режим:**  
  Управление несколькими вкладками в одном окне для удобства работы.

- **Приватный режим:**  
  Максимальная конфиденциальность — не сохраняется история просмотров, куки и кеш.

- **Встроенные инструменты:**  
  AdBlock для блокировки рекламы и Dark Reader для комфортного перехода на тёмную тему.

- **Расширяемость:**  
  Лёгкая интеграция пользовательских JavaScript-скриптов для дополнительного функционала.

- **Менеджер загрузок:**  
  Отслеживание статуса загрузок с возможностью приостановки или отмены.

- **Удобные настройки:**  
  Выбор поисковой системы (Google, Yandex, Bing, DuckDuckGo), языка интерфейса, шрифта и пути сохранения загрузок.

- **Управление данными:**  
  Быстрая очистка куки, кеша и других временных файлов для оптимальной работы.

---

## Скриншоты и демо

<div align="center">
  <h2>Превью интерфейса</h2>
  <img src="https://github.com/user-attachments/assets/7bd10a7a-202c-44a6-9aa8-b1b1aff65075" alt="Скриншот 1" width="200">
  <img src="https://github.com/user-attachments/assets/78238618-cad3-47ac-9044-da254d39a3fa" alt="Скриншот 2" width="200">
  <img src="https://github.com/user-attachments/assets/8d15212e-79fb-4e68-ad27-7cc9064fc1aa" alt="Скриншот 3" width="200">
  <img src="https://github.com/user-attachments/assets/4569f0ea-8648-4667-a25e-b3f1b82c058d" alt="Скриншот 4" width="200">
</div>

---

## Установка и запуск

### Требования
- **Python 3.9+** (рекомендуется Python 3.10+)
- **PyQt6** и **PyQt6-WebEngine**

### Установка зависимостей

1. (Опционально) Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate   # для Linux/macOS
   venv\Scripts\activate      # для Windows
   ```
2. Установите необходимые пакеты:
   ```bash
   pip install PyQt6 PyQt6-WebEngine
   ```

### Загрузка проекта

Клонируйте репозиторий:
```bash
git clone https://github.com/MiHaTsKiYi13/MiHa-Browser.git
```

### Запуск браузера

Перейдите в папку проекта и выполните:
```bash
python main.py
```
Для Windows можно запустить двойным кликом по файлу `main.pyw`.

---

## Настройка и расширения

**MiHa Browser** предоставляет удобный интерфейс для персонализации:
- **Настройки браузера:**  
  Измените поисковую систему, домашнюю страницу, язык, шрифт и путь загрузок.
  
- **Менеджер расширений:**  
  Лёгкое добавление, удаление и включение/отключение пользовательских JavaScript-скриптов. По умолчанию установлены AdBlock (MiBlock) и Dark Reader.
  
- **Очистка данных:**  
  Быстрая очистка куки, кеша и временных файлов для оптимизации работы.

---

## Git: клонирование и устранение ошибок

1. **Проверка установки Git:**  
   В терминале выполните:
   ```bash
   git --version
   ```
2. **Клонирование репозитория:**  
   Выполните:
   ```bash
   git clone https://github.com/MiHaTsKiYi13/MiHa-Browser.git
   ```
3. **Устранение распространённых ошибок:**
   - **Git не найден:**  
     Убедитесь, что Git установлен и правильно добавлен в PATH.
   - **Проблемы с доступом:**  
     Проверьте правильность URL репозитория и наличие публичного доступа.
   - **Сетевые ошибки:**  
     Проверьте стабильность интернет-соединения и настройки файрвола/антивируса.

---

## Планы развития и Roadmap

- **Новый дизайн интерфейса:**  
  Улучшение анимаций, добавление новых тем и визуальных эффектов.

- **Расширения:**  
  Интеграция дополнительных пользовательских скриптов с автоматической синхронизацией (например, с [Greasy Fork](https://greasyfork.org/)).

- **Обратная связь:**  
  Реализация системы отзывов для быстрого реагирования на пожелания пользователей.

- **Оптимизация:**  
  Повышение производительности и стабильности работы на разных платформах.

---

## Контакты и сообщество

- **GitHub:** [MiHa-Browser](https://github.com/MiHaTsKiYi13/MiHa-Browser)
- **Telegram/Discord:** [MiHaTsKiYi](https://t.me/mihatskiyi)

Присоединяйтесь к нашему сообществу, чтобы следить за обновлениями, обсуждать идеи и делиться опытом!
- **Telegram:** [DE3NAKE](https://t.me/DE3NAKE)
