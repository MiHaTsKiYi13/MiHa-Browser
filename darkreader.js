// darkreader.js - упрощённая логика "тёмного" режима

(function() {
    // 1) Скажем браузеру, что мы предпочитаем "dark" (для сайтов, у которых есть dark-theme)
    let meta = document.createElement('meta');
    meta.name = 'color-scheme';
    meta.content = 'dark';
    document.head.appendChild(meta);

    // 2) Пытаемся выставить prefers-color-scheme: dark через CSS
    let style = document.createElement('style');
    style.textContent = `
        @media (prefers-color-scheme: light) {
          :root {
            color-scheme: dark;
          }
        }
        /* Примитивная инверсия для "светлых" сайтов */
        html, body {
          background-color: #000 !important;
          color: #ccc !important;
          filter: invert(0.9) hue-rotate(180deg);
        }
        img, video, iframe, canvas {
          filter: invert(0.9) hue-rotate(180deg);
        }
    `;
    document.head.appendChild(style);
})();
