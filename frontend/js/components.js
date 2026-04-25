function loadNavbar() {
  var path = window.location.pathname;
  var links = [
    { href: "/", label: "Home" },
    { href: "/projects.html", label: "Projects" },
    { href: "/gym.html", label: "Gym" },
    { href: "/food.html", label: "Food" },
    { href: "/guestbook.html", label: "Guest Book" },
  ];

  var items = links.map(function (link) {
    var active = path === link.href || (link.href !== "/" && path.startsWith(link.href));
    return '<li' + (active ? ' class="active"' : '') + '><a href="' + link.href + '">' + link.label + '</a></li>';
  }).join("\n");

  document.getElementById("navbar").innerHTML =
    '<div class="container">' +
      '<div class="navbar-header">' +
        '<a class="navbar-brand" href="/">Tommy Elvebu</a>' +
      '</div>' +
      '<ul class="nav navbar-nav">' +
        items +
      '</ul>' +
    '</div>';
}

function loadFooter() {
  var footer = document.createElement('footer');
  footer.className = 'site-footer';
  footer.innerHTML =
    '<div class="container text-center">' +
      '<a href="https://github.com/tommyelvebu" target="_blank">GitHub</a>' +
      '<a href="https://www.linkedin.com/in/tommy-elvebu-a43108254/" target="_blank">LinkedIn</a>' +
      '<a href="mailto:tommy.elvebu@pm.me">Email</a>' +
    '</div>';
  document.body.appendChild(footer);
}

document.addEventListener("DOMContentLoaded", function() {
  loadNavbar();
  loadFooter();
});
