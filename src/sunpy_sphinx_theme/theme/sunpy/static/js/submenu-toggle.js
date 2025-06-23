
document.addEventListener("DOMContentLoaded", function () {
    const triggers = document.querySelectorAll('.dropdown-submenu > .dropdown-toggle');

    triggers.forEach(function (trigger, i) {
        // Prevent multiple listeners
        trigger.dataset.bound = "true";  
        trigger.addEventListener('click', function (e) {

        if (trigger.dataset.processing === "true") {
            // Defensive double-bind check to avoid multiple event listeners triggering
            return;
        }
        trigger.dataset.processing = "true";
        setTimeout(() => delete trigger.dataset.processing, 100);

        // stop bootstrap from using this click to close the parent dropdown
        e.preventDefault();
        e.stopPropagation();

        const submenu = trigger.nextElementSibling;
        // Close other submenus
        const parent = trigger.closest('.dropdown-menu');
        if (parent) {
            parent.querySelectorAll('.dropdown-menu.show').forEach(function (open) {
            if (open !== submenu) {
                open.classList.remove('show');
            }
            });
        }

        submenu.classList.toggle('show');
        });
    });
});
