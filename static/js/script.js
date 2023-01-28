
document.addEventListener('DOMContentLoaded', () => {
  const iconChangeButtons = document.querySelectorAll('button[data-menu-icon-change]');
  const menuOpenIcon = document.querySelector('#catalog-menu-open-button-icon');
  const menuCloseIcon = document.querySelector('#catalog-menu-close-button-icon');
  const menuActiveCheckbox = document.querySelector('#catalog-active-checkbox');
  menuOpenIcon.style.display = 'inline';
  menuCloseIcon.style.display = 'none';

  const updateIcon = () => {
    if (!menuActiveCheckbox.checked) {
      menuOpenIcon.style.display = 'none';
      menuCloseIcon.style.display = 'inline';
    } else {
      menuOpenIcon.style.display = 'inline';
      menuCloseIcon.style.display = 'none';
    }
  };

  iconChangeButtons.forEach(button => button.addEventListener('click', updateIcon));
});