document.addEventListener("DOMContentLoaded", function() {
  // === Функционал для выпадающего меню ===
  const menuIcon = document.getElementById('menu-icon');
  const dropdownMenu = document.getElementById('dropdown-menu');

  menuIcon.addEventListener('click', function() {
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
  });

  // === Функционал для выбора поисковой системы ===
  const searchEngineDropdown = document.getElementById('search-engine-dropdown');
  const selectedEngine = document.getElementById('selected-engine');
  const dropdownOptions = document.getElementById('dropdown-options');

  // Открытие/закрытие списка поисковых систем
  selectedEngine.addEventListener('click', function() {
    dropdownOptions.style.display = dropdownOptions.style.display === 'block' ? 'none' : 'block';
  });

  // Выбор поисковой системы
  dropdownOptions.querySelectorAll('.option').forEach(option => {
    option.addEventListener('click', function() {
      const selectedImg = this.querySelector('img').src;
      const selectedText = this.querySelector('span').innerText;
      const selectedURL = this.dataset.url;

      selectedEngine.querySelector('img').src = selectedImg;
      selectedEngine.querySelector('span').innerText = selectedText;
      selectedEngine.dataset.url = selectedURL;

      dropdownOptions.style.display = 'none'; // Закрываем список после выбора
    });
  });

  // === Функция для поиска ===
  function searchQuery() {
    const query = document.getElementById('search').value.trim();
    if (query !== "") {
      // Регулярное выражение для проверки, начинается ли строка с http:// или https://
      const urlPattern = /^(https?:\/\/)/;

      // Если строка не начинается с http:// или https://, добавляем https://
      let searchURL = query;

      if (!urlPattern.test(query)) {
        // Добавляем https://, если протокол не указан
        searchURL = "https://" + query;
      }

      // Пытаемся открыть сайт
      window.location.href = searchURL;
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

    background.appendChild(codeElement);
  });
});
