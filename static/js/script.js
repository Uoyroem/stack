
document.addEventListener('DOMContentLoaded', () => {
  const menuButton = document.querySelector('.button.button--large.navigation__menu-button');
  const menuOpenIcon = document.querySelector('#catalog-menu-open-button-icon');
  const menuCloseIcon = document.querySelector('#catalog-menu-close-button-icon');
  const menuActiveCheckbox = document.querySelector('#catalog-active-checkbox');
  menuOpenIcon.style.display = 'inline';
  menuCloseIcon.style.display = 'none';
  menuButton.addEventListener('', () => {
    if (!menuActiveCheckbox.checked) {
      menuOpenIcon.style.display = 'none';
      menuCloseIcon.style.display = 'inline';
    } else {
      menuOpenIcon.style.display = 'inline';
      menuCloseIcon.style.display = 'none';
    }
  });
});