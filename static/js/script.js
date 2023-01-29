/// <reference types="jquery"/>

$(function() {
  $('#catalog-active-checkbox').on('change', function() {
    const icon = $('#catalog-menu-open-button-icon, #catalog-menu-close-button-icon');
    icon.toggleClass('hidden');
  });

  $('[data-count-updater][data-count-updater-url]').on('click', function() {
    $.ajax({
      url: this.dataset.countUpdaterUrl,
    }).done(({message, count}) => {
      const target = $(`[data-update-count="${$(this).data('countUpdater')}"]`);
      const icon = $(this).find('.icon');
      if (!count) {
        target.hide();
        icon.removeClass('icon--blue');
        icon.addClass('icon--gray');
        return;
      }
      target.show();
      target.text(count);
      icon.removeClass('icon--gray');
      icon.addClass('icon--blue');
      if ($(this).attr('data-hide-if') == null) return;
      console.log(eval($(this).data('hideIf')));
      console.log(count);
      if (eval($(this).data('hideIf'))) {
        $(this).hide();
      } else {
        $(this).show();
      }
    });
  });
});