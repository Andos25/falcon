$(document).ready(function() {
  get_cluster_graph();
});

function get_cluster_graph() {
  $.getJSON("/ajax/cluster_data/", {}, function(data) {
    buildcolumnchart(data);
  });
}

function buildcolumnchart(info) {
  $('#container').highcharts({
    chart: {
      type: 'column',
      margin: [50, 50, 100, 80]
    },
    credits: {
      enabled: false
    },
    title: {
      text: 'Topic cluster with k-means algorithm'
    },
    xAxis: {
      categories: info["categories"],
      labels: {
        rotation: 0,
        align: 'right',
        style: {
          fontSize: '13px',
          fontFamily: 'Verdana, sans-serif'
        }
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: 'microblogs '
      }
    },
    legend: {
      enabled: false
    },
    tooltip: {
      pointFormat: 'There are : <b>{point.y:.1f} blogs in this cluster</b>',
    },
    series: [{
      name: 'Population',
      data: info["data"],
      dataLabels: {
        enabled: false,
        rotation: -90,
        color: '#FFFFFF',
        align: 'right',
        x: 4,
        y: 10,
        style: {
          fontSize: '13px',
          fontFamily: 'Verdana, sans-serif',
          textShadow: '0 0 3px black'
        }
      }
    }]
  });
}