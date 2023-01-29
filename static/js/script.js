/// <reference types="jquery"/>

$(function() {
  $('#catalog-active-checkbox').on('change', function() {
    const icon = $('#catalog-menu-open-button-icon, #catalog-menu-close-button-icon');
    icon.toggleClass('hidden');
  });

  $('[data-count-updater][data-count-updater-url]').on('click', function() {
    $.ajax({
      url: $(this).data('countUpdaterUrl'),
    }).done(({message, count, totalCount}) => {
      const target = $(`[data-update-count="${$(this).data('countUpdater')}"]`);
      const icon = $(this).find('.icon');
      console.log(message, count, totalCount)
      if (!count) {
        icon.removeClass('icon--blue');
        icon.addClass('icon--gray');
      }
      else {
        icon.removeClass('icon--gray');
        icon.addClass('icon--blue');
      }
      target.text(totalCount);
      if (!totalCount) {
        target.addClass('hidden');
      } else {
        target.removeClass('hidden');
      }
    });
  });
});