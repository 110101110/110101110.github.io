const toggle = document.getElementById('menu-toggle');
const menu = document.getElementById('site-menu');
const background = document.querySelectorAll('header, main, footer');

function setMenu(open) {
  menu.hidden = !open;
  background.forEach(element => { element.inert = open; });
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
}

toggle.addEventListener('click', () => setMenu(menu.hidden));
menu.addEventListener('click', (event) => {
  if (event.target === menu || event.target.closest('a')) {
    setMenu(false);
  }
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && !menu.hidden) {
    setMenu(false);
    toggle.focus();
  }
});
