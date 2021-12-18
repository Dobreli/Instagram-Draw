var myModal = new bootstrap.Modal(document.getElementById('loginModal'), {})
myModal.show()

function check() {
    let check = document.getElementById("id_accountcontact").checked
    if (check == false) {
        document.getElementById("dmessage").style.visibility = "visible";
        document.getElementById("dmessage").style.color = "red";
        return false

    } else if (check == true) {
        return true
    }
}





$('.username-check').hide()
$('.email-check').hide()
$('.password-check').hide()
var usernamestatus = false

function checkusername() {
    let username = $('#id_username').val()
    let csrf = $("input[name=csrfmiddlewaretoken]").val();
    if (username != '') {
        $.ajax({
            url: '/user/register/check-username/',
            type: 'POST',
            data: {
                'username': username,
                'csrfmiddlewaretoken': csrf
            },
            success: function(data) {
                if (data.status == true) {
                    let html = `<small>"` + username + `" kullanılabilir.</small>`
                    $('.username-check').show()
                    $('#id_username').removeClass('is-invalid').addClass('is-valid')
                    $('.username-check').removeClass('alert-warning').addClass('alert-success')
                    $('.username-check').html(html)
                    usernamestatus = true

                } else {
                    var html = ''
                    if (data.no == 1) {
                        html = `<small>Bu ` + username + ` kullanıcı adı alınmış.</small>`
                    } else if (data.no == 2) {
                        html = `<small>Kullanıcı adı harflerden ve rakamlardan oluşmalıdır.</small>`
                    }
                    $('.username-check').show()
                    $('.username-check').removeClass('alert-success').addClass('alert-warning')
                    $('#id_username').removeClass('is-valid').addClass('is-invalid')
                    $('.username-check').html(html)

                    usernamestatus = false

                }
            }
        })
    }
}

$(document).on('submit', '#buyregister', function(event) {
    event.preventDefault();
    let username = $('#id_username').val()
    let email = $('#id_email').val()
    let password = $('#id_password').val()
    let repassword = $('#id_repassword').val()
    let csrf = $("input[name=csrfmiddlewaretoken]").val();
    if (check() == true) {
        $.ajax({
            url: '/user/register/member-register/',
            type: 'POST',
            data: {
                'username': username,
                'email': email,
                'password': password,
                'repassword': repassword,
                'link': window.location.href,
                'csrfmiddlewaretoken': csrf,
            },
            success: function(data) {
                if (data.status == true) {
                    location.reload();
                } else {
                    if (data.no == 1) {
                        var info = data.info
                        info = `<small>"` + info + `</small>`
                        $('#id_password').val('')
                        $('#id_repassword').val('')
                        $('.username-check').show()
                        $('.username-check').removeClass('alert-success').addClass('alert-warning')
                        $('.username-check').html(info)
                    } else if (data.no == 2) {
                        $('.username-check').hide()
                        $('#id_password').val('')
                        $('#id_repassword').val('')
                        var info = data.info
                        info = `<small>"` + info + `</small>`
                        $('.email-check').show()
                        $('.email-check').removeClass('alert-success').addClass('alert-warning')
                        $('.email-check').html(info)

                    } else if (data.no == 3) {
                        $('.email-check').hide()
                        var info = data.info
                        info = `<small>"` + info + `</small>`
                        $('.password-check').show()
                        $('#id_password').val('')
                        $('#id_repassword').val('')
                        $('#id_password').removeClass('is-valid').addClass('is-invalid')
                        $('#id_repassword').removeClass('is-valid').addClass('is-invalid')
                        $('.password-check').removeClass('alert-success').addClass('alert-warning')
                        $('.password-check').html(info)

                    } else if (data.no == 4) {
                        var info = data.info
                        info = `<small>"` + info + `</small>`
                        $('#id_password').val('')
                        $('#id_repassword').val('')
                        $('.username-check').show()
                        $('.username-check').removeClass('alert-success').addClass('alert-warning')
                        $('.username-check').html(info)

                    }
                    $('#id_password').val('')
                    $('#id_repassword').val('')
                }
            }
        })
    }


})

$('.login-alert').hide()
$(document).on('submit', '#buylogin', function(event) {
    event.preventDefault();
    let form = $('#buylogin');
    $.ajax({
        url: '/user/login/',
        type: 'POST',
        data: form.serialize(),
        success: function(data) {
            if (data.status == true) {
                console.log('Doğru')
                myModal.hide()
                location.reload();
            } else {
                $('.login-alert').show()
            }
        }
    })
})

$('#payment-transfer').click(function() {
    let csrf = $("input[name=csrfmiddlewaretoken]").val()
    var form_action = $('#payment-form-transfer').attr('action')
    let bankval = document.getElementById("bank-select").value;
    if (bankval == 0) {
        $('#transfer-alert').css({
            'display': 'block'
        })
        $('#transfer-alert').html('Lütfen havale/eft yapılacak bankayı seçiniz.')
    } else {
        let reference = $('#referenceno').val()
        if (reference.length > 0) {
            var check = $('#transfercontract').prop('checked')
            if (check == false) {
                $('#transfer-alert').css({
                    'display': 'block'
                })
                $('#transfer-alert').html('Mesafeli satış sözleşmesine onay vermediniz.')
            } else {
                $('#transfer-alert').css({
                    'display': 'none'
                })
                $.ajax({
                    url: form_action,
                    type: 'POST',
                    data: {
                        'type': 2,
                        'data': JSON.stringify({

                            'reference': reference,
                            'bank': bankval,

                        }),

                        'csrfmiddlewaretoken': csrf,
                    },
                    success: function(data) {
                        if (data.info == true) {
                            var paymentinfo = new bootstrap.Modal(document.getElementById('paymentinfo'), {})
                            paymentinfo.show()
                            setTimeout(() => {
                                paymentinfo.hide()
                            }, 1000);
                            let username = $('#navbarUserDropdown').text()
                            window.location.replace('/user/' + username + '/buy-processes/')
                        } else {

                        }
                    }
                })
            }
        } else {
            $('#transfer-alert').css({
                'display': 'block'
            })
            $('#transfer-alert').html('Havale işleminizin refarans numarasını girmediniz.')
        }
    }


})

$(document).on("submit", "#payment-form-credit", function(e) {
    event.preventDefault()
    $('#credit-alert').css({
        'display': 'none'
    })
    var check = $('#buycontract').prop('checked')
    let csrf = $("input[name=csrfmiddlewaretoken]").val()
    let form_action = $('#payment-form-credit').attr('action')
    if (check == true) {
        $.ajax({
            url: form_action,
            type: 'POST',
            data: {
                'type': 1,
                'data': JSON.stringify({
                    'user': $('#validuser').val(),
                    'cardno': $('#creditno').val(),
                    'date': $('#creditvalid').val(),
                    'cvv': $('#creditcv').val(),
                }),
                'csrfmiddlewaretoken': csrf,
            },
            success: function(data) {
                console.log(data.info)
            }
        })

    } else {
        $('#credit-alert').css({
            'display': 'block'
        })
    }
})


function addslash() {
    txt = $('#creditvalid').val()
    console.log(txt)
    var key = window.event.keyCode;
    if (txt.length == 2) {
        if (key != 8) {
            $('#creditvalid').val($('#creditvalid').val() + '/')
        }
    }
}