function vote() {
    let el = $(event.target);
    $.ajax({
        type: "POST",
        url: '/vote/',
        data: {
            'choice': el.attr('id'),
            'voting': el.parent().parent().attr('id')
        },
        //headers: {'X-CSRFToken', $('input[name="csrfmiddlewaretoken"]'},
        success: (data) => {
            console.log(data)
        },
    });
}