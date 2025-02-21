console.log("%cYOUTUBE!", "background: (red)); color: white; font-size: 18px; font-weight: bold; padding: 5px;");
(function () {
  function removeYouTubeLogo() {
      let logo = document.querySelector("#logo-icon"); // Ищем логотип YouTube
      if (logo) logo.remove(); // Удаляем его
  }

  document.addEventListener("DOMContentLoaded", removeYouTubeLogo);
  setTimeout(removeYouTubeLogo, 2000); // Повторная попытка
})();
