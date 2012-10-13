var validate = validate||function(options,form){

    this.ignore = options.ignore ? options.ignore : 'hidden';
    this.requiredMsg=options.requiredMsg?options.requiredMsg:'此项必填';
    this.currentForm = form;
    this.eventType= options.eventType?options.eventType:'blur';
    this.emailMsg = options.emailMsg?options.eventType:'email格式不正确';
    this.nicknameMsg = options.nicknameMsg?options.nickname:'昵称不符合要求';
    this.rangeMsg = options.rangeMsg?options.rangeMsg:'长度不符合';
    this.invalidMsg = options.invalidMsg ? options.invalidMsg :'包含非法字符' ;

    this.allelements = $(this.currentForm).find("input, select, textarea").not(":submit, :reset, :image, [disabled]").not(this.ignore)

    that = this;

    $(this.currentForm).find(":submit").bind("click",function(){

        //在所有元素上触发验证
        $(that.allelements).trigger(that.eventType)

        if(that.validRegEmail()&&that.validRegNickname()&&that.validateRegPassword()){
            return true;
        }else{
            return false;
        }

       //console.log(that.validState)
      
    })

    $(this.currentForm).find(".required").bind(this.eventType,function(){

        if(!that.required($(this).val(),$(this)[0])){
            that.showError($(this),that.requiredMsg);
        }else{

           if( $(this).attr("name")=="email" ){
              if(!that.email($(this).val())){
                that.showError($(this),that.emailMsg)
              }
           }

           if( $(this).attr("name")=="password" ){
                if(!that.rangelength($(this).val(),$(this)[0],[6,16])){
                    that.showError($(this),that.rangeMsg); 
                }
           }


           if( $(this).attr("name")=="nickname" ){
               
              if(!that.rangelength($(this).val(),$(this)[0],[2,12])){
                  that.showError($(this),that.rangeMsg); 
              }else{
                    if(!that.nickname($(this).val())){
                        that.showError($(this),that.invalidMsg); 
                 }
              }
           }
        }
    })
}


validate.prototype.validRegEmail=function(){

   var email =  this.findByName("email")

   if(!that.required(email.val(),email[0]))
   {
     return false
   }

   if(!that.email(email.val())){

    return false
   }

    
   return true

}


validate.prototype.validRegNickname=function(){
   var nickname =  this.findByName("nickname")

 
   if(!that.required(nickname.val(),nickname[0]))
   {
       return false
   }

   if(!that.rangelength(nickname.val(),nickname[0],[2,12])){
        return false
   }

   if(!that.nickname(nickname.val())){
        return false
   }

   return true
}


validate.prototype.validateRegPassword=function(){
 var password =  this.findByName("password")

   if(!that.required(password.val(),password[0]))
   {
         return false
   }

   if(!that.rangelength(password.val(),password[0],[6,16])){
        return false
   }

   return true
}


validate.prototype.email=function(value){
    // contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
    return /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i.test(value);
}

validate.prototype.checkable=function(element){
    return /radio|checkbox/i.test(element.type);
}


validate.prototype.nickname=function(value){
    return /^[0-9a-zA-Z\u4e00-\u9fa5]{2,12}$/i.test(value);
}

validate.prototype.findByName=function(name){
    return $(this.currentForm).find("input[name="+name+"]");
}

validate.prototype.getLength=function(value,element){
    switch( element.nodeName.toLowerCase() ) {
        case 'select':
            return $("option:selected", element).length;
        case 'input':
            if( this.checkable(element) )
                return this.findByName(element.name).filter(':checked').length;
    }

    return value.length
}

validate.prototype.rangelength=function(value, element, param) {
    var length = this.getLength($.trim(value), element);
    return length >= param[0] && length <= param[1];
}

validate.prototype.showError=function(element,msg){
    //删除之前的错误消息
    $(element).siblings("p.error").remove()
    var p = $("<p>"+msg+"</p>").addClass("error");
    var span = $("<span></span>").addClass("arrow").appendTo(p)
    $(element).after(p)
}

validate.prototype.required=function(value,element){
     switch(element.nodeName.toLowerCase() ) {
            case 'select':
                // could be an array for select-multiple or a string, both are fine this way
                var val = $(element).val();
                return val && val.length > 0;
            case 'input':
                if ( this.checkable(element) )
                    return this.getLength(value, element) > 0;
            default:
                return $.trim(value).length > 0;
        }
}



$(document).ready(function(){
    var register_form = $("div.register_form").find("form");

if(register_form){

    
    register_form.find(":text").focus(function(){
        if($(this).attr("name")=="email"){
            $(this).siblings("p").remove()
            var tip=$("<span></span>").addClass("tip")
            tip.append("请使用正确的email");
            $(this).after(tip)
        }else if($(this).attr("name")=="nickname"){
            $(this).siblings("p").remove()
            var tip=$("<span></span>").addClass("tip")
            tip.html("2-12位，支持中文，数字，字母")
            $(this).after(tip)
        }
    }).blur(function(){
        $(this).siblings("span.tip").remove()
    })
    
    register_form.find(":password").focus(function(){
         $(this).siblings("p").remove()
        var tip=$("<span></span>").addClass("tip")
        tip.html("6-16位，支持字母，数字，符号");
        $(this).after(tip)
    }).blur(function(){
        $(this).siblings("span.tip").remove()
    })


    var validator = new validate({
        eventType:'blur'
    },register_form)
}

})
