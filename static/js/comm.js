function getParams() { 
	var params = {};
	var url = location.href; 
	var start = url.indexOf("?") + 1;
	if (start == 0)
		return params;	
	var end = url.indexOf("#") == -1?url.length : url.indexOf("#");
	var queryString = url.substring(start, end);
	var paraString = queryString.split('&');
	var cur = "";
	for (var i=0; i < paraString.length; i++) { 
		cur = paraString[i];
		var pos = cur.indexOf("=");
		params[cur.substring(0, pos)] = urlDecode(cur.substring(pos + 1, cur.length)); 
	}
	return params;
}

function getUrl() { 
	var url = location.href; 
	var end = url.indexOf("?");
	if (end == 0) return url;	
	return url.substring(0, end);
}

function getUrlParams(url) { 
	var params = {};
	var start = url.indexOf("?") + 1;
	if (start == 0)
		return params;	
	var end = url.indexOf("#") == -1?url.length : url.indexOf("#");
	var queryString = url.substring(start, end);
	var paraString = queryString.split('&');
	var cur = "";
	for (var i=0; i < paraString.length; i++) { 
		cur = paraString[i];
		var pos = cur.indexOf("=");
		params[cur.substring(0, pos)] = urlDecode(cur.substring(pos + 1, cur.length)); 
	}
	return params;
}

function getUrlPath(url) { 
	var end = url.indexOf("?");
	if (end == 0) return url;	
	return url.substring(0, end);
}

function getDateStr3(date) {
    var year = "";
    var month = "";
    var day = "";
    var now = date;
    year = ""+now.getFullYear();
    if((now.getMonth()+1)<10){
        month = "0"+(now.getMonth()+1);
    }else{
        month = ""+(now.getMonth()+1);
    }
    if((now.getDate())<10){
        day = "0"+(now.getDate());
    }else{
        day = ""+(now.getDate());
    }
    return year+"-"+month+"-"+day;
}

function getWeekStartAndEnd(AddWeekCount) {
    //起止日期数组
    var startStop = new Array();
    //一天的毫秒数
    var millisecond = 1000 * 60 * 60 * 24;
    //获取当前时间
    var currentDate = new Date();
    //相对于当前日期AddWeekCount个周的日期
    currentDate = new Date(currentDate.getTime() + (millisecond * 7*AddWeekCount));
    //返回date是一周中的某一天
    var week = currentDate.getDay();
    //返回date是一个月中的某一天
    var month = currentDate.getDate();
    //减去的天数
    var minusDay = week != 0 ? week - 1 : 6;
    //获得当前周的第一天
    var currentWeekFirstDay = new Date(currentDate.getTime() - (millisecond * minusDay));
    //获得当前周的最后一天
     var currentWeekLastDay = new Date(currentWeekFirstDay.getTime() + (millisecond * 6));
    //添加至数组
    startStop.push(getDateStr3(currentWeekFirstDay));
    startStop.push(getDateStr3(currentWeekLastDay));

    return startStop;
}

Date.prototype.format = function(format){

	var o = { 
		"M+" : this.getMonth() + 1, //month 
		"d+" : this.getDate(), //day 
		"h+" : this.getHours(), //hour 
		"m+" : this.getMinutes(), //minute 
		"s+" : this.getSeconds(), //second 
		"q+" : Math.floor((this.getMonth() + 3)/3), //quarter 
		"S" : this.getMilliseconds() //millisecond 
	} 
	
	if(/(y+)/.test(format)) { 
		format = format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length)); 
	} 
	
	for(var k in o) { 
		if(new RegExp("("+ k +")").test(format)) { 
			format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length)); 
		} 
	} 
	return format; 
}

function urlDecode(zipStr){  
    var uzipStr = "";  
    for(var i = 0; i < zipStr.length; i++){  
        var chr = zipStr.charAt(i);  
        if(chr == "+"){  
            uzipStr += " ";  
        }else if(chr == "%"){  
            var asc = zipStr.substring(i+1, i+3);  
            if(parseInt("0x" + asc)>0x7f){  
                uzipStr += decodeURI("%" + asc.toString() + zipStr.substring(i + 3, i + 9).toString());  
                i += 8;  
            }else{  
                uzipStr += AsciiToString(parseInt("0x" + asc));  
                i += 2;  
            }  
        }else{  
            uzipStr += chr;  
        }  
    }  
    return uzipStr;  
}  
  
function StringToAscii(str){  
    return str.charCodeAt(0).toString(16);  
}  
function AsciiToString(asccode){  
    return String.fromCharCode(asccode);  
}

function getQueryString() { 
	var params = {};
	var url = location.href; 
	var start = url.indexOf("?") + 1;
	if (start == 0)
		return '';	
	var end = url.indexOf("#") == -1?url.length:url.indexOf("#");
	var queryString = url.substring(start, end); 
	return queryString;
}

var by = function(name, order){
    return function(o, p){
        var a, b;
        if (typeof o === "object" && typeof p === "object" && o && p) {
            a = o[name];
            b = p[name];
            if (a === b) {
                return 0;
            }
            if (typeof a === typeof b) {
				if (order == 'DESC' || order == 'desc') {
					return a < b ? 1 : -1;
				} else {
					return a < b ? -1 : 1;
				}
            }
			if (order == 'DESC' || order == 'desc') {
				return typeof a < typeof b ? 1 : -1;
			} else {
				return typeof a < typeof b ? -1 : 1;
			}
        }
        else {
            throw ("error");
        }
    }
}

function trim(value) {
    return value.replace(/(^\s*)|(\s*$)/g, "");
}
