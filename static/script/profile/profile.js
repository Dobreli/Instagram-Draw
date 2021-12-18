var username = $('.username').text()
var csrf = $("input[name=csrfmiddlewaretoken]").val();
$('#alert-profile').hide()

function get() {
    var mname = $('#firstname').val()
    var mlname = $('#lastname').val()
    let user = { 'name': mname, 'lname': mlname }
    return user
}
mname = get()
$('#update-open').click(function() {
    var name = $('#firstname').val()
    var lname = $('#lastname').val()

    if (mname['name'] != name || mname['lname'] != lname) {

        $.ajax({
            url: '/user/' + username + '/profile/',
            type: 'post',
            data: {
                'username': username,
                'first_name': name,
                'last_name': lname,
                'csrfmiddlewaretoken': csrf,
            },
            success: function(data) {
                $('#alert-profile').show()
                if (data.info == true) {
                    $('#alert-profile').removeClass('alert-warning').addClass('alert-success')
                    $('#alert-profile-text').text('Bilgileriniz Güncellendi')
                    $('#firstname').val(name)
                    $('#lastname').val(lname)
                    mname = get()
                } else {
                    $('#alert-profile-text').text('EROR 500! Lütfen, daha sonra tekrar deneyiniz!')
                    $('#alert-profile').removeClass('alert-success').addClass('alert-warning')
                }
            }
        });
    } else {
        $('#alert-profile').show()
        $('#alert-profile').removeClass('alert-success').addClass('alert-warning')
        $('#alert-profile-text').text('Girilen "Ad" ve "Soyad" bilgileri eskisi ile aynı.')
    }
})
$('.changemail-alert').hide()

var csrf = $("input[name=csrfmiddlewaretoken]").val();
$(document).on("submit", "#form-change-mail", function(e) {
    $('.changemail-alert').show()
    e.preventDefault()
    let form_action = $('#form-change-mail').attr('action')
    $.ajax({
        url: form_action,
        type: 'POST',
        data: {
            'password': $('#checkpassword').val(),
            'email': $('#changemail').val(),
            'csrfmiddlewaretoken': csrf,
        },
        success: function(data) {
            if (data.info == false) {
                if (data.danger == 1) {

                    $('.changemail-alert').html('Parolanızı yanlış girdiniz.')
                    $('.changemail-alert').addClass('alert-warning').removeClass('alert-succress')

                } else if (data.danger == 2) {
                    $('.changemail-alert').html('Bu email ile bir kayıt bulunmakta.')
                    $('.changemail-alert').addClass('alert-warning').removeClass('alert-succress')
                }
            } else {
                $('.changemail-alert').html('Yeni mail adresiniz kayıt edildi.')
                $('.changemail-alert').addClass('alert-success').removeClass('alert-warning')
                $('#mainmail').text($('#changemail').val())
                setTimeout(() => {
                    $('.changemail-alert').hide()
                    $('#changemail').val('')
                    $('#checkpassword').val('')
                    $('#closemail').click()
                }, 1250);

            }
        }
    })
})
$('.changepassword-alert').hide()
var csrf = $("input[name=csrfmiddlewaretoken]").val();
$(document).on("submit", "#form-change-password", function(e) {
    e.preventDefault()
    let form_action = $('#form-change-password').attr('action')
    if ($('#newpassword').val() == $('#renewpassword').val()) {
        $.ajax({
            url: form_action,
            type: 'POST',
            data: {
                'oldpassword': $('#oldpassword').val(),
                'npassword': $('#newpassword').val(),
                'renpassword': $('#renewpassword').val(),
                'csrfmiddlewaretoken': csrf,
            },
            success: function(data) {
                if (data.info == false) {
                    if (data.danger == 1) {
                        $('.changepassword-alert').show()
                        $('.changepassword-alert').html('Eski şifrenizi yanlış girdiniz.')
                        $('.changepassword-alert').addClass('alert-warning').removeClass('alert-succsess')

                    } else if (data.danger == 2) {
                        $('.changepassword-alert').show()
                        $('.changepassword-alert').html(data.dangerinfo)
                        $('.changepassword-alert').addClass('alert-warning').removeClass('alert-succsess')


                    } else if (data.danger == 3) {
                        $('.changepassword-alert').show()
                        $('.changepassword-alert').html('Şifreler uyuşmuyor.')
                        $('.changepassword-alert').addClass('alert-warning').removeClass('alert-succsess')

                    } else if (data.danger == 4) {
                        $('.changepassword-alert').show()
                        $('.changepassword-alert').html('Yeni şifren eskisi ile aynı olamaz.')
                        $('.changepassword-alert').addClass('alert-warning').removeClass('alert-succsess')

                    }
                } else {
                    $('.changepassword-alert').show()
                    $('.changepassword-alert').html('Şifreniz değiştirildi.Tekrar giriş için yönlendiliceksiniz.')
                    $('.changepassword-alert').addClass('alert-success').removeClass('alert-warning')
                    setTimeout(() => {
                        window.location.replace('/user/login/')
                    }, 2000);

                }
            }
        })
    } else {
        $('.changepassword-alert').show()
        $('.changepassword-alert').html('Şifreler uyuşmuyor.')
        $('.changepassword-alert').addClass('alert-warning').removeClass('alert-succsess')
    }

})