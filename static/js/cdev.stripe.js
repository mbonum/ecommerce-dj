$(document).ready(function () {
  var stripeFormModule = $(".stripe-payment-form")
  var stripeModuleToken = stripeFormModule.attr("data-token")
  var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
  var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add card 💳"
  var stripeTemplate = $.templates("#stripeTemplate")
  var stripeTemplateDataContext = {
    publishKey: stripeModuleToken,
    nextUrl: stripeModuleNextUrl,
    btnTitle: stripeModuleBtnTitle
  }
  var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
  stripeFormModule.html(stripeTemplateHtml)

  // https
  var paymentForm = $(".payment-form")
  if (paymentForm.length > 1) {
    $.alert("Only one payment form is allowed per page")
    paymentForm.css("display", "none")
  }
  else if (paymentForm.length == 1) {

    var pubKey = paymentForm.attr("data-token")
    var nextUrl = paymentForm.attr("data-next-url")
    // Create a Stripe client
    var stripe = Stripe(pubKey);

    // Create an instance of Elements
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element
    var style = {
      base: {
        color: "#32325d",
        lineHeight: "22px",
        fontFamily: "'Helvetica Neue', Helvetica, sans-serif",
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
          color: "#95a1ae"//#aab7c4
        }
      },
      invalid: {
        color: "#fa755a",
        iconColor: "#fa755a"
      }
    };

    // Create an instance of the card Element
    var card = elements.create("card", { style: style });

    // Add an instance of the card Element into the `card-element` <div>
    card.mount("#card-element");

    // Handle real-time validation errors from the card Element
    card.addEventListener("change", function (event) {
      var displayError = document.getElementById("card-errors");
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = "";
      }
    });
    // Handle form submission
    // var form = document.getElementById('payment-form');
    // form.addEventListener('submit', function(event) {
    //   event.preventDefault();
    //   // get the btn
    //   // display new btn ui
    //   var loadTime = 1500
    //   var errorHtml = "<i class='fa fa-warning'></i> An error occured"
    //   var errorClasses = "btn btn-danger disabled my-3"
    //   var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
    //   var loadingClasses = "btn btn-success disabled my-3"

    //   stripe.createToken(card).then(function(result) {
    //     if (result.error) {
    //       // Inform the user if there was an error
    //       var errorElement = document.getElementById('card-errors');
    //       errorElement.textContent = result.error.message;
    //     } else {
    //       // Send the token to your server
    //       stripeTokenHandler(nextUrl, result.token);
    //     }
    //   });
    // });
    var form = $("#payment-form");
    var btnLoad = form.find(".btn-load")
    var btnLoadDefaultHtml = btnLoad.html()
    var btnLoadDefaultClasses = btnLoad.attr("class")
    form.on("submit", function (event) {
      event.preventDefault();
      // get the btn
      // display new btn ui
      var $this = $(this)
      // btnLoad = $this.find('.btn-load')
      btnLoad.blur()
      var loadTime = 900
      var currentTimeout;
      var errorHtml = "<span class='text-gray-600'><svg class='w-4 h-4 fill-current mr-1' viewBox='0 0 1792 1792' xmlns='http://www.w3.org/2000/svg' aria-hidden='true'><path d='M1088 1248v224q0 26-19 45t-45 19H768q-26 0-45-19t-19-45v-224q0-26 19-45t45-19h256q26 0 45 19t19 45zm30-1056l-28 768q-1 26-20.5 45t-45.5 19H768q-26 0-45.5-19T702 960l-28-768q-1-26 17.5-45t44.5-19h320q26 0 44.5 19t17.5 45z'/></svg> An error occured</span>"//<i class='fa fa-warning'></i> An error occured
      var errorClasses = "bg-red-600 rounded disabled my-3"//btn btn-danger disabled my-3
      var loadingHtml = "<span class='text-gray-600'><svg class='w-4 h-4 fill-current mr-1' viewBox='0 0 1792 1792' xmlns='https://www.w3.org/2000/svg' aria-hidden='true'><path d='M526 1394q0 53-37.5 90.5T398 1522q-52 0-90-38t-38-90q0-53 37.5-90.5T398 1266t90.5 37.5T526 1394zm498 206q0 53-37.5 90.5T896 1728t-90.5-37.5T768 1600t37.5-90.5T896 1472t90.5 37.5 37.5 90.5zM320 896q0 53-37.5 90.5T192 1024t-90.5-37.5T64 896t37.5-90.5T192 768t90.5 37.5T320 896zm1202 498q0 52-38 90t-90 38q-53 0-90.5-37.5T1266 1394t37.5-90.5 90.5-37.5 90.5 37.5 37.5 90.5zM558 398q0 66-47 113t-113 47-113-47-47-113 47-113 113-47 113 47 47 113zm1170 498q0 53-37.5 90.5T1600 1024t-90.5-37.5T1472 896t37.5-90.5T1600 768t90.5 37.5T1728 896zm-640-704q0 80-56 136t-136 56-136-56-56-136 56-136T896 0t136 56 56 136zm530 206q0 93-66 158.5T1394 622q-93 0-158.5-65.5T1170 398q0-92 65.5-158t158.5-66q92 0 158 66t66 158z'/></svg> Loading...</span>"//<i class='fa fa-spin fa-spinner'></i> Loading...
      var loadingClasses = "uppercase my-6 border-4 bg-blue-400 border-blue-400 hover:bg-blue-600 hover:border-blue-600 hover:text-white py-1 px-2 rounded-sm text-xs"//<button class="my-6 border-4 bg-yellow-400 border-yellow-400 hover:bg-yellow-600 hover:border-yellow-600 text-gray-900 hover:text-white py-1 px-2 rounded text-sm btn-load">//{{:btnTitle}}</button>//btn btn-success disabled my-3
      stripe.createToken(card).then(function (result) {
        if (result.error) {
          // Inform the user if there was an error
          var errorElement = $("#card-errors");
          errorElement.textContent = result.error.message;
          currentTimeout = displayBtnStatus(
            btnLoad,
            errorHtml,
            errorClasses,
            900,
            currentTimeout
          )
        } else {
          // Send the token to your server
          currentTimeout = displayBtnStatus(
            btnLoad,
            loadingHtml,
            loadingClasses,
            999,
            currentTimeout
          )
          stripeTokenHandler(nextUrl, result.token);
        }
      });
    });
    function displayBtnStatus(element, newHtml, newClasses, loadTime) {//, timeout
      // if (timeout){
      //   clearTimeout(timeout)
      // }
      if (!loadTime) {
        loadTime = 900
      }
      //var defaultHtml = element.html()
      //var defaultClasses = element.attr("class")
      element.html(newHtml)
      element.removeClass(btnLoadDefaultClasses)
      element.addClass(newClasses)
      return setTimeout(function () {
        element.html(btnLoadDefaultHtml)
        element.removeClass(newClasses)
        element.addClass(btnLoadDefaultClasses)
      }, loadTime)
    }

    function redirectToNext(nextPath, timeoffset) {
      if (nextPath) {
        setTimeout(function () {
          window.location.href = nextPath
        }, timeoffset)
      }
    }
    // Submit the form with the token ID
    function stripeTokenHandler(nextUrl, token) {
      // console.log(token.id)
      var paymentMethodEndpoint = "/billing/payment-method/create/"
      var data = {
        "token": token.id
      }
      $.ajax({
        data: data,
        url: paymentMethodEndpoint,
        method: "POST",
        success: function (data) {
          var succesMsg = data.message || "Great! Your card has been added. Thank you"
          card.clear()
          if (nextUrl) {
            succesMsg = succesMsg + "<br><p class='items-center inline-flex'><svg class='animate-spin w-4 h-4 mr-2' viewBox='0 0 80 80' xml:space='preserve'><path d='M40,72C22.4,72,8,57.6,8,40C8,22.4, 22.4,8,40,8c17.6,0,32,14.4,32,32c0,1.1-0.9,2-2,2 s-2-0.9-2-2c0-15.4-12.6-28-28-28S12,24.6,12,40s12.6, 28,28,28c1.1,0,2,0.9,2,2S41.1,72,40,72z'></svg> Redirecting...</p>"//<br/><i class='fa fa-spin fa-spinner'></i> Redirecting...
          }
          if ($.alert) {
            $.alert(succesMsg)
          } else {
            alert(succesMsg)
          }
          btnLoad.html(btnLoadDefaultHtml)
          btnLoad.attr("class", btnLoadDefaultClasses)
          redirectToNext(nextUrl, 900)
        },
        error: function (error) {
          // console.log(error)
          $.alert({ title: "We're sorry, an error occured", content: "Please reload the page and try again. If the error persists please contact us." })
          btnLoad.html(btnLoadDefaultHtml)
          btnLoad.attr("class", btnLoadDefaultClasses)
        }
      })
    }
  }
})