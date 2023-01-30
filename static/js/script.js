/// <reference types="jquery"/>

const METHODS = {
  hideIf0(data, target, updater) {
    target.text(data.totalCount);
    if (!data.totalCount) target.addClass('hidden')
    else target.removeClass('hidden');

    const icon = updater.find('.icon');
    if (data.count) {
      icon.removeClass('icon--gray');
      icon.addClass('icon--blue');
    } else {
      icon.removeClass('icon--blue');
      icon.addClass('icon--gray');
    }
  },
  productCard(data, target, updater) {
    target.text(data.totalCount);
    if (!data.totalCount) target.addClass('hidden')
    else target.removeClass('hidden');

    if (data.count) {
      if (target.find('.icon').text() == 'shopping_cart') {
        
      }
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
      console.log(data, target, methodName);
      if (!(methodName in METHODS)) {
        console.error(`${methodName} not in ${Object.keys(METHODS)}.`)
        return;
      }
      METHODS[methodName](data, target, $(this));
    });
  });
});