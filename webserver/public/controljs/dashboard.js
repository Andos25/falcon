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
        credits: {
            enabled: false
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
    categories = ['0-4', '5-9', '10-14', '15-19',
            '20-24', '25-29', '30-34', '35-39', '40-44',
            '45-49', '50-54', '55-59', '60-64', '65-69',
            '70-74', '75-79', '80-84', '85-89', '90-94',
            '95-99', '100 +'];
    $('#sex_detail').highcharts({
            chart: {
                type: 'bar'
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'Population pyramid for Germany, midyear 2010'
            },
            subtitle: {
                text: 'Source: www.census.gov'
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
                    formatter: function(){
                        return (Math.abs(this.value) / 1000000) + 'M';
                    }
                },
                min: -4000000,
                max: 4000000
            },
    
            plotOptions: {
                series: {
                    stacking: 'normal'
                }
            },
    
            tooltip: {
                formatter: function(){
                    return '<b>'+ this.series.name +', age '+ this.point.category +'</b><br/>'+
                        'Population: '+ Highcharts.numberFormat(Math.abs(this.point.y), 0);
                }
            },
    
            series: [{
                name: 'Male',
                data: [-1746181, -1884428, -2089758, -2222362, -2537431, -2507081, -2443179,
                    -2664537, -3556505, -3680231, -3143062, -2721122, -2229181, -2227768,
                    -2176300, -1329968, -836804, -354784, -90569, -28367, -3878]
            }, {
                name: 'Female',
                data: [1656154, 1787564, 1981671, 2108575, 2403438, 2366003, 2301402, 2519874,
                    3360596, 3493473, 3050775, 2759560, 2304444, 2426504, 2568938, 1785638,
                    1447162, 1005011, 330870, 130632, 21208]
            }]
        });
  };