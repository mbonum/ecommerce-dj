// async
if (document.readyState == 'loading') {
  document.addEventListener('DOMContentLoaded', ready);
} else {
  ready();
}
function ready() {
  var removeBtn = document.getElementsByClassName('rem');
  for (var i = 0; i < removeBtn.length; i++) {
    var btn = removeBtn[i];
    btn.addEventListener('click', removeCartItem);
  }
  var qtyInputs = document.getElementsByClassName('cart-qty');
  for (var i = 0; i < qtyInputs.length; i++) {
    var input = qtyInputs[i];
    input.addEventListener('change', qtyChanged);
  }
}

function removeCartItem(event) {
  var btnClicked = event.target;
  btnClicked.parentElement.remove();
  updateCartTotal();
}

function qtyChanged(event) {
  var input = event.target;
  if (isNaN(input.value) || input.value <= 0) {
    input.value = 1;
  }
  updateCartTotal();
}

function updateCartTotal() {
  var cartContainer = document.getElementsByClassName('cart-body')[0]
  var cartRows = document.getElementsByClassName('cart-product');
  var c = document.getElementsByClassName('currency');
  var total = 0;
  for (var i = 0; i < cartRows.length; i++) {
    var cartRow = cartRows[i];
    var priceItem = cartRow.getElementsByClassName('price-item')[0]
    var qtyItem = cartRow.getElementsByClassName('qty-item')[0];
    // var price = parseFloat(priceItem.innerText.replace('$', ''));
    var qty = qtyItem.nodeValue;
    total = total + (price * qty);
  }
  total = Math.round(total * 100) / 100;
  document.getElementsByClassName('cart-total')[0].innerText = c + total;
}