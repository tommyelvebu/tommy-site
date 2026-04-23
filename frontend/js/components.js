var style = document.createElement('style');
style.textContent =
  '.navbar-brand:hover::first-letter { color: #000 !important; }' +
  '.nav.navbar-nav li a::first-letter { color: #7b2fbe; }' +
  '.btn-primary, .btn-primary:hover, .btn-primary:focus, .btn-primary:active { background-color: #7b2fbe !important; border-color: #7b2fbe !important; }' +
  '.btn::first-letter { color: inherit !important; }' +
  '.hero-image { width: 100%; height: 500px; object-fit: cover; object-position: center 65%; margin-bottom: 20px; }' +
  '.content-container { padding-top: 70px; }' +
  'html { height: 100%; }' +
  'body { min-height: 100%; display: flex; flex-direction: column; }' +
  '.content-container { flex: 1; }' +
  '.site-footer { background: #000084; color: #bbb; padding: 20px 0; border-top: 2px solid #bbb; }' +
  '.site-footer a { color: #7b2fbe; margin: 0 10px; text-decoration: none; }' +
  '.site-footer a:hover { color: #fff; }' +
  '#viewer-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 10000; background: rgba(0,0,0,0.5); }' +
  '#viewer { position: fixed; top: 40px; bottom: 40px; left: 10%; right: 10%; z-index: 10001; display: flex; border: 2px solid #bbb; }' +
  '#viewer-sidebar { width: 220px; min-width: 220px; background: #000084; color: #bbb; overflow-y: auto; padding: 10px 0; border-right: 2px solid #bbb; }' +
  '#viewer-sidebar .sidebar-title { padding: 8px 12px; font-weight: bold; color: #fff; border-bottom: 1px solid #555; margin-bottom: 5px; }' +
  '#viewer-sidebar a { display: block; padding: 6px 12px; color: #bbb; text-decoration: none; cursor: pointer; }' +
  '#viewer-sidebar a:hover, #viewer-sidebar a.active { background: #7b2fbe; color: #000; }' +
  '#viewer-close { position: fixed; top: 10px; right: 10px; z-index: 10002; background: #a00; color: #fff; border: 2px solid #bbb; padding: 2px 10px; font-size: 18px; cursor: pointer; }' +
  '#viewer-frame { flex: 1; border: none; background: #fff; }';
document.head.appendChild(style);

function loadNavbar() {
  var path = window.location.pathname;
  var links = [
    { href: "/", label: "Home" },
    { href: "/projects.html", label: "Projects" },
    { href: "/gym.html", label: "Gym" },
    { href: "/food.html", label: "Food" },
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
