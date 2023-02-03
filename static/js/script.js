/// <reference types="jquery"/>

const METHODS = {
  hideIf0(data, target, updater) {
    let count = parseInt(target.first().text());
    const icon = updater.find('.icon');
    // Если кнопка активна то у него есть icon--blue класс.
    if (icon.hasClass('icon--blue')) {
      icon.removeClass('icon--blue').addClass('icon--gray');
      target.text(--count);
      if (!count) {
        target.addClass('hidden');
      }
    } else {
      icon.removeClass('icon--gray').addClass('icon--blue');
      target.text(++count);
      target.removeClass('hidden');
    }
  },
  changeFavorite(data, target, updater) {
    this.hideIf0(data, target, updater);
    const updaterText = updater.find('.text');
    const icon = updater.find('.icon');
    if (icon.hasClass('icon--blue')) {
      updaterText.text('В избранном');
    } else {
      updaterText.text('В избранное');
    }
  },
  changeCompare(data, target, updater) {
    this.hideIf0(data, target, updater);
    const updaterText = updater.find('.text');
    const icon = updater.find('.icon');
    if (icon.hasClass('icon--blue')) {
      updaterText.text('В сравнении');
    } else {
      updaterText.text('Добавить в сравнение');
    }
  },
  productCard(data, target, updater) {
    let count = parseInt(target.first().text());
    const icon = updater.find('.icon');
    const badge = updater.find('.badge');

    if (icon.text().includes('add_shopping_cart')) {
      target.text(++count);
      badge.text(parseInt(badge.text()) + 1);
    } else {
      icon.text('add_shopping_cart');
      updater.data('countUpdaterUrl', `/cart/${data.id}/increment`);
      target.removeClass('hidden');
      target.text(++count);
      badge.removeClass('hidden');
      badge.text(1);
    }
  }
};


function sendMessage(message, delayMs = 3000) {
  if ($('.messages__item').toArray().some(item => $(item).text().trim() == message)) return;
  const messageItem = $(`<div class="messages__item">${message}</div>`).appendTo('.messages__inner');
  setTimeout(() => messageItem.remove(), delayMs);
}


$(function() {
  $('#catalog-active-checkbox').on('change', function() {
    const icon = $('#catalog-menu-open-button-icon, #catalog-menu-close-button-icon');
    icon.toggleClass('hidden');
  });

  $('[data-count-updater][data-count-updater-url]').on('click', function() {
    $.ajax({
      url: $(this).data('countUpdaterUrl'),
    }).done(data => {
      const target = $(`[data-update-count="${$(this).data('countUpdater')}"]`); 
      const methodName = $(this).data('countUpdaterMethod');
      if (!(methodName in METHODS)) {
        console.error(`${methodName} not in ${Object.keys(METHODS)}.`)
        return;
      }
      METHODS[methodName](data, target, $(this));
      if (data.message != null) {
        sendMessage(data.message)
      }
    }).fail(({responseJSON}) => {
      if (responseJSON.message != null) {
        sendMessage(responseJSON.message);
      }
    });
  });

  $('.product__img-container').on('click', function() {
    $('.product__img-container.selected').removeClass('selected');
    $(this).addClass('selected');
    $('.product__main-img').attr('src', $(this).find('.product__img').attr('src'));
  });

  $('.accordion__header').on('click', function() {
    $(this).parent('.accordion').toggleClass('active');
  });
});