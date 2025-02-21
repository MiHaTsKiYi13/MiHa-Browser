document.addEventListener("DOMContentLoaded", function() {
  // === Функционал для выпадающего меню ===
  const menuIcon = document.getElementById('menu-icon');
  const dropdownMenu = document.getElementById('dropdown-menu');

  menuIcon.addEventListener('click', function() {
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
  });

  // === Функция для поиска или перехода по URL ===
  function searchQuery() {
    const query = document.getElementById('search').value.trim();
    if (query !== "") {
      // Регулярное выражение для проверки, начинается ли строка с http://, https:// или file://
      const urlPattern = /^(https?:\/\/|file:\/\/)/;

      // Если начинается с file://, заменяем на https://
      if (query.startsWith("file://")) {
        const newURL = query.replace("file://", "https://");
        window.location.href = newURL;
        return;
      }

      // Если строка не начинается с http:// или https://, добавляем https://
      if (!urlPattern.test(query)) {
        // Проверяем, содержит ли запрос точку, как в домене (например, example.com)
        const domainPattern = /\.[a-z]{2,}$/i;
        if (domainPattern.test(query)) {
          // Добавляем https://, если это похоже на домен
          window.location.href = "https://" + query;
        } else {
          // Выполняем поиск в DuckDuckGo, если это не домен
          window.location.href = "https://duckduckgo.com/?q=" + encodeURIComponent(query);
        }
      } else {
        // Если уже есть http:// или https://, переходим по адресу
        window.location.href = query;
      }
    }
  }

  // Обработчик нажатия Enter
  document.getElementById('search').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      searchQuery();
    }
  });

  // Обработчик клика по кнопке поиска
  document.getElementById('search-button').addEventListener('click', searchQuery);

  // === Фоновая анимация Python-команд ===
  const commands = [
    "print('Hello, World!')",
    "for i in range(10):",
    "if __name__ == '__main__':",
    "def my_function():",
    "import this",
    "lambda x: x * 2",
    "list_comp = [x for x in range(5)]",
    "with open('file.txt', 'r') as f:",
    "try:",
    "except Exception as e:",
    "import sys",
    "class MyClass:",
    "import os",
    "while True:",
    "elif x > 0:",
    "raise ValueError('Invalid value')",
    "import random",
    "my_list = [1, 2, 3]",
    "print(len(my_list))",
    "my_dict = {'a': 1, 'b': 2}",
    "sorted_list = sorted(my_list)",
    "def add(a, b): return a + b",
    "import math",
    "print(math.pi)",
    "for index, value in enumerate(my_list):",
    "my_set = set([1, 2, 2, 3])",
    "def decorator(func):",
    "class AnotherClass(MyClass):",
    "from datetime import datetime"
  ];

  const background = document.getElementById('background');

  commands.forEach(cmd => {
    const codeElement = document.createElement("div");
    codeElement.className = "python-code";
    codeElement.innerText = cmd;

    let randomTop;
    do {
      randomTop = Math.random() * 100;
    } while (randomTop > 40 && randomTop < 60); // Запрещаем спавн в центре

    codeElement.style.top = randomTop + "%";
    codeElement.style.left = Math.random() * 90 + "%";
    codeElement.style.animationDelay = Math.random() * 5 + 's';
    codeElement.style.animation = "floatUp 10s linear infinite";

    background.appendChild(codeElement);
  });
});
