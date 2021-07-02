$(document).ready(function () {
  var contactForm = $(".contact-form");
  var contactFormMethod = contactForm.attr("method");
  var contactFormEndpoint = contactForm.attr("action");
  function displaySubmitting(submitBtn, defaultText, doSubmit) {
    if (doSubmit) {
      submitBtn.addClass("disabled");
      submitBtn.html(`<svg class="animate-spin" viewBox="0 0 80 80"><path d="M40,72C22.4,72,8,57.6,8,40C8,22.4, 22.4,8,40,8c17.6,0,32,14.4,32,32c0,1.1-0.9,2-2,2 s-2-0.9-2-2c0-15.4-12.6-28-28-28S12,24.6,12,40s12.6, 28,28,28c1.1,0,2,0.9,2,2S41.1,72,40,72z"></path></svg>`);
    } else {// xml:space="preserve" aria-hidden="true" w-4 h-4 text-gray-700 fill-current mr-2 Sending...<animateTransform attributeType="xml" attributeName="transform" type="rotate" from="0 40 40" to="360 40 40" dur="0.8s" repeatCount="indefinite"/>
      submitBtn.removeClass("disabled");
      submitBtn.html(defaultText);
    }
  }
  contactForm.submit(function (e) {
    e.preventDefault();
    var contactFormSubmitBtn = contactForm.find("[type='submit']");
    var contactFormSubmitBtnTxt = contactFormSubmitBtn.text();
    var contactFormData = contactForm.serialize();
    var thisForm = $(this);
    displaySubmitting(contactFormSubmitBtn, "", true)
    $.ajax({
      url: contactFormEndpoint,
      method: contactFormMethod,
      data: contactFormData,
      success: function (_data) {
        thisForm[0].reset();
        $.alert({
          title: "Thank you!",
          content: "We're going to answer you as soon as we can.",// data.message
          theme: "modern",
        });
        setTimeout(function () {
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
        }, 2000);
      },
      error: function (error) {
        var jsonData = error.responseJSON;
        var msg = "";
        $.each(jsonData, function (key, value) {// key, value array index / object
          msg += key + ": " + value[0].message + "<br/>";
        });
        $.alert({
          title: "Sorry, try to reload",
          content: msg,
          theme: "modern",
        });
        setTimeout(function () {
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
        }, 500);
      }
    });
  });
  // Auto Search
  var searchForm = $(".search-form");
  var searchInput = searchForm.find("[name='q']");// input name='q'
  var typingTimer;
  var typingInterval = 500;
  var searchBtn = searchForm.find("[type='submit']");

  searchInput.keyup(function (e) {
    // key released
    clearTimeout(typingTimer);
    typingTimer = setTimeout(performSearch, typingInterval);
  })
  searchInput.keydown(function (e) {
    // key pressed
    clearTimeout(typingTimer);
  })
  function displaySearching() {
    searchBtn.addClass("disabled");
    searchBtn.html(`<svg class="animate-spin hover:text-black fill-current w-4 h-4" viewBox="0 0 80 80" xml:space="preserve"><path d="M40,72C22.4,72,8,57.6,8,40C8,22.4, 22.4,8,40,8c17.6,0,32,14.4,32,32c0,1.1-0.9,2-2,2 s-2-0.9-2-2c0-15.4-12.6-28-28-28S12,24.6,12,40s12.6, 28,28,28c1.1,0,2,0.9,2,2S41.1,72,40,72z"></svg>`);
  }
  function performSearch() {
    displaySearching();
    var query = searchInput.val();
    setTimeout(function () {
      window.location.href = "/search/?q=" + query;
    }, typingInterval);
  }
  // Cart + add products
  var productForm = $(".form-product-ajax");

  function getOwnedProduct(productId, submitSpan) {
    var actionEndpoint = "/orders/endpoint/verify/ownership/";
    var httpMethod = "GET";
    var data = {
      product_id: productId
    };
    var isOwner;
    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: data,
      success: function (data) {
        if (data.owner) {
          isOwner = true;
          submitSpan.html(`<a class="bg-blue-500 border-4 border-blue-500 hover:bg-blue-600 hover:border-blue-600 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2" href="/library/">In Library</a>`);// dig_lib_url
        } else {
          isOwner = false;
        }
      },
      error: function (error) {
        console.log(error);
      }
    })
    return isOwner;
  }
  $.each(productForm, function (_index, _object) {
    var $this = $(this);
    var isUser = $this.attr("data-user");
    var submitSpan = $this.find(".submit-span");
    var productInput = $this.find("[name='product_id']");
    var productId = productInput.attr("value");
    var productIsDigital = productInput.attr("data-is-digital");
    if (productIsDigital && isUser) {
      getOwnedProduct(productId, submitSpan);
      //var isOwned =  if (isOwned){
      //   submitSpan.html("<a href='/library/'>In Library</a>")
      // }
    }//else { submitSpan.html("<button type='submit' class='inline-flex items-center bg-yellow-400 hover:bg-yellow-500 border-4 border-yellow-400 hover:border-yellow-500 text-xs rounded focus:outline-none focus:ring-1 ring-yellow-200 ring-offset-transparent ring-offset-2 transform hover:scale-110 py-1 px-2'>Buy</button>")}
  })
  // Cart async Buy/In Cart moved Remove btn on Cart
  productForm.submit(function (e) {
    e.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();
    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function (data) {
        var submitSpan = thisForm.find(".submit-span");
        if (data.added) {
          submitSpan.html(`<a href="/cart/" class="inline-flex items-center bg-gradient-to-tr to-yellow-300 from-yellow-400 hover:to-yellow-300 hover:from-yellow-500 text-gray-800 border-2 border-yellow-300 hover:border-yellow-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2"><svg class="fill-current w-4 h-4 mr-2" aria-labelledby="title" title="Your cart" preserveAspectRatio="xMidYMid meet" viewBox="0 0 21 21"><path d="M16.2 14.919H7.837l-.827-2.884 10.158-.746 1.9-7.063H4.783l-.051-.192C4.035 1.557 3.741.418 1.163.162A.815.815 0 1 0 1 1.784c1.73.172 1.793 1.38 2.162 2.694l3.3 11.506a1.694 1.694 0 1 0 .285.939 1.63 1.63 0 0 0-.042-.374h8.106a1.722 1.722 0 0 0-.044.386 1.688 1.688 0 0 0 1.689 1.691 1.776 1.776 0 0 0 1.692-1.788 1.905 1.905 0 0 0-1.948-1.919z"></path></svg>In Cart</a>`);
          /*<button type='submit' class='inline-flex items-center rounded border-b-4 border-gray-600 text-gray-700 hover:text-gray-800 hover:border-gray-700 bg-gray-300 p-2 pb-1'><svg class='fill-current w-4 h-4' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 25 24'><path d='M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z'/></svg><span class='text'>Remove</span></button>") aria-labelledby="title"*/
        } else {
          submitSpan.html(`<button type="submit" class="inline-flex items-center bg-gradient-to-tr to-yellow-300 from-yellow-400 hover:to-yellow-300 hover:from-yellow-500 text-gray-800 border-2 border-yellow-300 hover:border-yellow-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2"><svg class="fill-current w-4 h-4 mr-2" preserveAspectRatio="xMidYMid meet" viewBox="0 0 21 21"><path d="M16.2 14.919H7.837l-.827-2.884 10.158-.746 1.9-7.063H4.783l-.051-.192C4.035 1.557 3.741.418 1.163.162A.815.815 0 1 0 1 1.784c1.73.172 1.793 1.38 2.162 2.694l3.3 11.506a1.694 1.694 0 1 0 .285.939 1.63 1.63 0 0 0-.042-.374h8.106a1.722 1.722 0 0 0-.044.386 1.688 1.688 0 0 0 1.689 1.691 1.776 1.776 0 0 0 1.692-1.788 1.905 1.905 0 0 0-1.948-1.919z"></path></svg>Buy</button>`);
        }
        // document.getElementById("qty").innerHTML = $('#qty option:selected').text();//
        var navbarCount = $(".navbar-cart-count");
        navbarCount.text(data.cartItemCount);
        var currentPath = window.location.href;
        if (currentPath.indexOf("cart") = -1) {
          refreshCart();
        }
      },
      error: function (_error) {
        $.alert({
          title: "Sorry!",
          content: "An error occurred. Try to reload the page.",
          theme: "modern",
        });
      }
    })
  })
  function refreshCart() {
    var cartTable = $(".cart-table");
    var cartBody = cartTable.find(".cart-body");
    var productRows = cartBody.find(".cart-product");
    var currentUrl = window.location.href;
    var refreshCartUrl = "/api/cart/";
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function (data) {
        var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
        if (data.products.length > 0) {
          productRows.html(" ");
          i = data.products.length;
          // var qty = $('#qty option:selected').text();
          var currency = data.currency;
          if (currency == "USD") { currency = "$" } else { currency = "€" }
          $.each(data.products, function (_index, value) {
            var newCartItemRemove = hiddenCartItemRemoveForm.clone();
            newCartItemRemove.css("display", "block");//.removeClass("hidden-class")
            newCartItemRemove.find(".cart-item-product-id").val(value.id);
            // console.log(value) cart.views cart_detail_api_view<td scope="row" class="text-sm">' + i + '</td>
            // <img class="w-20 h-20" src="{ { object.image.url }}">
            cartBody.prepend(`<tr class="cart-product border-b border-gray-300 align-middle text-center">
            <td colspan="1"></td><td class="justify-around px-4 py-2"><a class="hover:text-blue-a focus:outline-none" href="' + value.url + '" target="_blank">`
              + value.name + `</a></td><td colspan="1"></td>` + // + value.qty + 
              //'<select class="appearance-none border border-gray-400 text-black p-1 rounded-lg focus:outline-none focus:ring ring-yellow-100 ring-offset-transparent ring-offset-1 bg-white hover:border-gray-600 shadow" name="qty" id="id_qty"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-gray-600"><svg class="r-180 fill-current h-4 w-4" viewBox="0 0 20 20" aria-hidden="true"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"></path></svg><td class="px-4 py-2">'
              `<td class="text-center">` + currency + " " + value.price + `</td><td class="sm:pl-2 py-2 xl:border-b xl:border-gray-300">` + newCartItemRemove.html() + `</td></tr>`);
            // if (currency === "$" || currency === "£") { qty *
            //   cartBody.prepend("<tr class='cart-product border-b border-gray-300 align-middle text-center'><th scope=\"row\">" + i + "</th><td class='px-4 py-2'><a class='hover:text-blue-700 focus:outline-none' href='" + value.url + "' target='_blank'>"
            //     + value.name + "</a></td><td class='px-4 py-2'> " + currency + " "
            //     + value.price + "</td><td class='sm:pl-2 py-2 xl:border-b xl:border-gray-300'>" + newCartItemRemove.html() + "</td></tr>")
            // } else {
            //   cartBody.prepend("<tr class='cart-product border-b border-gray-300 align-middle text-center'><th scope=\"row\">" + i + "</th><td class='px-4 py-2d'><a class='hover:text-blue-700 focus:outline-none focus:shadow-outline' href='" + value.url + "' target='_blank'>"
            //   + value.name + "</a></td><td class='px-4 py-2'>"
            //   + value.price + " " + currency + "</td><td class='sm:pl-2 py-2 xl:border-b xl:border-gray-300'>" + newCartItemRemove.html() + "</td></tr>")
            // }
            i--
          })// cartBody.find(".cart-subtotal").text(data.subtotal) qty * // ship cost
          cartBody.find(".cart-total").text(currency + " " + data.total);
          // if (currency === "$" || currency === "£") {
          //   cartBody.find(".cart-total").text(currency + " " + data.total)
          // } else {
          //   cartBody.prepend(cartBody.find(".cart-total").text(data.total) + " " + currency)
          // }
        } else {
          $(location).attr('href', currentUrl);
          window.location.href = currentUrl; // bug
          location.reload();
        }
      },
      error: function (_error) {
        $.alert({
          title: "Sorry!",
          content: "An error occurred. Try to reload the page.",
          theme: "modern",//material bootstrap supervan dark light
        });
      }
    })
  }
})
