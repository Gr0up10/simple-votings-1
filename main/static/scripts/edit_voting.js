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
    choices[id] = ({'new': true});
    get_element('new_voting_choice', el => $(el).insertBefore('.add.choice').attr('id', id));
}

function done_choice_editing() {
    let element = $(event.target).parent();
    let text = element.children('.input').children('input').val();
    choices[element.attr('id')] = {'new': false, 'text': text}
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
    $('.popups').html('')
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
console.log($('input[name="csrfmiddlewaretoken"]').val())
    $.ajax({
        type: "POST",
        url: "/new_voting/",
        data: {
            'data':JSON.stringify({
                'title': $('.title-input').val(),
                'description': $('.desc-input').html(),
                'choices': choices,
                'choice_type': choice_type
            }),
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){close_voting_editing()},
        failure: function(errMsg) {
            alert(errMsg);
        }
    });
}