document.addEventListener("DOMContentLoaded", function () {
  // Setup toggle for nested submenus
  const triggers = document.querySelectorAll(".dropdown-submenu > .dropdown-toggle");

  triggers.forEach(function (trigger, i) {
    trigger.dataset.bound = "true";
    trigger.addEventListener("click", function (e) {
      if (trigger.dataset.processing === "true") return;

      trigger.dataset.processing = "true";
      setTimeout(() => delete trigger.dataset.processing, 100);

      e.preventDefault();
      e.stopPropagation();

      const submenu = trigger.nextElementSibling;

      // Close other submenus at this level
      const parent = trigger.closest(".dropdown-menu");
      if (parent) {
        parent.querySelectorAll(".dropdown-menu.show").forEach(function (open) {
          if (open !== submenu) {
            open.classList.remove("show");
          }
        });
      }

      submenu.classList.toggle("show");
    });
  });

  // Close all open submenus when a top-level dropdown is closed
  document.querySelectorAll('.dropdown').forEach(function (dropdown) {
    dropdown.addEventListener('hide.bs.dropdown', function () {
      dropdown.querySelectorAll('.dropdown-menu.show').forEach(function (submenu) {
        submenu.classList.remove('show');
      });
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll('.dropdown-menu.show').forEach(function (submenu) {
        submenu.classList.remove('show');
      });
    }
  });
});
