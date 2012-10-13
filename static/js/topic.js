function  topicComments(that,id){
        
        var commentcontent = $("#t"+id).find("div.commentcontent");
        //清空内容
        commentcontent.find("div.comment").remove()

        //显示加载图片
        commentcontent.find("div.loading").show()
        //显示评论
        commentcontent.show()
        $.ajax({
            url:'/topic/loadcomment/'+id+'',
            type:'get',
            dateType:'text',
            timeout:10000,
            success:function(data,textStatus){
                //加载成功之后，去掉加载图片
                commentcontent.find("div.loading").hide();
                commentcontent.append(data)
                $("textarea").elastic()
            }
        })
}


$("div.newtopic input[type='submit']").click(function(){

   if(($("input[type='hidden'][name='subject_list']").length>=1 || $("input[type='hidden'][name='tag_list']").length>=1 )&& $("textarea[name='topic']").val().length>0){
     return true;
   }

   if($("textarea[name='topic']").val().length>0){
      alert("至少选择一个标签或主题");
   }

    return false;
})

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
})


$("textarea").elastic()

$("a.reply").live("click",function(){
    html="<label class='reply_to' >RT "
    html += "<a href='javascript:void(0)'>"
    html += $.trim($(this).siblings("a").text())
    html +=':</a><a class="remove"  href="javascript:void(0)"></a></label>'
    var textarea =$(this).parent("span").parent("div").parent("li").parent("ul").find("textarea")
    textarea.parent("li").siblings("label").remove()
    textarea.parent("li").before(html)
    textarea.siblings("input[name='to_user_id']").val($(this).siblings("input[name='user_id']").val())
    var id = $(this).siblings("input[name='id']").val()
    $.scrollTo("#"+id,1000,function(){});
})
  
$("a.remove").live("click",function(){
    $("input[name='to_user_id']").val("")
    $(this).parent('label').remove()
})



$("span.slideup a").click(function(){
    var comment =  $(this).parent("span").parent("div.commentcontent")
    comment.slideUp(700, function(){});
})


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
        para+=$(this).attr("name")+"="+encodeURIComponent($(this).val())+"&"
    })
  
    return para
}


function createElement(element){
    return document.createElement(element)
}


function validate(elem){
    if ($(elem).val()==""){
  
        // $. showEmptyWarningDialog("写点什么吧，回应是不能为空的",function(){

        //   })
        return false;
    }else{
        return true;
    }
}

function submitComment(formname){
    var form = $("form[name='"+formname+"']")
     
    if (!validate(form.find("textarea"))){
        return
    }
    var loading = form.parent("ul").find("div.loadingchange")
    loading.show()
    // form.find("input[type='button']").attr("disabled","disabled")
    $.ajax({
        url:'/topic/comment',
        type:'post',
        data:wrapdata(formname),
        dataType:'text',
        timeout:10000,
        success:function(data){
            loading.hide()
            // form.find("input[type='button']").removeAttr("disabled")
            form.after(data)
            document.getElementsByTagName("textarea")[0].value=''
            form.find("a.remove").trigger("click")
        },
        error:function(){
               
        }

    })
}