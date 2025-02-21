console.log("%cYOUTUBE!", "background: (red)); color: white; font-size: 18px; font-weight: bold; padding: 5px;");
(function () {
  function removeYouTubeLogo() {
      let logoContainer = document.querySelector("#logo"); // Контейнер логотипа
      let logoIcon = document.querySelector("#logo-icon"); // Сам логотип

      if (logoContainer) logoContainer.remove(); // Удаляем контейнер
      if (logoIcon) logoIcon.remove(); // Удаляем сам логотип
  }

  document.addEventListener("DOMContentLoaded", removeYouTubeLogo);
  setTimeout(removeYouTubeLogo, 2000); // Повторная попытка через 2 сек (на случай задержки)
})();
