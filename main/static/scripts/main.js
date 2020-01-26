function show_error(error) {
    console.log(error);
}

function render_in(url, selector, callback) {
    $.ajax({
        url: url,
        success: (data) => { $(selector).html(data); if(callback) callback();},
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
    render_in('/new_voting/', '.popups', ()=> $(".centered").addClass('show-top-anim'))
}

function isEmpty(obj) {
    return Object.entries(obj).length === 0
}

function last(obj) {
    return Object.keys(obj)[Object.keys(obj).length - 1]
}

function change_language(lang) {
    console.log(lang)
    $.ajax({
        type: "POST",
        url: '/change_language/',
        data: {'language': lang},
        success: (data) => {
            location.reload();
        },
    });
}
