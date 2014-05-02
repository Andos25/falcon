$(document).ready(function(){
    select_sexinfo();
    $("li#1").addClass('section');
    select_popinfo();
  })
  function select_popinfo(){
    $.getJSON("/ajax/dashboard_select_popinfo/", {"selectinfo":$("select#multiSelect2 option:selected").attr("name")}, function(data) {
      buildpopchart(data);
        }
    )}
  function buildpopchart(info){
    $('#popinfo').highcharts({
        chart: {
            type: 'pie',
            options3d: {
        enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: 'Browser market shares at a specific website, 2014'
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
            name: 'Browser share',
            data: info
        }]
    });
  } 


  function select_sexinfo(){
    $.getJSON("/ajax/dashboard_select_sexinfo/", {"selectinfo":$("select#multiSelect1 option:selected").attr("name")}, function(data) {
      buildsexchart(data);
        }
    )}
  function buildsexchart(info) {
    var chart;
    $('#container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: '安全事件类型比例统计'
        },
        tooltip:{
                formatter:function(){
                    return'<b>'+this.point.name+'</b>: '+Highcharts.numberFormat(this.percentage, 2)+' %';
                }
            },
        plotOptions:{
            pie:{
                allowPointSelect:true,
                cursor:'pointer',
                dataLabels:{
                    enabled:false
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
            data: info
        }]
    });
  };