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
- [Git: Клонирование репозитория и устранение ошибок](#git-клонирование-репозитория-и-устранение-ошибок)
- [Планы развития и Roadmap](#планы-развития-и-roadmap)
- [Лицензия](#лицензия)
- [Контакты и сообщество](#контакты-и-сообщество)

---

## Описание

**MiHa Browser** – экспериментальный браузер на Python, созданный с использованием [PyQt6 WebEngine](https://pypi.org/project/PyQt6-WebEngine/). Проект предназначен для пользователей, ценящих простоту, функциональность и возможность адаптировать браузер под свои нужды. Среди основных возможностей:

- **Многовкладочный режим** и **приватный режим** для безопасного просмотра
- Встроенный **AdBlock** и поддержка **тёмного режима** (Dark Reader)
- Поддержка пользовательских расширений (JavaScript-скриптов)
- Менеджер загрузок, история посещений, закладки и удобное управление данными (куки, кеш)
- Гибкая настройка поисковой системы (Google, Yandex, Bing, DuckDuckGo), языка, шрифта и домашней страницы

Ключевые слова: **Браузер на Python**, **PyQt6**, **GitHub проект**, **экспериментальный браузер**, **расширения для браузера**.

---

## Особенности

- **Многовкладочный режим:** Открытие и удобное управление несколькими сайтами в одном окне.
- **Приватный режим:** Полная конфиденциальность — не сохраняется история, куки и кеш.
- **AdBlock и Dark Reader:** Встроенные решения для блокировки рекламы и переключения на тёмную тему.
- **Расширения:** Лёгкое добавление и управление пользовательскими JavaScript-скриптами для расширения функционала.
- **Менеджер загрузок:** Отслеживание прогресса загрузок с возможностью приостановки и отмены.
- **История и закладки:** Удобное сохранение посещённых сайтов с функцией быстрого доступа.
- **Гибкие настройки:** Возможность выбрать поисковую систему, язык интерфейса, шрифт и путь загрузок.
- **Управление данными:** Очистка куки, кеша и других данных для оптимизации работы браузера.

---

## Скриншоты и демо

<div align="center">
  <h2>Превью интерфейса</h2>
  <img src="https://github.com/user-attachments/assets/7bd10a7a-202c-44a6-9aa8-b1b1aff65075" alt="Скриншот 1" width="200">
  <img src="https://github.com/user-attachments/assets/78238618-cad3-47ac-9044-da254d39a3fa" alt="Скриншот 2" width="200">
  <img src="https://github.com/user-attachments/assets/8d15212e-79fb-4e68-ad27-7cc9064fc1aa" alt="Скриншот 3" width="200">
  <img src="https://github.com/user-attachments/assets/4569f0ea-8648-4667-a25e-b3f1b82c058d" alt="Скриншот 4" width="200">
</div>

> **Демо:** Ознакомьтесь с коротким видео работы MiHa Browser на [YouTube](https://www.youtube.com/) или запустите интерактивное демо через GitHub Pages (ссылка в разделе Контакты).

---

## Установка и запуск

### Требования
- Python 3.9 или выше (рекомендуется Python 3.10+)
- PyQt6 и PyQt6-WebEngine

### Установка зависимостей
Откройте терминал и выполните:
```bash
pip install PyQt6 PyQt6-WebEngine
```

### Загрузка проекта
Склонируйте репозиторий:
```bash
git clone https://github.com/MiHaTsKiYi13/MiHa-Browser.git
```

### Запуск браузера
Перейдите в папку проекта и выполните:
```bash
python main.py
```
Или, для Windows, дважды кликните по файлу `main.pyw`.

---

## Настройка и расширения

**MiHa Browser** предоставляет удобный интерфейс для настройки и управления расширениями:
- **Настройки браузера:** Изменение поисковой системы, домашней страницы, языка, шрифта и режима загрузок.
- **Менеджер расширений:** Добавление, удаление и включение/отключение пользовательских JavaScript-скриптов. По умолчанию установлены AdBlock (MiBlock) и Dark Reader.
- **Управление данными:** Очистка куки, кеша и данных сайтов для повышения производительности.

Эта гибкость позволяет репозиторию занимать лидирующие позиции по запросам «Браузер на Python GitHub», улучшая его видимость в поиске.

---

## Git: Клонирование репозитория и устранение ошибок

1. **Проверка установки Git:**  
   Откройте терминал и выполните:
   ```bash
   git --version
   ```
2. **Клонирование репозитория:**  
   Выполните:
   ```bash
   git clone https://github.com/MiHaTsKiYi13/MiHa-Browser.git
   ```
3. **Распространённые ошибки:**  
   - **Git не найден:** Проверьте установку Git с помощью команды `git --version`.
   - **Проблемы с доступом:** Убедитесь, что URL репозитория указан правильно и репозиторий открыт для публичного доступа.
   - **Сетевые ошибки:** Проверьте стабильность интернет-соединения и настройки файрвола/антивируса.

---

## Планы развития и Roadmap

- **Новые возможности интерфейса:** Улучшение анимаций и добавление новых тем оформления.
- **Расширения:** Подключение дополнительных пользовательских скриптов с автоматической синхронизацией с Greasy Fork.
- **Обратная связь:** Интеграция системы отзывов для улучшения функционала.
- **Мобильная версия:** Исследование вариантов адаптации интерфейса для сенсорных устройств.

---

## Лицензия

Проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

---

## Контакты и сообщество

- **GitHub:** [MiHa-Browser](https://github.com/MiHaTsKiYi13/MiHa-Browser)
- **Telegram/Discord:** [MiHaTsKiYi](https://t.me/mihatskiyi)
