document.addEventListener('DOMContentLoaded', function(){
    $('body').on('input', '#input', function(e){
        let len = $(e.target).val().length || $(e.target).html().length
        let counter = $(e.target).parent().children('.char-counter')
        counter.html(len.toString() + '/' + counter.html().split('/')[1])
    });
}, false);

choices = [];
choice_type = 0;

function add_new_choice() {
    if (!isEmpty(choices) && choices[last(choices)]['new']===true) return;
    let id = !isEmpty(choices) ? parseInt(last(choices))+1 : 0
    choices[id] = ({'new': true, 'finished': false});
    get_element('new_voting_choice', el => $(el).insertBefore('.add.choice').attr('id', id));
}

function done_choice_editing() {
    let element = $(event.target).parent();
    let text = element.children('.input').children('input').val();
    choices[element.attr('id')] = {'new': false, 'finished': true, 'text': text}
    get_element('voting_choice', el => {
        let new_el = $(el);
        element.replaceWith(new_el);
        new_el.children('p').text(text);
        new_el.attr('id', element.attr('id'));
    });
}

function delete_voting() {
    let element = $(event.target).parent();
    delete choices[element.attr('id')]
    element.remove()
}

function edit_voting() {
    let prev_element = $(event.target).parent();
    get_element('new_voting_choice', el => {
        choices[id]['finished'] = false
        let element = $(el);
        let id = prev_element.attr('id');
        prev_element.replaceWith(element);
        element.attr('id', id);
        let input = element.children('.input').children('input');
        input.val(choices[id]['text']);
        input.trigger('input');
    });
}

function close_voting_editing() {
    $('.centered').addClass('hide-top-anim');
    setTimeout(()=>$('.popups').html(''), 400)

}

function choice_type_change() {
    let el = $(event.target)
    let id = el.attr('id')
    if(id != choice_type) {
        $('.choice-variant').removeClass('active')
        el.addClass('active')
        choice_type = id
    }
}

function submit_voting() {
    for (const [ key, value ] of Object.entries(choices)) {
        if(!value["finished"]) {
            value['text'] = $('#'+key.toString()).children('.input').children('input').val()
        }
    }
    var http = new XMLHttpRequest();
    var url = '/new_voting/';
    http.open('POST', url, true);
    http.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val())
    http.onload  = function() {
       var data = JSON.parse(http.response);
       if('error' in data) $('.error-container').html(data['error']);
            else close_voting_editing();
    };
    var form_data = new FormData($('#image-loader')[0]);
    form_data.append('data', JSON.stringify({
                                    'title': $('.title-input').val(),
                                    'description': $('.desc-input').val(),
                                    'choices': choices.map(c => c['text']),
                                    'choice_type': choice_type
                                }))
    http.send(form_data);
}

function upload_file() {
    document.getElementById("image-selector").click();
}