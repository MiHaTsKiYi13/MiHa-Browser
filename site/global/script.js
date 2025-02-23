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

  // Объект сопоставления поисковых систем с их настройками
  const searchEngineMapping = {
    duckduckgo: { text: "DuckDuckGo", url: "https://duckduckgo.com/?q=", img: "assets/icons/duck.png" },
    bing: { text: "Bing", url: "https://www.bing.com/search?q=", img: "assets/icons/bing.png" },
    google: { text: "Google", url: "https://www.google.com/search?q=", img: "assets/icons/google.png" },
    yandex: { text: "Yandex", url: "https://www.yandex.ru/search/?text=", img: "assets/icons/yandex.png" }
  };

  // Загрузка настроек из settings.json
  fetch('assets/config/settings.json')
    .then(response => response.json())
    .then(settings => {
      const engine = settings.search_engine;
      if (searchEngineMapping[engine]) {
        const config = searchEngineMapping[engine];
        selectedEngine.querySelector('img').src = config.img;
        selectedEngine.querySelector('span').innerText = config.text;
        selectedEngine.dataset.url = config.url;
      } else {
        console.error("Неверное значение search_engine в настройках:", engine);
      }
    })
    .catch(err => console.error("Ошибка загрузки настроек:", err));

  // Открытие/закрытие списка поисковых систем
  selectedEngine.addEventListener('click', function() {
    dropdownOptions.style.display = dropdownOptions.style.display === 'block' ? 'none' : 'block';
  });

  // Выбор поисковой системы
  dropdownOptions.querySelectorAll('.option').forEach(option => {
    option.addEventListener('click', function() {
      const selectedImg = this.querySelector('img').src;
      const selectedText = this.querySelector('span').innerText;
      const selectedKey = this.dataset.engine;

      if (searchEngineMapping[selectedKey]) {
        selectedEngine.querySelector('img').src = selectedImg;
        selectedEngine.querySelector('span').innerText = selectedText;
        selectedEngine.dataset.url = searchEngineMapping[selectedKey].url;
      }

      dropdownOptions.style.display = 'none';
    });
  });

  // === Поиск ===
  window.searchQuery = function() {
    const query = document.getElementById('search').value.trim();
    if (query === "") return;

    const searchURL = selectedEngine.dataset.url + encodeURIComponent(query);
    window.location.href = searchURL;
  };

  document.getElementById('search').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') searchQuery();
  });

  document.getElementById('search-button').addEventListener('click', searchQuery);

  // === Фоновая анимация Python-команд ===
  const commands = [
    "print('Hello, World!')", "for i in range(10):", "if __name__ == '__main__':",
    "def my_function():", "import this", "lambda x: x * 2",
    "list_comp = [x for x in range(5)]", "with open('file.txt', 'r') as f:",
    "try:", "except Exception as e:", "import sys", "class MyClass:",
    "import os", "while True:", "elif x > 0:", "raise ValueError('Invalid value')",
    "import random", "my_list = [1, 2, 3]", "print(len(my_list))",
    "my_dict = {'a': 1, 'b': 2}", "sorted_list = sorted(my_list)",
    "def add(a, b): return a + b", "import math", "print(math.pi)",
    "for index, value in enumerate(my_list):", "my_set = set([1, 2, 2, 3])",
    "def decorator(func):", "class AnotherClass(MyClass):",
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
    } while (randomTop > 40 && randomTop < 60);

    codeElement.style.top = randomTop + "%";
    codeElement.style.left = Math.random() * 90 + "%";
    codeElement.style.animationDelay = Math.random() * 5 + 's';

    background.appendChild(codeElement);
  });
});
