var style = document.createElement('style');
style.textContent = '.navbar-brand:hover::first-letter { color: #000 !important; }';
document.head.appendChild(style);

function loadNavbar() {
  var path = window.location.pathname;
  var links = [
    { href: "/", label: "Home" },
    { href: "/projects.html", label: "Projects" },
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

document.addEventListener("DOMContentLoaded", loadNavbar);
