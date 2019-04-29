function addLineBarChart(data, myChart) {
    //data.xAxis['splitNumber'] = 9;
    var option = {
        //color: data.color,
        title: {
            x: 'center',
            text: data.title
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                animation: false
            }
        },
        //grid: {
        //    x: 60,
        //    x2: 20,
        //    y: 40,
        //    y2: 70
        //},
        legend: data.legend,
        xAxis: data.xAxis,
        yAxis : [
            {
                type : 'value',
                splitNumber: 9,
                axisLabel : {
                    formatter: function (v) {
                        //if(v >= 1000*1000*1000) {
                        //    return (v / (1000*1000*1000)) + 'B'
                        //} else
                        if(v >= 10000*10000*10) {
                            return (v/(10000*10000*10)) + 'B'
                        } else if(v >= 1000*1000) {
                            return (v/(1000*1000)) + 'M'
                        }  else if(v >= 1000) {
                            return (v/(1000)) + 'K'
                        }
                        return v
                    }
                },
                axisTick:{
                    inside:true
                }
            }
        ],
        series: data.series
    };
    if(data.yAxis) {
        option.yAxis = data.yAxis;
    }
    if(data.grid) {
        option.grid = data.grid;
    }
    if(data.color) {
        option.color = data.color;
    }
    myChart.setOption(option);
}

function addLineBarTimeChart(data, myChart) {
    data.xAxis['splitNumber'] = 9;
    var option = {
        //color: data.color,
        title: {
            x: 'center',
            text: data.title
        },
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                var date = new Date(params[0].value[0]).format('yyyy-MM-dd hh:mm:ss')
                res = ["时间:" + date]
                for(var i in params) {
                    var param = params[i];
                    var units = "";
                    if(typeof param.data.units != "undefined") {
                        units = param.data.units;
                    }
                    res.push(param.seriesName + ' : ' + param.value[1] + " " + units)
                }
                return res.join("<br/>");
            },
            axisPointer: {
                animation: false
            }
        },
        //tooltip : {
        //    trigger: 'axis'
        //},
        //toolbox: {
        //    show : true,
        //    feature : {
        //        mark : {show: true},
        //        dataView : {show: true, readOnly: false},
        //        magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
        //        restore : {show: true},
        //        saveAsImage : {show: true}
        //    }
        //},
        legend: data.legend,
        xAxis: data.xAxis,
        //yAxis: {
        //    type: 'value',
        //    splitNumber: 7,
        //    axisTick:{
        //        inside:true
        //    }
        //},
        yAxis : [
            {
                type : 'value',
                splitNumber: 9,
                axisLabel : {
                    formatter: function (v) {
                        //if(v >= 1000*1000*1000) {
                        //    return (v / (1000*1000*1000)) + 'B'
                        //} else
                        if(v >= 10000*10000*10) {
                            return (v/(10000*10000*10)) + 'B'
                        } else if(v >= 1000*1000) {
                            return (v/(1000*1000)) + 'M'
                        }  else if(v >= 1000) {
                            return (v/(1000)) + 'K'
                        }
                        return v
                    }
                },
                axisTick:{
                    inside:true
                }
            }
        ],
        series: data.series
    };
    if(data.yAxis) {
        option.yAxis = data.yAxis;
    }
    if(data.grid) {
        option.grid = data.grid;
    }
    if(data.color) {
        option.color = data.color;
    }
    myChart.setOption(option);
}

function addBarChart(data, myChart) {
    var option = {
        title: {
            x: 'center',
            text: data.title
        },
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                var date = new Date(params[0].value[0]).format('yyyy-MM-dd hh:mm:ss')
                res = ["时间:" + date]
                for(var i in params) {
                    var param = params[i];
                    res.push(param.seriesName + ' : ' + param.value[1])
                }
                return res.join("<br/>");
            },
            axisPointer: {
                animation: false
            }
        },
        grid: {
            x: 60,
            x2: 60,
            y: '60',
            y2: '30'
        },
        legend: data.legend,
        xAxis: data.xAxis,
        yAxis: {
            type: 'value',
            axisTick:{
                inside:true
            }
        },
        series: data.series
    };
    if(data.color) {
        option.color = data.color;
    }
    myChart.setOption(option);
}

function addPieChart(data, myChart) {
    var option = {
        color: data.color,
        title : {
            text: data.title,
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: data.legend,
        series : data.series
    };
    if(data.color) {
        option.color = data.color;
    }
    if(data.grid) {
        option.grid = data.grid;
    }
    myChart.setOption(option);
}

function addStatusChart(data, myChart) {
    var option = {
        title: {
            text: data.title,
            x: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: function(params, ticket, callback) {
                var sc = params.value[2];
                var ch = params.value[3];
                var r;
                if(sc == 1){
                    r = '正常';
                } else {
                    r = '异常'
                }
                return ch + '<br/>状态:' + r + '<br>';
            },
            axisPointer: {
                show: false,
                type: 'shadow' //shadow  cross line
            },
            backgroundColor: 'rgba(245, 245, 245, 0.8)',
            borderWidth: 1,
            borderColor: '#ccc',
            padding: 10,
            textStyle: {
                color: '#000'
            },
            /*position: function(pos, params, el, elRect, size) {
                var obj = {
                    top: 10
                };
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            },*/
            //extraCssText: 'width: 170px'
        },
        animation: true,
        grid: {
            //height: '50%',
            y: '55',
            y2: '40',
            x: '20',
            x2: '20'
        },
        xAxis: {
            type: 'category',
            data: data.xAxis.data,
            position: 'top',
            splitArea: {
                show: false
            },
            axisTick:{
                inside:false
            }
        },
        yAxis: {
            inverse: true,
            type: 'category',
            data: data.yAxis.data,
            splitArea: {
                show: false
            },
            axisTick:{
                inside:false
            }
        },
        grid: {
            x: 15,
            x2: 15,
            y: 30,
            y2: 15
        },
        legend: {
            orient: 'vertical',
            x:'left',
            data:['正常','异常'],
            textStyle: {
                "color": "#fff"
            }
        },
        visualMap: {
            type: 'piecewise',
            splitNumber: 2,
            pieces: [
                {
                    min: 0,
                    max: 0,
                    color:'rgba(255,51,51,0.7)',//红色 一定要带透明度,否则背景的网格看不出来
                },// 不指定 min，表示 min 为无限大（-Infinity）。
               {
                    min: 1,
                    max: 1,
                    color:'rgba(102,153,102,0.4)',
                }// 不指定 min，表示 min 为无限大（-Infinity）。
            ],
            dimension: 2,
            align: 'left',
            show: true,
            orient: 'horizontal', //'vertical'  horizontal
            left: 'right', //center
            top: 'top',
            bottom: '15%'
        },
        series: [{
            name: 'channel',
            type: 'heatmap',
            data: data.series[0].data,
            label: {
                normal: {
                    show: true,
                    formatter: function(v) {
                        return v.value[3] ;
                    }
                }
            }
        }]
    };

    myChart.setOption(option);


    myChart.on("click", function (param) {
        var seriesName = param.seriesName;
        var name = param.name;
        window.open(param.value[4])
    });
}