// ==UserScript==
// @name         Remove Adblock Thing + Global Ads Blocker
// @namespace    http://tampermonkey.net/
// @version      5.1
// @description  Удаляет блоки-реклама и скрывает рекламные элементы – на YouTube и на всех сайтах
// @author       JoelMatic / Модифицирован пользователем
// @match        *://*/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=youtube.com
// @updateURL    https://github.com/TheRealJoelmatic/RemoveAdblockThing/raw/main/Youtube-Ad-blocker-Reminder-Remover.user.js
// @downloadURL  https://github.com/TheRealJoelmatic/RemoveAdblockThing/raw/main/Youtube-Ad-blocker-Reminder-Remover.user.js
// @grant        none
// ==/UserScript==

(function() {
    //
    //      Config
    //

    // Включить механизм обхода антиадблока YouTube
    const adblocker = true;

    // Включить удаление popup-ок (без него не работает обход антиадблока)
    const removePopup = false;

    // Проверка обновлений (удаляет всплывающее окно)
    const updateCheck = true;

    // Вывод отладочных сообщений в консоль
    const debugMessages = true;

    // Включить модальное окно для обновлений
    const updateModal = {
        enable: true, // если true, используется SweetAlert2, иначе стандартный window.confirm
        timer: 5000, // время отображения модального окна
    };

    //
    //      Основной код
    //

    // Определяем, находимся ли мы на YouTube
    const isYouTube = window.location.hostname.includes("youtube.com");

    // Стартовое сообщение
    log("Script started");

    // Если мы на YouTube, запускаем оригинальные функции
    if (isYouTube) {
        if (adblocker) removeAds();
        if (removePopup) popupRemover();
        if (updateCheck) checkForUpdate();
    }

    // На всех сайтах (в том числе на YouTube) запускаем дополнительную блокировку реклам через CSS
    removeGlobalAds();

    //
    // Функции для YouTube (оставлены без изменений)
    //

    // Храним текущий URL
    let currentUrl = window.location.href;
    let isAdFound = false;
    let adLoop = 0;

    // Имитируем клик по элементам
    const event = new PointerEvent('click', {
        pointerId: 1,
        bubbles: true,
        cancelable: true,
        view: window,
        detail: 1,
        screenX: 0,
        screenY: 0,
        clientX: 0,
        clientY: 0,
        ctrlKey: false,
        altKey: false,
        shiftKey: false,
        metaKey: false,
        button: 0,
        buttons: 1,
        width: 1,
        height: 1,
        pressure: 0.5,
        tiltX: 0,
        tiltY: 0,
        pointerType: 'mouse',
        isPrimary: true
    });

    let hasIgnoredUpdate = false;

    // Удаление всплывающих окон (popup)
    function popupRemover() {
        setInterval(() => {
            const modalOverlay = document.querySelector("tp-yt-iron-overlay-backdrop");
            const popup = document.querySelector(".style-scope ytd-enforcement-message-view-model");
            const popupButton = document.getElementById("dismiss-button");
            const video = document.querySelector('video');

            document.body.style.setProperty('overflow-y', 'auto', 'important');

            if (modalOverlay) {
                modalOverlay.removeAttribute("opened");
                modalOverlay.remove();
            }

            if (popup) {
                log("Popup detected, removing...");

                if (popupButton) popupButton.click();
                popup.remove();

                if (video) {
                    video.play();
                    setTimeout(() => {
                        video.play();
                    }, 500);
                }

                log("Popup removed");
            }
            if (video && video.paused) {
                video.play();
            }

        }, 1000);
    }

    // Функция обхода рекламы в YouTube
    function removeAds() {
        log("removeAds()");

        var videoPlayback = 1;

        setInterval(() => {
            var video = document.querySelector('video');
            const ad = [...document.querySelectorAll('.ad-showing')][0];

            // Если изменился URL, удаляем рекламные блоки на странице
            if (window.location.href !== currentUrl) {
                currentUrl = window.location.href;
                removePageAds();
            }

            if (ad) {
                isAdFound = true;
                adLoop++;

                // Метод для центра рекламы
                const openAdCenterButton = document.querySelector('.ytp-ad-button-icon');
                openAdCenterButton?.dispatchEvent(event);
 
                const blockAdButton = document.querySelector('[label="Block ad"]');
                blockAdButton?.dispatchEvent(event);

                const blockAdButtonConfirm = document.querySelector('.Eddif [label="CONTINUE"] button');
                blockAdButtonConfirm?.dispatchEvent(event);

                const closeAdCenterButton = document.querySelector('.zBmRhe-Bz112c');
                closeAdCenterButton?.dispatchEvent(event);

                // Если появляется popup, скрываем его
                var popupContainer = document.querySelector('body > ytd-app > ytd-popup-container > tp-yt-paper-dialog');
                if (popupContainer && popupContainer.style.display === "") {
                    popupContainer.style.display = 'none';
                }

                log("Found Ad");

                // Поиск кнопок пропуска рекламы
                const skipButtons = ['ytp-ad-skip-button-container', 'ytp-ad-skip-button-modern', '.videoAdUiSkipButton', '.ytp-ad-skip-button', '.ytp-ad-skip-button-modern', '.ytp-ad-skip-button', '.ytp-ad-skip-button-slot' ];

                if (video) {
                    skipButtons.forEach(selector => {
                        const elements = document.querySelectorAll(selector);
                        if (elements && elements.length > 0) {
                            elements.forEach(element => {
                                element?.dispatchEvent(event);
                            });
                        }
                    });
                    video.play();
                    let randomNumber = Math.random() * (0.5 - 0.1) + 0.1;
                    video.currentTime = video.duration + randomNumber || 0;
                }

                log("skipped Ad (✔️)");
            } else {
                if (video && video.playbackRate === 10) {
                    video.playbackRate = videoPlayback;
                }
                if (isAdFound) {
                    isAdFound = false;
                    if (videoPlayback == 10) videoPlayback = 1;
                    if (video && isFinite(videoPlayback)) video.playbackRate = videoPlayback;
                    adLoop = 0;
                } else if (video) {
                    videoPlayback = video.playbackRate;
                }
            }
        }, 50);

        removePageAds();
    }

    // Удаление рекламных блоков на странице (не видеорекламы)
    function removePageAds() {
        const sponsor = document.querySelectorAll("div#player-ads.style-scope.ytd-watch-flexy, div#panels.style-scope.ytd-watch-flexy");
        const style = document.createElement('style');

        style.textContent = `
            ytd-action-companion-ad-renderer,
            ytd-display-ad-renderer,
            ytd-video-masthead-ad-advertiser-info-renderer,
            ytd-video-masthead-ad-primary-video-renderer,
            ytd-in-feed-ad-layout-renderer,
            ytd-ad-slot-renderer,
            yt-about-this-ad-renderer,
            yt-mealbar-promo-renderer,
            ytd-statement-banner-renderer,
            ytd-ad-slot-renderer,
            ytd-in-feed-ad-layout-renderer,
            ytd-banner-promo-renderer-background,
            statement-banner-style-type-compact,
            .ytd-video-masthead-ad-v3-renderer,
            div#root.style-scope.ytd-display-ad-renderer.yt-simple-endpoint,
            div#sparkles-container.style-scope.ytd-promoted-sparkles-web-renderer,
            div#main-container.style-scope.ytd-promoted-video-renderer,
            div#player-ads.style-scope.ytd-watch-flexy,
            ad-slot-renderer,
            ytm-promoted-sparkles-web-renderer,
            masthead-ad,
            tp-yt-iron-overlay-backdrop,
            #masthead-ad {
                display: none !important;
            }
        `;

        document.head.appendChild(style);

        sponsor?.forEach((element) => {
            if (element.getAttribute("id") === "rendering-content") {
                element.childNodes?.forEach((childElement) => {
                    if (childElement?.data.targetId && childElement?.data.targetId !== "engagement-panel-macro-markers-description-chapters") {
                        element.style.display = 'none';
                    }
                });
            }
        });

        log("Removed page ads (✔️)");
    }

    // Проверка обновлений скрипта
    function checkForUpdate(){
        if (window.top !== window.self && !(window.location.href.includes("youtube.com"))){
            return;
        }
        if (hasIgnoredUpdate){
            return;
        }
        const scriptUrl = 'https://raw.githubusercontent.com/TheRealJoelmatic/RemoveAdblockThing/main/Youtube-Ad-blocker-Reminder-Remover.user.js';
        fetch(scriptUrl)
        .then(response => response.text())
        .then(data => {
            const match = data.match(/@version\s+(\d+\.\d+)/);
            if (!match) {
                log("Unable to extract version from the GitHub script.", "e");
                return;
            }
            const githubVersion = parseFloat(match[1]);
            const currentVersion = parseFloat(GM_info.script.version);
            if (githubVersion <= currentVersion) {
                log('You have the latest version of the script. ' + githubVersion + " : " + currentVersion);
                return;
            }
            console.log('Remove Adblock Thing: A new version is available. Please update your script. ' + githubVersion + " : " + currentVersion);
            if (updateModal.enable) {
                if (parseFloat(localStorage.getItem('skipRemoveAdblockThingVersion')) === githubVersion) {
                    return;
                }
                const script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11';
                document.head.appendChild(script);
                const style = document.createElement('style');
                style.textContent = '.swal2-container { z-index: 2400; }';
                document.head.appendChild(style);
                script.onload = function () {
                    Swal.fire({
                        position: "top-end",
                        backdrop: false,
                        title: 'Remove Adblock Thing: New version is available.',
                        text: 'Do you want to update?',
                        showCancelButton: true,
                        showDenyButton: true,
                        confirmButtonText: 'Update',
                        denyButtonText: 'Skip',
                        cancelButtonText: 'Close',
                        timer: updateModal.timer ?? 5000,
                        timerProgressBar: true,
                        didOpen: (modal) => {
                            modal.onmouseenter = Swal.stopTimer;
                            modal.onmouseleave = Swal.resumeTimer;
                        }
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.replace(scriptUrl);
                        } else if (result.isDenied) {
                            localStorage.setItem('skipRemoveAdblockThingVersion', githubVersion);
                        }
                    });
                };
                script.onerror = function () {
                    var result = window.confirm("Remove Adblock Thing: A new version is available. Please update your script.");
                    if (result) {
                        window.location.replace(scriptUrl);
                    }
                }
            } else {
                var result = window.confirm("Remove Adblock Thing: A new version is available. Please update your script.");
                if (result) {
                    window.location.replace(scriptUrl);
                }
            }
        })
        .catch(error => {
            hasIgnoredUpdate = true;
            log("Error checking for updates:", "e", error);
        });
        hasIgnoredUpdate = true;
    }

    // Вывод отладочных сообщений в консоль
    function log(message, level = 'l', ...args) {
        if (!debugMessages) return;
        const prefix = 'Remove Adblock Thing:';
        const fullMessage = `${prefix} ${message}`;
        switch (level) {
            case 'e':
            case 'err':
            case 'error':
                console.error(fullMessage, ...args);
                break;
            case 'l':
            case 'log':
                console.log(fullMessage, ...args);
                break;
            case 'w':
            case 'warn':
            case 'warning':
                console.warn(fullMessage, ...args);
                break;
            case 'i':
            case 'info':
            default:
                console.info(fullMessage, ...args);
                break;
        }
    }

    //
    // Функция для глобальной блокировки реклам (работает на всех сайтах)
    //
    function removeGlobalAds() {
        const adCss = `
            /* Общие селекторы для рекламы */
            [id*="ad-"],
            [class*="ad-"],
            [class*="ads-"],
            [class*="advert"],
            iframe[src*="ad"],
            .ad,
            .ads,
            .advertisement,
            .sponsor,
            .sponsored {
                display: none !important;
            }
        `;
        const style = document.createElement('style');
        style.textContent = adCss;
        document.head.appendChild(style);
        log("Global ad blockers CSS applied");
    }

})();
