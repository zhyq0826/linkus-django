$(document).ready(function(){
    $("div.first,div.second").mouseover(function(){
        $(this).children("ul").show();
    })
    $("div.first,div.second").mouseout(function(){
        $(this).children("ul").hide();
    })
    
    $("div.home li").live("mouseover",function(){
        $(this).addClass("current_li");
    });
    
    $("div.home li").live("mouseout",function(){
        $(this).removeClass("current_li");
    });
    
    $("div.home li").live("click",function(){
        var span = $(this).parent("ul").parent("div").children("span");

       
        var option = $(this).text();
        span.text(option);
        if(!isNaN(option)){
             var input = $(this).parent("ul").parent("div").children("input");
             input.val(option);
        }

        
        $(this).parent("ul").hide();           
    });

    //初始化    
})


function init(pid,cid){
    var content='';
    var cites = mycity[pid]
    if (cites){
        $.each(cites,function(index){
        content+="<li onclick=catch_area("+cites[index].id+")>"+cites[index].name+"</li>"
    })
    }
    $("#city_options").html(content)

    var areas = myarea[cid]
    var content='';
    if (areas){
        $.each(areas,function(index){
            content+="<li onclick=set_area("+areas[index].id+")>"+areas[index].name+"</li>"
        })
    }
    
    $("#area_options").html(content)
}



function catch_city(id){
    $("input[name='province']").val(id)
    $("#city_options").html("")
    $("#city_options").parent("div").children("span").html("---");
    $("#area_options").html("")
    $("#area_options").parent("div").children("span").html("---");
    var content='';
    var cites = mycity[id]
    if (cites){
        $.each(cites,function(index){
        content+="<li onclick=catch_area("+cites[index].id+")>"+cites[index].name+"</li>"
    })
    }
    $("#city_options").html(content)
}

function catch_area(id){
    $("input[name='city']").val(id)
    $("#area_options").html("")
    $("#area_options").parent("div").children("span").html("---");
    var areas = myarea[id]
    var content='';
    if (areas){
        $.each(areas,function(index){
            content+="<li onclick=set_area("+areas[index].id+")>"+areas[index].name+"</li>"
        })
    }
    
    $("#area_options").html(content)
}


function set_area(id){

    $("input[name='hometown']").val(id)
     
}


function wrapdata(formname){
     var para=''
    $("form[name='"+formname+"']  input").each(function(){
        if ($(this).attr("name")!='csrfmiddlewaretoken' && $(this).attr("type")!='button'){
            if ($(this).attr("type")=='radio'){
                if ($(this).attr('checked')){
                    para+=$(this).attr("name")+"="+encodeURIComponent($(this).val())+"&"
                }
            }else{
                para+=$(this).attr("name")+"="+encodeURIComponent($(this).val())+"&"
            }
        }
    })

    $("form[name='"+formname+"']  textarea").each(function(){
         para+=$(this).attr("name")+"="+encodeURIComponent($(this).val())+"&"
    })
    
    return para
}




function post_personl_data(){
    $.ajax({
        url:'/setting/profile/',
        data:wrapdata('person_form'),
        type:'post',
        timeout:10000,
        success:function(data){
            if(data==""){
                return
            }
           var json = eval("("+data+")")
              if(json.status){
                $("p.tip").remove()
                $("form").before("<p id='tip' class='tip' >保存成功</p>")
                 $.scrollTo('#tip',0,function(){});
              }else
              {
                 $("p.tip").remove()
                 $("form").before("<p id='tip' class='tip' >保存失败</p>")
                 $.scrollTo('#tip',0,function(){});
              }
        },
        error:function(XMLHttpRequest, textStatus, errorThrown){
            if(textStatus=='error'){
                $("p.tip").remove()
                 $("form").before("<p id='tip' class='tip' >保存失败</p>")
                 $.scrollTo('#tip',0,function(){}) 
            }
        }
    });
}

function post_school_data(){
    $.ajax({
        url:'/setting/school/',
        data:wrapdata('school_form'),
        type:'post',
        success:function(data){
            if(data==""){
                return
            }
           var json = eval("("+data+")")
              if(json.status){
                $("p.tip").remove()
                $("form").before("<p id='tip' class='tip' >保存成功</p>")
                 $.scrollTo('#tip',0,function(){});
              }else
              {
                 $("p.tip").remove()
                 $("form").before("<p id='tip' class='tip' >保存失败</p>")
                 $.scrollTo('#tip',0,function(){});
              }
        },
        error:function(XMLHttpRequest, textStatus, errorThrown){
            if(textStatus=='error'){
                $("p.tip").remove()
                 $("form").before("<p id='tip' class='tip' >保存失败</p>")
                 $.scrollTo('#tip',0,function(){}) 
            }
        }
    })
}


function  catch_college(id)
{
    $.ajax({
        url:'/setting/getcollege/'+id+'/',
        type:'get',
        success:function(data){
            $("div.university ul").html(data)
        }
    })
}

function catch_school(that,id){

    //设置学校
     $("input[name='college']").val(id).parent('div').children('a').text($(that).text())
     //初始化学院
     $("input[name='school']").val('').parent("div").children('span').text('---')
     $.fancybox.close()

     // $("input[name='college']")
     
      $.ajax({
        url:'/setting/getschool/'+id+'/',
        type:'get',
        success:function(data){
            $("#school_options").html(data);
        }
     });
 }


 function set_school(id){
    $("input[name='school']").val(id)
 }