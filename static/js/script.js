async function onButtonClick() {
    to = this.dataset.to;
    const response = await fetch(to);
    const message = await response.text();
    location.reload();
}

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button[data-to]');
    if (!buttons) return;
    buttons.forEach(button => button.addEventListener('click', onButtonClick));
});

