
$("div.askform input[type='submit']").click(function(){

   if($("textarea[name='question']").val().length>0 && ( $("input[type='hidden'][name='subject_list']").length>=1 || $("input[type='hidden'][name='tag_list']").length>=1 )){
     return true;
   }

   if($("textarea[name='question']").val().length>0 ){

    alert("至少选择一个标签或主题");

   }
    return false;
});

$("a.subject").live("click",function(){

 var sdiv = $("div.sj");
 var subject = $(this).html();
 var id = $(this).attr("id");

 if($(this).hasClass("shighelight")){

   $(this).removeClass("shighelight");
   $("input[name='subject_list'][type='hidden'][value='"+id+"']").remove()

 }else{

   if(sdiv.find("a.shighelight").length<3)
   {
       $(this).addClass("shighelight");
       var input = $("<input/>").attr({
        name:'subject_list',
        value:id,
        type:'hidden'
       });
       $("form").append(input)

   }else{
    
   }
 }
});



function close_question(that,id){
    var state = $(that).attr('ref');
    var rurl='';
    var html = ''
    var newstate = ''
    if(id){
        if(state=='open'){
            rurl='/question/'+id+'/open';
            html='关闭问题';
            newstate='close';
        }else{
            rurl='/question/'+id+'/close';
            html='打开问题';
            newstate='open';
        }
        $.ajax({
            url:rurl,
            type:'get',
            dataType:'text',
            timeout:10000,
            success:function(data){
                
                if(data==''){
                    return 
                }

                var json=eval("("+data+")")
                if(json.status){
                    $(that).html(html);
                    $(that).attr('ref',newstate);
                    if(state=='close'){
                        //如果用户回答过问题了，说明form不存在
                        if(user_answer_state){
                            //tip 是存在的，直接修改tip
                            $("div.answered_tip").html("此问题不允许回答");
                        }else{
                            //否则说明用户没有回答过问题
                            editor.destroy();
                            $("form[name='answer_form']").hide();
                            $("div.ask").append("<div class='answered_tip' >此问题不允许回答</div>")
                        }
                    }else{
                        //用户回答过问题了,说明form不存在
                        if(user_answer_state){
                            //tip是存在的，直接修改tip
                            $("div.answered_tip").html("你已经回答过这个问题了,如果想继续回答，请修改你的答案");
                        }else{
                            editor = init_new_eidtor();
                            $("form[name='answer_form']").show();
                            editor.render("answer");
                        }
                        
                    }
                }
            },
            error:function(){
               
            }

        });
    }
}


function init_new_eidtor(){
   return new baidu.editor.ui.Editor({ 
        toolbars:[[
                'Bold', 'Italic', 'Underline','JustifyLeft', 'JustifyCenter', 'JustifyRight','Horizontal','Link','InsertOrderedList', 'InsertUnorderedList']],
        autoFloatEnabled:true,
        textarea : 'editorValue',
        initialStyle: 'body{font-size: 14px; font-family:Arial,Helvetica,sans-serif;font-weight:normal;color:#333333 !important;}',
        autoHeightEnabled:true,
        minFrameHeight:100,
        wordCount:false
    });
}

function wrapdata(formname){
    var para=''
    $("form[name='"+formname+"']  input").each(function(){
        if ($(this).attr("name")!='csrfmiddlewaretoken' && $(this).attr("type")!='button'){
            if ($(this).attr("type")=='radio'){
                if ($(this).attr('checked')){
                    para+=$(this).attr("name")+"="+$(this).val()+"&"
                }
            }else{
                para+=$(this).attr("name")+"="+$(this).val()+"&"
            }
        }
    })

    $("form[name='"+formname+"']  textarea").each(function(){
        para+=$(this).attr("name")+"="+$(this).val()+"&"
    })

    return para
}


function editanswer(that){

    if(editor){
        editor = new baidu.editor.ui.Editor({ 
            toolbars:[[
                    'Bold', 'Italic', 'Underline','JustifyLeft', 'JustifyCenter', 'JustifyRight','Horizontal','Link','InsertOrderedList', 'InsertUnorderedList']],
            autoFloatEnabled:true,
            textarea : 'editorValue',
            initialStyle: 'body{font-size: 14px; font-family:Arial,Helvetica,sans-serif;font-weight:normal;color:#333333 !important;}',
            autoHeightEnabled:true,
            minFrameHeight:100,
            wordCount:false
        });
    }else{

    }

    var oldanswer= $(that).parent("div.answer_action").parent("div.answer");
    var content=oldanswer.find("div.answer_content").html();
    var a_id =oldanswer.find("input[type='hidden']").val()

    var form = $("<form></form>").addClass("answer_form").attr({
        name:'answer_form',
        action:'',
        method:'post'
    });

    var divAnaser=$("<div></div>").addClass("answer").css({
        'padding-top':'30px',
        'position':'relative'
    }).appendTo(form);

    var divLoading=$("<div></div>").addClass("loading").appendTo(divAnaser);
    $("<img>").attr({
        src:'/static/image/ajax-loader.gif',
        width:'22',
        height:'22'
    }).appendTo(divLoading);

    $("<span>正在加载,请稍后...</span>").appendTo(divLoading);

    $("<textarea name='answer' id='answer' ></textarea><br>").appendTo(divAnaser)
    var wrapinput=$("<p></p>").attr("style","text-align:right;padding-right:10px").appendTo(divAnaser)

    $("<a href='#' >取消</a>").addClass("cancel").click(function(){
        editor.destroy();
        form.remove();
        oldanswer.show();
    }).appendTo(wrapinput)

    $("<input/>").attr({
        type:'hidden',
        name:'q_id',
        value:q_id
    }).appendTo(wrapinput);

    $("<input/>").addClass("action").attr({
        type:'button',
        value:'保存'
    }).click(function(){
        if (!validate()){
            return
        }
        para='a_id='+a_id+"&answer="+encodeURIComponent(editor.getContent())
        divLoading.show()
        $.ajax({
            url:'/answer/save',
            type:'post',
            data:para,
            dataType:'text',
            timeout:10000,
            success:function(data){
                if(data==''){
                    return 
                }
                divLoading.hide()
                form.before(data)
                editor.destroy()
                form.remove()
                oldanswer.remove()
            },
            error:function(){
               
            }

        })

    }).appendTo(wrapinput);



    oldanswer.hide()
    oldanswer.before(form)
    editor.render("answer")
    editor.setContent(content)

}



function validate(){
    if (editor.hasContents()){
        return true;
    }else{
        // $. showEmptyWarningDialog("提交的答案是不能为空的",function(){
    
        // })
        return false
    }
}





function addanswer(){
    var form = $("form[name='answer_form']")
    if (!validate()){
        return
    }
    var loading = $("div.loading")
    loading.show()
    // form.find("input[type='button']").attr("disabled","disabled")
    para=wrapdata('answer_form')
    para+='answer='+encodeURIComponent(editor.getContent())
    $.ajax({
        url:'/answer/add',
        type:'post',
        data:para,
        dataType:'text',
        timeout:10000,
        success:function(data){
            loading.hide()
            form.before(data)
            editor.destroy()
            form.remove()
            //说明用户对此问题进行了添加
            user_answer_state=true;
            $("<div>你已经回答过这个问题了,如果想继续回答，请修改你的答案</div>").addClass("answered_tip").appendTo("div.ask");
        },
        error:function(){
            
        }

    })
}