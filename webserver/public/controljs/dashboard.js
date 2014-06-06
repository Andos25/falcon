$(document).ready(function() {
  select_sexinfo();
  $("li#1").addClass('section');
  select_popinfo();
});

function select_popinfo() {
  $.getJSON("/ajax/dashboard_select_popinfo/", {
    "selectinfo": $("select#multiSelect2 option:selected").attr("name")
  }, function(data) {
    buildpopchart(data);
  })
}

function get_username() {
  $.getJSON("/ajax/user_name", {}, function(data) {
    return data;
  });
}

function buildpopchart(info) {
  $('#popinfo').highcharts({
    chart: {
      type: 'pie',
      options3d: {
        enabled: true,
        alpha: 45,
        beta: 0
      }
    },
    credits: {
      enabled: false
    },
    title: {
      text: '全国各省（市）用户比例'
    },
    tooltip: {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        depth: 35,
        dataLabels: {
          enabled: true,
          format: '{point.name}'
        }
      }
    },
    series: [{
      type: 'pie',
      name: '用户比例为',
      data: info
    }]
  });
}


function select_sexinfo() {
  $.getJSON("/ajax/dashboard_select_sexinfo/", {
    "selectinfo": $("select#multiSelect1 option:selected").attr("name")
  }, function(data) {
    buildsexchart(data);
  })
}

function buildsexchart(info) {
  $('#container').highcharts({
    chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false
    },
    title: {
      text: '各省用户性别比例'
    },
    tooltip: {
      formatter: function() {
        return '<b>' + this.point.name + '</b>: ' + Highcharts.numberFormat(this.percentage, 2) + ' %';
      }
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: false
        },
        showInLegend: true
      }
    },
    credits: {
      enabled: false
    },
    series: [{
      type: 'pie',
      name: '所占比例',
      data: info.percentage
    }]
  });
  categories = info.categories;
  $('#sex_detail').highcharts({
    chart: {
      type: 'bar'
    },
    credits: {
      enabled: false
    },
    title: {
      text: '各市（省）用户性别统计'
    },
    xAxis: [{
      categories: categories,
      reversed: false,
      labels: {
        step: 1
      }
    }, { // mirror axis on right side
      opposite: true,
      reversed: false,
      categories: categories,
      linkedTo: 0,
      labels: {
        step: 1
      }
    }],
    yAxis: {
      title: {
        text: null
      },
      labels: {
        formatter: function() {
          return (Math.abs(this.value) / 1000) + 'K';
        }
      },
    },

    plotOptions: {
      series: {
        stacking: 'normal'
      }
    },

    tooltip: {
      formatter: function() {
        return '<b>' + this.series.name + this.point.category + '</b><br/>' +
          'Population: ' + Highcharts.numberFormat(Math.abs(this.point.y), 0);
      }
    },

    series: [{
      name: 'Male',
      data: info.malelist
    }, {
      name: 'Female',
      data: info.femalelist
    }]
  });
};