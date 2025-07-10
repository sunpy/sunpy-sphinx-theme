document.addEventListener("DOMContentLoaded", function () {
  // Handle concertina toggle clicks inside dropdown
  document.querySelectorAll(".concertina-toggle").forEach(function (toggle) {
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();

      const submenuId = toggle.getAttribute("aria-controls");
      const submenu = document.getElementById(submenuId);
      if (!submenu) return;
      submenu.classList.add("collapse"); // Remove bootstraps control to ensure we can toggle
      const expanded = submenu.classList.contains("show");
      submenu.classList.toggle("show", !expanded);
      submenu.classList.toggle("collapse", !expanded);
      toggle.setAttribute("aria-expanded", String(!expanded));
    });
  });

  // Prevent dropdown from closing when clicking inside the concertina
  document.querySelectorAll(".dropdown-menu").forEach(function (menu) {
    menu.addEventListener("click", function (e) {
      if (
        e.target.closest(".concertina-toggle") ||
        e.target.closest(".concertina-submenu")
      ) {
        e.stopPropagation();
      }
    });
  });

  // Reset all concertinas when dropdown is hidden
  document.querySelectorAll(".dropdown").forEach(function (dropdown) {
    dropdown.addEventListener("hide.bs.dropdown", function () {
      dropdown
        .querySelectorAll(".concertina-submenu.show")
        .forEach(function (submenu) {
          submenu.classList.remove("show");
        });
      dropdown
        .querySelectorAll(".concertina-toggle")
        .forEach(function (toggle) {
          toggle.setAttribute("aria-expanded", "false");
        });
    });
  });
});
