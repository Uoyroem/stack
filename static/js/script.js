function makeMessage(text, pasteElement, delay = 5000) {
    const message = document.createElement('div');
    message.classList.add('message');
    
    message.textContent = text;

    pasteElement.appendChild(message);
    setTimeout(() => {
        pasteElement.removeChild(message);
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
                }
                const counter = document.getElementById(this.dataset.forCounter);
                const buttonIcon = this.querySelector('.bi');
                let counted = false;
                for (const toggle of this.dataset.toggle.split(',')) {
                    const [a, b] = toggle.split('<->').map(item => item.trim());
                    if (b) {
                        if (buttonIcon.classList.contains(b)) {
                            buttonIcon.classList.remove(b);
                            buttonIcon.classList.add(a);
                        } else {
                            buttonIcon.classList.remove(a);
                            buttonIcon.classList.add(b);
                        }
                        if (counter && !counted) {
                            let count = parseInt(counter.textContent);
                            counted = true;
                            count += buttonIcon.classList.contains(b) ? 1 : -1;
                            counter.textContent = count;
                            counter.style.display = !count ? 'none' : 'inline';
                        }
                        continue;
                    }
                    buttonIcon.classList.toggle(a);
                    if (counter && !counted) {
                        counted = true
                        counter.textContent = parseInt(counter.textContent) + buttonIcon.classList.contains(a) ? 1 : -1;
                    }
                }
            });
        });
    }
});

