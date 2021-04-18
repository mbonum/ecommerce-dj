$(document).ready(function () {
  function renderChart(id, data, labels) {
    // var ctx = document.getElementById("myChart").getContext('2d');
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
        }
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
      success: function (responseData) {
        renderChart(id, responseData.data, responseData.labels)
      }, error: function (error) {
        $.alert('An error occured')
      }
    })
  }
  var chartsToRender = $('.render-saleschart')
  $.each(chartsToRender, function (index, html) {
    var $this = $(this)
    if ($this.attr('id') && $this.attr('data-type')) {
      getSalesData($this.attr('id'), $this.attr('data-type'))
    }
  })
})