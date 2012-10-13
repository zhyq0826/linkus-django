/* 
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

(function($,undefined){
    $.fn.complete=function(opt){
        return this.queue(function(){
            
            function init(){
                createComplete();
            }
           
            function createComplete(){
                
                /////////////////////////////////
                //构造标签holder
                /////////////////////////////////
               

               
               if(element.prevAll("ul.holder").length==0){
                  holder=$('<ul class="holder" ></ul>');
                  element.before(holder);
               }else{
                  holder = element.prev("ul.holder");
                  //console.log(element.prev("ul.holder"));
                  holder.find("span").click(function(){
                    $(this).parent("li").remove()
                  });
               }

                
                /////////////////////////////////
                //自动完成块
                /////////////////////////////////
                complete = $('<div class="auto_complete" ></div>');
                

                
                //加载数据的时，显示的文字
                // if (options.complete_text != "") {
                //     var completeText = options.complete_text;
                //     complete.append('<div class="default">' + completeText +  '</div>');
                // }
                
                complete.hover(function() {
                    complete_hover = 0;
                }, function() {
                    complete_hover = 1;
                });
                
                //数据源ul
                feed = $('<ul id="'+elemid+'_feed" ></ul>');
                element.after(complete.prepend(feed))
                
                //进行事件绑定
                elPrepare();
            }
            
           
            
            function elPrepare(){
                
                //数据缓存
                element.data('cache',{});
                
                //input绑定addItem事件
                element.bind("addItem", function(event,data){
                    addItem(data.key,data.value);
                });
                
                //input绑定focus事件
                element.focus(function(){
                    isactive=true;
                    if(maxItems()){
                        if(element.val().length>0){
                            var etext=xssPrevent(element.val(), 1);
                            complete.fadeIn("fast");
                            load_feed(etext);
                            complete.children(".default").hide();
                            feed.show();
                        }
                    }
                });

               
                
                element.blur(function(){
                    isactive=false;
                    if(complete_hover){
                        complete.fadeOut("fast")
                    }else{
                        element.focus();
                    }
                });

                
                element.keyup(function(event){
                    var etext=xssPrevent(element.val(), 1);
                    
                    //退格键，且输入的字符长度为0，不处理
                    if(event.keyCode==_key.backspace && etext.length==0){
                        return false;
                    }
                    
                    if (event.keyCode != _key.downarrow && event.keyCode != _key.uparrow && event.keyCode!= _key.leftarrow && event.keyCode!= _key.rightarrow && etext.length > options.input_min_size) {
                        
                        load_feed(etext);
                        complete.children(".default").hide();
                        feed.show();
                    }
                });
            }
            
            function addItem(key,value,preadded,added){
                var liclass="bit_box"
                var id=key;
                var txt = document.createTextNode(xssDisplay(value));
                var input=null;
                var label = null;

                //新添加的标签
                if(added){
                   input = $('<input type="hidden" name="tag_list"/>').attr('value', '-'+key);
                   label = $('<label></label>').prepend(key);
                }else{
                   input = $('<input type="hidden" name="tag_list"/>').attr('value', key);
                   label = $('<label></label>').prepend(txt);
                }
                var span = $('<span></span>');
                var li = $('<li class="'+liclass+'"  id="pt_'+id+'"></li>').prepend(span).append(label).append(input);
                
                span.click(function(){
                    $(this).parent("li").remove();
                    return false;
                });
               
                holder.append(li);
            }
            
            function addMembers(etext,data){
                feed.html('');
                //清除缓存
                if(!options.cache && data !=null){
                    cache.clear()
                }
                
              
                
                //数据加入cache
                if(data !=null && data.length){
                    $.each(data,function(i,val){
                        cache.set(xssPrevent(val.key), xssPrevent(val.value));
                    });
                }

                //加入用户输入的
                addTextItem(etext);

                var maximum = options.maxshownitems < cache.length() ? options.maxshownitems: cache.length();
                var content=''
                $.each(cache.search(etext),function(i,object){
                    if(maximum){
                        content += '<li rel="' + object.key + '">' + xssDisplay(itemIllumination(object.value, etext)) + '</li>';
                        counter++;
                        maximum--;
                    }
                });
                
                feed.append(content);
        
                if (maxItems() && complete.is(':hidden')) {
                    complete.show();
                }
            }
            
            function bindFeedEvent(){
                feed.children("li").mouseover(function(){
                    feed.children("li").removeClass("auto_focus");
                    focuson = $(this);
                    focuson.addClass("auto_focus");
                   
                });
                
                feed.children("li").mouseout(function(){
                    $(this).removeClass("auto_focus");
                    focuson = null;
                });
            }
            
            function removeFeedEvent() {
                feed.unbind("mouseover").unbind("mouseout").mousemove( function() {
                    bindFeedEvent();
                    feed.unbind("mousemove");
                });
            }
            
            function bindEvents(){
                bindFeedEvent();
                
                feed.children("li").unbind("mousedown").mousedown(function(e){
                    var option = $(this)
                    var added=0
                    if($(this).hasClass("new_tag_added")){
                        added=1
                    }
                    addItem(option.attr("rel"),option.text(),0,added);
                    _preventDefault(e);
                    element.val('');
                    complete.hide("fast");
                });
                
                element.unbind("keydown");
                element.keydown(function(event){
                    
                    //回车事件
                    if ((event.keyCode == _key.enter || event.keyCode == _key.tab || event.keyCode == _key.comma) && checkFocusOn()) {
                        var added=0
                        if(focuson.hasClass("new_tag_added")){
                            added=1
                        }
                        var option = focuson;
                        addItem(option.attr("rel"),option.text(), 0,added);
                        _preventDefault(event);
                        element.val('');
                        complete.fadeOut("fast")
                        return false
                    }
                    
                    //上下 键
                    if (event.keyCode == _key.downarrow) {
                        nextItem('first');
                    }
                    if (event.keyCode == _key.uparrow) {
                        nextItem('last');
                    }
                });
               
                
            }
            
            function nextItem(position) {
                removeFeedEvent();
                if (focuson == null || focuson.length == 0) {
                    if(position=='first'){
                        focuson = feed.children("li").first()
                    }else{
                        focuson = feed.children("li").last()
                    }
                    
                } else {
                    focuson.removeClass("auto_focus");

                    focuson = position == 'first' ? focuson.next("li") : focuson.prev("li");

                    if(!focuson.html()){
                        focuson = position=='first'?feed.children("li").first():feed.children("li").last();
                    }

                }
                feed.children("li").removeClass("auto_focus");
                focuson.addClass("auto_focus");
            }
            
            function checkFocusOn() {
                if (focuson == null || focuson.length == 0) {
                    return false;
                }
                return true;
            }
            
            function _preventDefault(event) {
                
                //防止点击li的出现跳动的现象
                element[0].onbeforedeactivate = function () {
                    window.event.returnValue = false;
                    element[0].onbeforedeactivate = null;
                };
                
                complete.hide();
                event.preventDefault();
                focuson = null;
                return false;
            }
            
            
            function itemIllumination(text, etext) {
                var string_regex_adder = options.filter_begin ? '': '(.*)';
                var regex_result = options.filter_begin ? '<em>$1</em>$2' : '$1<em>$2</em>$3';
                var string_regex = string_regex_adder + (options.filter_case ? "(" + etext + ")(.*)" : "(" + etext.toLowerCase() + ")(.*)");
                try {
                    var regex = new RegExp(string_regex, ((options.filter_case) ? "g":"gi"));
                    var text = text.replace(regex, regex_result);
                } catch(ex) {};
                return text;
            }
            
            function addTextItem(value){
                if(options.newel && maxItems()){
                    feed.children("li[fckb=1]").remove();
                    if(value.length==0){
                        return;
                    }

                    var li=null;

                    if(!cache.exist(value)){
                        var li = $('<li fckb="1" class="new_tag_added"  rel="'+value+'" ></li>').html('添加&nbsp;'+xssDisplay(value)+'&nbsp;标签');
                        feed.prepend(li);
                        counter++;
                    }else{

                    }
                }
            }
            
            
            function maxItems() {
                return options.maxitems != 0 && (holder.children("li.bit_box").length < options.maxitems);
            }
            
            
            function xssDisplay(string, flag) {
                string = string.toString();
                string = string.replace('\\', "");
                if (typeof flag != "undefined") {
                    return string;
                }
                return unescape(string);
            }
            
            function xssPrevent(string, flag) {
                string = String(string)
                if (typeof flag != "undefined") {
                    for(i = 0; i < string.length; i++) {
                        var charcode = string.charCodeAt(i);
                        if ((_key.exclamation <= charcode && charcode <= _key.slash) ||
                            (_key.colon <= charcode && charcode <= _key.at) ||
                            (_key.squarebricket_left <= charcode && charcode <= _key.apostrof)) {
                            string = string.replace(string[i], escape(string[i]));
                        }
                    }
                    string = string.replace(/(\{|\}|\*)/i, "\\$1");
                }
                return string.replace(/script(.*)/g, "");
            }
            
            function load_feed(etext){
                if(options.json_url && maxItems()){
                    
                    if(options.cache && json_cache_object.get(etext))
                    {
                        addMembers(etext);
                        bindEvents();     
                    }else
                    {
                        setTimeout(function(){
                            $.getJSON(options.json_url, {
                                "q":xssDisplay(etext)
                            }, function(data){
                                if(!isactive)return;
                                addMembers(etext,data)
                                json_cache_object.set(etext, 1);
                                bindEvents();
                            });
                        },options.delay);
                    }
                }else{
                    addMembers(etext);
                    bindEvents();
                }
            }
            
            
      
            
            var options = $.extend({
                json_url: null,
                width: 512,
                cache: true,
                height: "10",
                newel: true,
                addontab: false,
                addoncomma: false,
                firstselected: false,
                filter_case: false,
                filter_selected: false,
                filter_begin: false,
                complete_text: "正在搜索...",
                select_all_text:  null,
                maxshownitems: 15,
                maxitems: 6,
                oncreate: null,
                onselect: null,
                onremove: null,
                attachto: null,
                delay: 1000,
                input_tabindex: 0,
                input_min_size: 0,
                input_name: "",
                bricket: true
            },
            opt);
            
            //system variables
            var holder = null
            var feed = null;
            var complete = null;
            var counter = 0;
            
            
            var isactive = false;
            var focuson = null;
            var deleting = 0;
            var complete_hover = 1;
            
           
            var element = $(this);
            var elemid = element.attr("id");
            
            var json_cache_object = {
                'set': function (id, val) {
                    var data = element.data("jsoncache");
                    data[id] = val;
                    element.data("jsoncache", data);
                },
                'get': function(id) {
                    return element.data("jsoncache")[id] != 'undefined' ? element.data("jsoncache")[id] : null;
                },
                'init' : function () {
                    element.data("jsoncache", {});
                }
            };
            
            var randomId = function() {
                var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
                var randomstring = '';
                for (var i = 0; i < 32; i++) {
                    var rnum = Math.floor(Math.random() * chars.length);
                    randomstring += chars.substring(rnum, rnum + 1);
                }
                return randomstring;
            };
            
            var cache = {
                'search': function (text, callback) {
                    var temp = new Array();
                    var regex = new RegExp((options.filter_begin ? '^' : '') + text, (options.filter_case ? "g": "gi"));
                    $.each(element.data("cache"), function (i, _elem) {
                        if (typeof _elem.search === 'function') {
                            if (_elem.search(regex) != -1) {
                                temp.push({
                                    'key': i, 
                                    'value': _elem
                                });
                            }
                        }
                    });
                    return temp;
                },
                'exist':function(text){
                    var e = false;
                    $.each(element.data("cache"),function(i,_elem){
                        if(text==_elem){
                           e=true;
                           return false;
                        }
                        
                    });

                    if(e){
                        return true;
                    }else{
                        return false;
                    }

                    
                },
                'set': function (id, val) {
                    var data = element.data("cache");
                    data[id] = val;
                    element.data("cache", data);
                },
                'get': function(id) {
                    return element.data("cache")[id] != 'undefined' ? element.data("cache")[id] : null;
                },
                'clear': function() {
                    element.data("cache", {});
                },
                'length': function() {
                    if ( typeof(element.data('cache')) == "object") {
                        var _length = 0;
                        for (i in element.data('cache')) {
                            _length++;
                        }
                        return _length;
                    } else {
                        return element.data("cache").length;
                    }
                },
                'init': function () {
                    if (element.data("cache") == 'undefined') {
                        element.data("cache", {});
                    }
                }
            };
            
            var _key={
                'enter': 13,
                'tab': 9,
                'comma': 188,
                'backspace': 8,
                'leftarrow': 37,
                'uparrow': 38,
                'rightarrow': 39,
                'downarrow': 40,
                'exclamation': 33,
                'slash': 47,
                'colon': 58,
                'at': 64,
                'squarebricket_left': 91,
                'apostrof': 96
            }
            
            //initialization
            init();
      
            //cache initialization
            json_cache_object.init();
            cache.init();
            
            return this;
        });
    };
}
)(jQuery)


$("input[name='tagtext']").complete({
    json_url:'/tag/'
});



