var activeNavItem = $(".nav-item");

activeNavItem.click(function () {
  activeNavItem.removeClass("active");
  $(this).addClass("active");
});
