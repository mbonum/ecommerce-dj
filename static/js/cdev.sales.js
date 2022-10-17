$(document).ready(function () {
  function renderChart(id, data, labels) {
    // var ctx = document.getElementById('myChart').getContext('2d');
    var ctx = $('#' + id)
    var myChart = new Chart(ctx, {
      type: 'line',// radar bar pie https://www.chartjs.org/docs/latest/charts/
      data: {
        labels: labels,
        datasets: [{
          label: 'Sales',
          data: data,
          backgroundColor: 'rgba(0, 173, 67, 0.2)',
          borderColor: 'rgba(0, 173, 67, 1)',
          // backgroundColor: ['rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)',
          //     'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)',
          //     'rgba(153, 102, 255, 0.2)', 'rgba(110, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'
          // ],
          // borderColor: ['rgba(255,99,132,1)', 'rgba(54, 162, 235, 1)',
          //     'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)',
          //     'rgba(153, 102, 255, 1)', 'rgba(110, 102, 255, 1)', 'rgba(255, 159, 64, 1)'
          // ],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        },
        backgroundColor: 'rgba(75, 192, 192, 1)'
      }
    });
  }
  function getSalesData(id, type) {
    var url = '/analytics/sales/data/'
    var method = 'GET'
    var data = { 'type': type }
    $.ajax({
      url: url,
      method: method,
      data: data,
      success: function (response) {
        renderChart(id, response.data, response.labels)
      }, error: function (error) {
        $.alert({
          title: 'Sorry.',
          content: 'An error occured, please reload the page.',
          theme: 'modern'//supervan dark material bootstrap
        });
      }
    })
  }
  var chartsToRender = $('.render-saleschart')
  $.each(chartsToRender, function (index, html) {
    var $this = $(this);
    if ($this.attr('id') && $this.attr('data-type')) {
      getSalesData($this.attr('id'), $this.attr('data-type'));
    }
  });
  jconfirm.defaults = {
  // $.confirm({
    title: 'Clavem',
    titleClass: 'font-c-sans',
    // type: 'default',
    typeAnimated: true,
    draggable: true,
    dragWindowGap: 15,
    dragWindowBorder: true,
    animateFromElement: true,
    smoothContent: true,
    content: 'Are you sure to continue?',
    // contentClass: 'font-c-sans',
    buttons: {
      ok: {
        action: function () {
          // ***
        }
      },
    },
    // defaultButtons: {
      // close: {
        // action: function () {
        // }
    //   },
    // },
    // contentLoaded: function (data, status, xhr) {
    // },
    // icon: '',
    lazyOpen: false,
    bgOpacity: true,
    theme: 'dark',//light
    animation: 'scale',
    closeAnimation: 'scale',
    animationSpeed: 300,
    animationBounce: 1,
    rtl: false,
    container: 'body',
    containerFluid: false,
    backgroundDismiss: true,
    backgroundDismissAnimation: 'shake',
    closeIcon: true,
    // closeIconClass: false,
    watchInterval: 100,
    // columnClass: 'max-w-xs mx-auto',
    boxWidth: '25%',
    scrollToPreviousElement: true,
    scrollToPreviousElementAnimate: true,
    useBootstrap: false,
    // offsetTop: 40,
    offsetBottom: 90,//
    // bootstrapClasses: {
    //   container: 'container',
    //   containerFluid: 'container-fluid',
    //   row: 'row',
    // },
    // onContentReady: function () { },
    // onOpenBefore: function () { },
    // onOpen: function () { },
    // onClose: function () { },
    // onDestroy: function () { },
    // onAction: function () { }
  };//)
})