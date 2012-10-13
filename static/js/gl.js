
$(".user_info li").hover(function(){
                var ul = $(this).children("ul")
                if(ul){
                    ul.slideDown(100);
                }
            },function(){
                var ul = $(this).children("ul")
                if(ul){
                    ul.hide()
                }
});

$("a.follow").live("click",function(){
	var id = $(this).siblings("input[type='hidden']").val();
	that = $(this)
	if(id){
		if($(this).hasClass("followed"))
		{
			$.ajax({
				url:'/follow/'+id+'/no',
				type:'get',
				dataType:'text',
		        timeout:10000,
				success:function(data){
					that.removeClass("followed").html("关注TA");
				}
			})
			
		}else{
			$.ajax({
				url:'/follow/'+id+'/yes',
				type:'get',
				dataType:'text',
		        timeout:10000,
				success:function(data){
					that.addClass("followed").html("取消关注");
				}
			})
			
		}
	}

});

$(".gmenu li").click(function(){

	if($(this).hasClass("us")){

        $("div.u").hide();
		$(this).addClass("current_gmenu");
		$("div.usubject").slideDown(700);
		
		$(this).siblings("li").removeClass("current_gmenu");
	}
	if($(this).hasClass("uc")){
		$(this).addClass("current_gmenu");
		$("div.u").hide();
		$("div.ucolumn").slideDown(700);
		
		$(this).siblings("li").removeClass("current_gmenu");

	}

	if($(this).hasClass("ub")){
		$(this).addClass("current_gmenu");
		$("div.u").hide();
		$("div.ubook").slideDown(700);
		$(this).siblings("li").removeClass("current_gmenu");
	}
});
