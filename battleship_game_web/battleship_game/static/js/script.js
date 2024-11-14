document.addEventListener('DOMContentLoaded', function() {
    const popupOverlay = document.getElementById('popupOverlay');
    const popup = document.getElementById('popup');
    const closePopup = document.getElementById('closePopup');

    function openPopup() {
        popupOverlay.style.display = 'block';
    }

    function closePopupFunc() {
        popupOverlay.style.display = 'none';
    }

    openPopup();
    closePopup.addEventListener('click', closePopupFunc);
    popupOverlay.addEventListener('click', function(event) {
        if (event.target === popupOverlay) {
            closePopupFunc();
        }
    });
});