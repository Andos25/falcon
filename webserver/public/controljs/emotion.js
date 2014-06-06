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
    credits: 
   {
      enabled : false
    },
    
    title: {
      text: '情感倾向分析'
    },
    subtitle: {
      text: '根据分类算法，统计出微博情感倾向'
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