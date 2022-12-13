document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button[data-to]');
    for (const button of buttons) {
        button.addEventListener('click', function() {
            fetch(this.dataset.to).then(() => location.reload());
        });
    }
});

