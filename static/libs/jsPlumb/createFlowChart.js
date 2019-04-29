			var params = getParams();

			var maxHeight = 0, maxWidth = 0;

			var idlist = [];

			//单击延迟
			var _delay = null;

			var tpid = '';
			if(typeof params.tpid != 'undefined') {
				tpid = params.tpid;
			}

			var color = '';
			if(typeof params.color != 'undefined') {
				color = params.color;
			}

			var lineStyle = '';
			if(typeof params.lineStyle != 'undefined') {
				lineStyle = params.lineStyle;
			}

			//创建拓扑节点
			var createAreas = function(opts) {

				if(color == '') {
					var bst = "font-size: 30px; border:1px solid black;";
				} else {
					var bst = "font-size: 30px; border:1px solid #00EEEE;";
				}

				var _obj = $('<div id="arreas_"' + opts.id + ' style="' + bst + '" class="window"><strong>' + opts.name + '</strong></div>').css({
//				var _obj = $('<div id="arreas_"' + opts.id + ' style="font-size: 30px; border:1px solid #F00; color: black; opacity:0.5; filter:alpha(Opacity=40);" class="window"><strong>' + opts.name + '</strong></div>').css({
			        position: 'absolute',
			        zIndex: '-10',
			        top: opts.top + 'px',
			        left: opts.left + 'px',
			        height: opts.height,
			        width: opts.width,
			        textAlign: 'left'
			    }).appendTo('#network');
			}

			//创建拓扑节点
			var CreateNodeElem = function(opts) {

			    //节点类型参数
			    var typeOpts = {
			    		start: {height: 97, width:75, bg: 'green'},
				        end: {height: 42, width:100, bg: 'blue'},
						normal: {height: 125, width:85, bg: ''},
				    };

                var node = typeOpts[opts.type];
                if(!node) {
                    node = {
                            height: '60px',
                            width: '180px',
                            bg: 'green'
                    };
                }

                //单击事件
                var sClick = function() {
                    // 取消上次延时未执行的方法
                    clearTimeout(_delay);
                };

                //双击事件
                var dClick = function() {
                    if(opts.href) {
                        window.open(opts.href);
                    } else {
                        if(opts.ntpid) {
                            window.location.href = getUrl() + "?tpid=" + opts.ntpid;
                        }
                    }
                };

                if("cld" == opts.type) {
                    var st = 'vertical-align:middle;text-align:center;height:' + node.height +'px;line-height:' + node.height + 'px; color:black;';
                } else {
                    var st = 'vertical-align:middle;text-align:center;height:' + node.height +'px;line-height:' + node.height + 'px;';
                }
                this.elem = $('<div id="' + opts.id + '_img" style="' + st +'">' + (opts.innerText || '') + '</div>').css({
                    position: 'absolute',
                    zIndex: '-1',
                    height: node.height,
                    width: node.width,
                    background: node.bg,
                    textAlign: 'center'
                });

                var _height = node.height + opts.top,
                    _width = node.width + opts.left;

                var _text = null;
                if(opts.text) {
                    _text = $('<div id="' + opts.id + '_text" style="white-space:nowrap;">' + opts.text + '<div id="' + opts.id + '_tra"></div></div>').css({
                        position: 'absolute',
                        zIndex: '9999',
                        top: node.height,
                        left: 0,
                        textAlign: 'left'
                    });
                    _height += _text.height();
                    _width += _text.width();
                }

                var _obj_h = node.height;
                var _obj_w = node.width;
                if(_text != null) {
                    _obj_h += _text.height();
                    if(_text.width() > _obj_w) _obj_w = _text.width();
                }
                var _obj = $('<div id="' + opts.id + '" class="window"></div>').css({
                    position: 'absolute',
                    zIndex: '9997',
                    top: opts.top,
                    left: opts.left,
                    height: _obj_h,
                    width: _obj_w,
                    textAlign: 'left'
                }).appendTo('#network');

                this.elem.appendTo('#' + opts.id);
                if (_text != null) {
                    _text.insertAfter(this.elem);
                }
                var obj = $('#' + opts.id);
                var _x, _y;

                //绑定点击事件
                obj.bind('dblclick', dClick);

                if(_height > maxHeight) maxHeight = _height;
                if(_width > maxWidth) maxWidth = _width;
			};

			jsPlumb.importDefaults({
				DragOptions : { cursor: "pointer", zIndex:2000 },
				HoverClass:"connector-hover"
			});

			var stateMachineConnector = {
				connector:"StateMachine",
				paintStyle:{lineWidth:3,strokeStyle:"#056"},
				hoverPaintStyle:{strokeStyle:"#dbe300"},
				endpoint:"Blank",
				anchor:"Continuous",
				overlays:[ ["PlainArrow", {location:1, width:15, length:12} ]]
			};

			var conn4Color = "rgba(46,164,26,0.8)";
			var connectorStrokeColor = "rgba(50, 50, 200, 1)",
				connectorHighlightStrokeColor = "rgba(180, 180, 200, 1)",
				hoverPaintStyle = { strokeStyle:"#7ec3d9" };


			var connArr = [] ;

			//创建互联
			var strokeLine = function() {
				var time = $('#DatePicker').val();
				var traffic = $('#traffic').prop("checked");
				var t = '';
				if(traffic) {
					t = true;
				}
			    $.post('../../../api/?action=network&method=getLines&tpid=' + tpid + '&time=' + time + '&traffic=' + t + '&color=' + color + '&lineStyle=' + lineStyle, function(data) {
					if(connArr.length) {
						for(var j in connArr) {
							jsPlumb.detach(connArr[j]);
						}
						connArr = [];
					}
			        var json = $.parseJSON(data);
					jsPlumb.setSuspendDrawing(true);
			        $.each(json.relate, function(i, n) {
						if (n && typeof document.getElementById(n[0]) != 'undefined' && typeof document.getElementById(n[1]) != 'undefined') {
							var conn = null;
							var color = '#00CD00';
							if(n[2] == 1) {
								color = "#00CD00";
							} else if(n[2] == 2) {
								color = "green";
							} else if(n[2] == 3) {
								color = "#FF8000";
							} else if(n[2] == 4) {
								color = "#FF0000";
							}
							try {
								conn = jsPlumb.connect({
									source: n[0],
									target: n[1],
									anchors: [n[3], n[4]],
									paintStyle: {
										lineWidth: n[9],
										strokeStyle: color
									},
									connector:"Straight",
									hoverPaintStyle: hoverPaintStyle,
									anchor: "AutoDefault",
									detachable: false,
									endpointStyle: {
										gradient: {
											stops: [[0, connectorStrokeColor], [1, connectorHighlightStrokeColor]],
											offset: 3,
											innerRadius: 2
										},
										radius: 0.5
									},
									overlays : [
										["Label", {
											cssClass:"l1 component label",
											label : n[5],
											location: n[7],
											id:"label",
											events:{
												"click":function(label, evt) {
													//var from = label.component.sourceId;
													//var to = label.component.targetId;
													//var port = label.label;
													//window.open('clist.html?from=' + from + '&to=' + to + '&label=' + port);
												}
											}
										}],
										["Label", {
											cssClass:"l1 component label",
											label : n[6],
											location: n[8],
											id:"label",
											events:{
												"click":function(label, evt) {
													//var from = label.component.sourceId;
													//var to = label.component.targetId;
													//var port = label.label;
													//window.open('clist.html?from=' + from + '&to=' + to + '&label=' + port);
												}
											}
										}]
//										,
//										["Arrow", {
//											location: n[8],
//											//direction: -1,
//											width: 12,
//											length: 12,
//											events:{
//												"click":function(arrow, evt) {
//													var from = arrow.component.sourceId;
//													var to = arrow.component.targetId;
//													var port = arrow.label;
//													window.open('clist.html?from=' + from + '&to=' + to);
//												}
//											}
//										}]
									]
								});
								connArr.push(conn);
							} catch(err) {

							}
						}
			        });
					jsPlumb.setSuspendDrawing(false, true);
			        $.each(json.traffic, function(i, n) {
			            $('#' + n.id + '_tra').html(n.text);
			        });
			    });
			    //定时刷新请求
			    setTimeout(strokeLine, 60000);
			};

            function connetc(lines) {

            }


			function createAllNode() {
				$.post('../../../api/?action=network&method=getNodes&tpid=' + tpid, function(data) {
			        var json = $.parseJSON(data);
			        $('#network').html('');

			        $.each(json.areas, function(i, n) {
			        	createAreas(n);
			        });

			        $.each(json.nodes, function(i, n) {
						idlist.push(n.id);
			            var opts = {
			                id: n.id,
			                ntpid: n.ntpid,
			                type: n.type,
			                innerText: n.innerText || '',
			                text: n.text || '',
			                href: n.href || '',
			                top: n.top,
			                left: n.left,
			                ports: n.ports
			            };
			            new CreateNodeElem(opts);
			        });
					jsPlumb.draggable(jsPlumb.getSelector(".window"), { containment:".topology"});
			        strokeLine();
			    });
			};
			createAllNode();
