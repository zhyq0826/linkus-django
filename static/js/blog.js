//博客主题和标签
$("div.new_article input[type='submit']").click(function(){

   if(editor.hasContents() && $("input[name='title']").val().length>0){
     return true;
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


//博客评论
$("div.comment_action span:first a:first").click(function(){
    $("div.comment").slideUp(700, function(){})
    $(this).css("display","none");
    $(this).siblings("a").css("display","block");

})
$("div.comment_action span:first a:first").siblings("a").click(function(){
    $("div.comment").slideDown(700, function(){})
    $(this).css("display","none");
    $(this).siblings("a").css("display","block");
})

$("a.reply").live("click",function(){
    html="<label class='reply_to' >RT "
    html += "<a href='javascript:void(0)'>"
    html += $.trim($(this).siblings("a").text())
    html +=':</a><a class="remove"  href="javascript:void(0)"></a></label>'
    $("div.comment textarea").parent("li").siblings("label").remove()
    $("div.comment textarea").parent("li").before(html)
    $("input[name='to_user_id']").val($(this).siblings("input[type='hidden']").val())
    $.scrollTo('#commentform',1000,function(){});
})

$("a.remove").live("click",function(){
    $("input[name='to_user_id']").val("")
    $(this).parent('label').remove()
})


$("div.comment textarea").elastic()
$("div.comment input[type='button'][name='addcomment']").click(submitComment)



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
  // $. showEmptyWarningDialog("写点什么吧，评论是不能为空的",function(){

  //   })
      return false;
}else{
    return true;
}
}

function submitComment(){

   if (!validate($("form").find("textarea"))){
      return
   }

    $.ajax({
        url:'/blog/comment',
        type:'post',
        data:wrapdata("commentform"),
        dataType:'text',
        timeout:10000,
        success:function(data){
              $("form").before(data).fadeIn("normal")
              document.getElementsByTagName("textarea")[0].value=''
              $("a.remove").trigger("click")
            
        },
        error:function(){
             
        }

    })
}