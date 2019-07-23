$( document ).ready(function() {
    window.setInterval(function () {
        $.get('get_new_posts/' + $('.post-div').first().attr('id'))
        .done(function(data){
            $(".post-div").before(data);
        })
    }, 5000)
});