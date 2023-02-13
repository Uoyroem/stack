/// <reference types="jquery"/>

// HELPERS
function formatPrice(price, sep = ' ', denomination = '₸') {
  if (!price) {
    return null;
  }
  return [...price.toString()].reverse().join('').match(/\d{1,3}/g).reverse().map(part => [...part].reverse().join('')).join(sep) + ' ' + denomination;
}

function combine(...functions) {
  return function(...args) {
    return functions.reduce((value, currentFunction) => value == null ? currentFunction.apply(this, args) : currentFunction.call(this, value), null);
  }
}
function increment(_, oldCount) {
  return parseInt(oldCount.trim()) + 1;
}
function decrement(_, oldCount) {
  return parseInt(oldCount.trim()) - 1;
}
function addOrRemoveClassesIf(addOrRemove, classes, predicate) {
  return function(value) {
    if (predicate.call(this, value)) {
      if (addOrRemove == 'add' || addOrRemove == 'remove') {
        $(this)[`${addOrRemove}Class`](classes);
      } else {
        console.error('The argument addOrRemove should be "add" or "remove"');
      }
    }
    return value;
  }
}
const addHiddenIf0 = addOrRemoveClassesIf('add', 'hidden', value => value == 0);
function removeHiddenClass(value) {
  $(this).removeClass('hidden');
  return value;
}

const incrementAndRemoveHiddenClass = combine(increment, removeHiddenClass);
const decrementAndAddHiddenIf0 = combine(decrement, addHiddenIf0);

function cartRemoveIf0(cartProduct) {
  return function(value) {
    if (value == 0) {
      const cartList = cartProduct.parent();
      cartProduct.next().remove();
      cartProduct.remove();
      if (!cartList.children().length) {
        const parent = cartList.parent()
        parent.children().remove();
        $('<div>Корзина пуста</div>').appendTo(parent);
      }
    }
    return value;
  }
}


// Знаю что ужасно всё это выглядит, но пока это лучшее что мне пришло в голову. 
const METHODS = {
  hideIf0(data, target, updater) {
    const icon = updater.find('.icon');
    // Если кнопка активна то у него есть icon--blue класс.
    if (icon.hasClass('icon--blue')) {
      icon.removeClass('icon--blue').addClass('icon--gray');
      target.text(decrementAndAddHiddenIf0);
    } else {
      icon.removeClass('icon--gray').addClass('icon--blue');
      target.text(incrementAndRemoveHiddenClass);
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
    const icon = updater.find('.icon');
    const badge = updater.find('.badge');

    if (icon.text().includes('add_shopping_cart')) {
      target.text(increment);
      badge.text(increment);
    } else {
      icon.text('add_shopping_cart');
      updater.data('countUpdaterUrl', `/cart/${data.id}/increment`);
      target.text(incrementAndRemoveHiddenClass);
      badge.text(incrementAndRemoveHiddenClass);
    }
  },
  productCart(data, target, updater) {
    updater.addClass('hidden');
    const buttonGroup = updater.next();
    target.text(incrementAndRemoveHiddenClass);
    buttonGroup.removeClass('hidden');
    buttonGroup.find('.product__cart-count').text(1);
    buttonGroup.children().first().attr('data-count-updater-url', `/cart/${data.id}/decrement`).end()
                          .last().attr('data-count-updater-url', `/cart/${data.id}/increment`);
  },
  cartIncrement(data, target, updater) {
    target.text(increment);
    updater.prev().find('.product__cart-count').text(increment);
  },
  cartDecrement(data, target, updater) {
    target.text(decrementAndAddHiddenIf0);
    updater.next().find('.product__cart-count').text(combine(decrement, function(value) {
      if (value == 0) {
        $(this).parents('.button-group').addClass('hidden').prev().removeClass('hidden');
      }
      return value;
    }));
  },
  cartProductIncrement(data, target, updater) {
    const totalPrice = $('.cart-buy .cart-buy__info-price');
    const cartProduct = $(updater).parents('.cart-product');
    const productPrice = cartProduct.find('.cart-product__info-price');
    const counter = updater.prev();
    const count = parseInt(counter.text());
    const price = parseInt(productPrice.text().split(' ').join('')) / count
    totalPrice.text(function(_, oldPrice) {
      oldPrice = oldPrice.split(' ').join('');
      return formatPrice(parseInt(oldPrice) + price);
    });
    target.text(incrementAndRemoveHiddenClass);
    counter.text(combine(increment, function(value) {
      productPrice.text(formatPrice(price * value));
      return value;
    }));
  },
  cartProductDecrement(data, target, updater) {
    target.text(decrementAndAddHiddenIf0);
    const totalPrice = $('.cart-buy .cart-buy__info-price');
    const cartProduct = $(updater).parents('.cart-product');
    const productPrice = cartProduct.find('.cart-product__info-price');
    const counter = updater.next();
    const count = parseInt(counter.text());
    const price = parseInt(productPrice.text().split(' ').join('')) / count
    totalPrice.text(function(_, oldPrice) {
      oldPrice = oldPrice.split(' ').join('');
      return formatPrice(parseInt(oldPrice) - parseInt(price));
    });
    updater.next().text(combine(decrement, cartRemoveIf0(cartProduct), function(value) {
      productPrice.text(formatPrice(price * value));
      return value;
    }));
  },
  cartProductDelete(data, target, updater) {
    const totalPrice = $('.cart-buy .cart-buy__info-price');
    const cartProduct = $(updater).parents('.cart-product');
    const productPrice = cartProduct.find('.cart-product__info-price');
    const counter = cartProduct.find('.cart-product__info-count');
    const count = parseInt(counter.text());
    const price = parseInt(productPrice.text().split(' ').join('')) / count;
    totalPrice.text(function(_, oldPrice) {
      oldPrice = oldPrice.split(' ').join('');
      return formatPrice(parseInt(oldPrice) - price * count);
    });
    target.text(combine(function(_, oldCount) {
      console.log(oldCount, count)
      console.log(parseInt(oldCount) - count)
      return parseInt(oldCount) - count
    }, cartRemoveIf0(cartProduct), addHiddenIf0));
    cartProduct.next().remove();
    cartProduct.remove();
    
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

  $('.review-form__rating-stars .icon').hover(
    function() {
      $(this).prevAll().addBack().addClass('icon--blue');
    }, function() {
      $(this).prevAll().addBack().filter(':not([data-selected])').removeClass('icon--blue');
    }).on('click', function() {
      $('.review-form__rating-stars .icon').removeClass('icon--blue').removeAttr('data-selected');
      $('.review-form__rating-input').val($(this).index() + 1);
      $(this).prevAll().addBack().addClass('icon--blue').attr('data-selected', true);
    });

    $('.tabs .tabs__tab[data-active-tab-content]').on('click', function() {
      $(this).siblings().removeClass('active');
      $(this).addClass('active');
      
      const tabContent = $(`#${$(this).data('activeTabContent')}`);
      tabContent.siblings().removeClass('active');
      tabContent.addClass('active');
    });

    $('.button.button--link[data-href]').on('click', function() {
      location.replace($(this).data('href'));
    });

    setTimeout(() => $('.catalog').removeClass('hidden'), 1500);
});