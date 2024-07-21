document.addEventListener("DOMContentLoaded", function () {
    var changeCssButton = document.getElementById("changeCssButton");
    var icon = document.getElementById("icon");
    var bodyElement = document.querySelector('body');
    var chatElement = document.querySelector('.card');
    var sidenavElement = document.querySelector('.sidenav');
    var faqs = document.querySelector('.faq-section');
    var graphPlotterButton = document.querySelector('a[href="/graphs"]');
    var chatBotButton = document.querySelector('a[href="/"]');
    var aboutusbutton = document.querySelector('a[href="/about"]');
    var modal = document.querySelector('.modal-content');
    var faqItems = document.querySelectorAll('.list-group-item');
    var msgtimesend = document.querySelectorAll('.msg_time_send');
    var msgtime = document.querySelectorAll('.msg_time');
    var showtableModal = document.querySelector('.showtableModal');
    var rectanglebox = document.querySelector('.rectangle-box');
    var img1 = document.querySelector('.img1');
    var img2 = document.querySelector('.img2');
    var img3 = document.querySelector('.img3');
    var captions = document.querySelectorAll('.caption'); // Select all caption elements
    // Function to apply dark mode
    function enableDarkMode() {
        bodyElement.style.backgroundColor = "#070F2B";
        bodyElement.style.color = "#f7f8fc";
        if (showtableModal) showtableModal.style.backgroundColor = "#070F2B";
        if (modal) modal.style.backgroundColor = "#070F2B";
        if (chatElement) chatElement.style.backgroundColor = "#070F2B";
        if (chatElement) chatElement.style.color = "#f7f8fc";
        if (rectanglebox) rectanglebox.style.backgroundColor = "#ffffff";
        if (sidenavElement) sidenavElement.style.backgroundColor = "#070F2B";
        if (sidenavElement) sidenavElement.style.color = "white";
        if (faqs) faqs.style.backgroundColor = "#535C91";
        changeCssButton.style.color = "white";
        if (graphPlotterButton) graphPlotterButton.style.color = "#FF9EAA";
        if (aboutusbutton) aboutusbutton.style.color = "#FF9EAA";
        if (chatBotButton) chatBotButton.style.color = "#FF9EAA";
        if (img1) img1.style.backgroundColor = "#070F2B";
        if (img2) img2.style.backgroundColor = "#070F2B";
        if (img3) img3.style.backgroundColor = "#070F2B";
        captions.forEach(function (caption) {
            caption.style.color = "#ffffff"; // Change caption color to white
        });
        msgtimesend.forEach(function (element) {
            element.style.color = "#FFFFFF";
        });
        msgtime.forEach(function (element) {
            element.style.color = "#FFFFFF";
        });
        faqItems.forEach(function (item) {
            item.style.backgroundColor = "#292B4A";
            item.style.color = "white";
        });
        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");
        localStorage.setItem('darkMode', 'enabled');
    }

    // Function to disable dark mode
    function disableDarkMode() {
        bodyElement.style.backgroundColor = "";
        bodyElement.style.color = "";
        if (showtableModal) showtableModal.style.backgroundColor = "";
        if (modal) modal.style.backgroundColor = "";
        if (chatElement) chatElement.style.backgroundColor = "";
        if (chatElement) chatElement.style.color = "";
        if (rectanglebox) rectanglebox.style.backgroundColor = "";
        if (sidenavElement) sidenavElement.style.backgroundColor = "";
        if (sidenavElement) sidenavElement.style.color = "";
        if (faqs) faqs.style.backgroundColor = "";
        changeCssButton.style.color = "black";
        if (graphPlotterButton) graphPlotterButton.style.color = "";
        if (aboutusbutton) aboutusbutton.style.color = "";
        if (chatBotButton) chatBotButton.style.color = "";
        if (img1) img1.style.backgroundColor = "";
        if (img2) img2.style.backgroundColor = "";
        if (img3) img3.style.backgroundColor = "";
        captions.forEach(function (caption) {
            caption.style.color = "rgb(212, 13, 113)"; // Reset caption color
        });

        msgtimesend.forEach(function (element) {
            element.style.color = "#000000";
        });
        msgtime.forEach(function (element) {
            element.style.color = "#000000";
        });
        faqItems.forEach(function (item) {
            item.style.backgroundColor = "";
            item.style.color = "";
        });
        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");
        localStorage.setItem('darkMode', 'disabled');
    }

    // Check the stored value in localStorage
    if (localStorage.getItem('darkMode') === 'enabled') {
        enableDarkMode();
    } else {
        disableDarkMode();
    }

    if (changeCssButton) {
        changeCssButton.addEventListener("click", function () {
            if (localStorage.getItem('darkMode') !== 'enabled') {
                enableDarkMode();
            } else {
                disableDarkMode();
            }
        });
    }
});