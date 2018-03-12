$("#subscribe").click(function(){
    var email = $("#email").val();
    var from="subscribe";
    $.post("mymail.php",{mail:email}, function(data){
        alert(data);
    })
    
});