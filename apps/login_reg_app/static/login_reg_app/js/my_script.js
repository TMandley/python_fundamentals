function formValid(param1, param2){
    $(param1).keyup(function(){
        event.preventDefault();
        var data = $(this).serialize()
        var thing = this
        console.log(data)
        $.ajax({
            method: "GET",
            url: param2,
            data: data
        })
        .done(function(res){
            console.log(res)
            $("p").remove(".something");
            $(thing).after(res)
        })
    })
}

$(document).ready(function(){
    formValid('#email', "/regvalidate");
    formValid('#first_name', "/regfnvalidate");
    formValid('#last_name', "/reglnvalidate");
});

//seperated the function to use again... but couldnt quite do it without... wait.. I might have just figured it out
