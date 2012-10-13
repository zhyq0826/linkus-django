$(document).ready(function(){

    $("div.answer").live("mouseover",function(){
        $(this).find("a.editanswer").show()
    })

    $("div.answer").live("mouseout",function(){
        $(this).find("a.editanswer").hide()
    });


    $("div.answer_dig a.dig_up").live("click",agree);
    $("div.answer_dig a.dig_down").live("click",oppose);


    $("input.action").click(addanswer)

    $("a.expand_diggers").live("click",function(){
        $(this).siblings("span.hide").show()
        $(this).remove()
    })
})

function agree(){
    var  that=$(this)
    var a_id=$(this).parent("div").parent("div").find("input[type='hidden']").val()
    if(that.hasClass("highlight_dig_a")){
        return;
    }
    if(a_id){
        $.ajax({
            url:'/answer/'+a_id+'/agree',
            type:'post',
            dataType:'text',
            timeout:10000,
            success:function(data){
                if(data==''){
                    return
                }

                var json = eval("("+data+")")
                if(json.status){
                    var user=null
                   if($("div.answer_diggers").find("a").length>1){
                     user = $("<a href='"+json.url+"' >"+json.name+"</a><span> 、</span>")
                   }else{
                     user = $("<a href='"+json.url+"' >"+json.name+"</a>")
                   }
                   
                   $("div.answer_diggers").find("span").first().html(""+json.agree_count+" 赞成 / "+json.oppose_count+"反对").after(user)
                   that.addClass("highlight_dig_a");
                   that.siblings("a.dig_down").removeClass("highlight_dig_a");

                }else{

                }
            },
            error:function(){
               
            }
        })
    }
}

function oppose(){
    var  that=$(this)
    var a_id=$(this).parent("div").parent("div").find("input[type='hidden']").val()
    if(that.hasClass("highlight_dig_a")){
        return;
    }
    if(a_id){
        $.ajax({
            url:'/answer/'+a_id+'/oppose',
            type:'post',
            dataType:'text',
            timeout:10000,
            success:function(data){
                if(data==''){
                    return
                }

                var json = eval("("+data+")")
                if(json.status){
                    //删除反对用户的信息
                    console.log(json.u_url)
                    $("div.answer_diggers").find("a[href='"+json.url+"']").remove();
                    $("div.answer_diggers").find("a[href='"+json.url+"']").next("span").remove();
                    $("div.answer_diggers").find("span").first().html(""+json.agree_count+" 赞成 / "+json.oppose_count+"反对");
                    that.addClass("highlight_dig_a");
                    that.siblings("a.dig_up").removeClass("highlight_dig_a")
                }else{

                }
            },
            error:function(){
              
            }
        })
    }
}
