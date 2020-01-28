function show_error(error) {
    console.log(error);
}

function render_in(url, selector) {
    $.ajax({
        url: url,
        success: (data) => { $(selector).html(data);},
    });
}

function render_in_append(url, selector) {
    $.ajax({
        url: url,
        success: (data) => { $(selector).append(data);},
    });
}

function get_element(name, callback) {
    $.ajax({
        url: '/element/'+name,
        success: (data) => {callback(data)},
    });
}

function go_to_page(page) {
    location.href = page;
}

function login() {
    $.ajax({
        type: "POST",
        url: '/login/',
        data: $('#login-form').serialize(),
        success: (data) => {
            if(data['success']) go_to_page('/');
            else $('.error-container').html(data['error']);
        },
    });
}

function register() {
    $.ajax({
        type: "POST",
        url: '/register/',
        data: $('#register-form').serialize(),
        success: (data) => {
            console.log(data)
            if(data['success']) go_to_page('/');
            else $('.buttons').html(data['form']);
        },
    });
}

function show_registration() {
    render_in('/register/', '.buttons');
}

function show_login() {
    render_in('/login/', '.buttons');
}

function show_voting_creation() {
    render_in('/new_voting/', '.popups')
}

function isEmpty(obj) {
    return Object.entries(obj).length === 0
}

function last(obj) {
    return Object.keys(obj)[Object.keys(obj).length - 1]
}

function like(poll_id) {
    $.ajax({
        type:"POST",
        url: '/leavelike/',
        data: {
            'data': JSON.stringify({
                'poll_id': poll_id
            }),
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data){
            let al = document.createElement("div")
            if (data.created){
                al.classList.add("alert", "alert-primary")
                al.textContent = "Опрос сохранен!"
            } else {
                al.classList.add("alert", "alert-warning")
                al.textContent = "Опрос удален из сохраненных!"
            }
            document.getElementById(poll_id).appendChild(al)
            console.log(al)
            $(".alert").delay(2000).slideUp(100, function() {
                $(this).remove();
            });
        },
        failure: function(errMsg){console.log(errMsg)}
    })
}