$( document ).ready(function () {
    // using jQuery
    // https://docs.djangoproject.com/en/1.10/ref/csrf/
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).on("click", '.comment', function(evt) {
        evt.preventDefault();
        $(event.target).parent().find(".error_text").remove();
        if ($(evt.target).parent().parent().find("textarea").length !== 0) {
            return;
        }
        form_html = "<br><textarea class=\"form-control\" rows=\"3\" placeholder=\"42 characters or less\" required autofocus></textarea><br>\n" +
            "<button class=\"btn btn-sm btn-primary comment-btn\">Submit</button>\n";
        $(evt.target).after(form_html);
        $(".comment-btn").on('click', function(evt){
            evt.preventDefault();
            var pid = $(evt.target).parent().parent().attr('id');
            var textarea = $(evt.target).parent().find("textarea");
            var content = textarea.val();
            console.log(content);
            $.post("comment/" + pid, {'text':content})
                .done(function(data) {
                    $(evt.target).parent().append(data);
                    var err_msg = $(evt.target).parent().find(".error_text");
                    err_msg.remove();
                    $(evt.target).parent().find('.comment').after(err_msg);
                    textarea.remove();
                    $(evt.target).parent().find('br').remove();
                    $(evt.target).remove();
                });
        });
    })

});

