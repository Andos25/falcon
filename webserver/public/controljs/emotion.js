$(document).ready(function() {
  $("li#3").addClass('section');
  get_emotion();
});

var get_emotion = function() {
  $.getJSON("/ajax/emotion/", function(data) {
    buildchart(data);
  })
}

var buildchart = function(info) {
  $('#container').highcharts({
    chart: {
      type: 'pie',
      options3d: {
        enabled: true,
        alpha: 45
      }
    },
    title: {
      text: 'Contents of Highsoft\'s weekly fruit delivery'
    },
    subtitle: {
      text: '3D donut in Highcharts'
    },
    plotOptions: {
      pie: {
        innerSize: 100,
        depth: 45
      }
    },
    series: [{
      name: 'Delivered amount',
      data: info
    }]
  });
}