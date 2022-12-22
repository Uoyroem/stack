function makeMessage(text, pasteElement, delay = 5000) {
    const message = document.createElement('div');
    message.classList.add('message');
    
    message.textContent = text;

    pasteElement.appendChild(message);
    setTimeout(() => {
        pasteElement.removeChild(message);
        location.reload();
    }, delay);
}

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button[data-to]');
    const messages = document.querySelector('.messages')
    for (const button of buttons) {
        button.addEventListener('click', function() {
            fetch(this.dataset.to).then(response => response.text()).then(message => {
                if (message) {
                    makeMessage(message, messages);
                } else {
                    location.reload();
                }
                
            });
        });
    }
});

