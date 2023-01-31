/// <reference types="jquery"/>

const METHODS = {
  hideIf0(data, target, updater) {
    let count = parseInt(target.text());
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
  productCard(data, target, updater) {
    let count = parseInt(target.text());
    const icon = updater.find('.icon');
    const badge = updater.find('.badge');
    console.log(icon.text(), count)

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
        const messageItem = $(`<div class="messages__item">${data.message}</div>`).appendTo('.messages__inner');
        setTimeout(() => messageItem.remove(), 3000);
      }
    });
  });

  $('.badge-parent').each(function() {
    console.log(this);
  });
});