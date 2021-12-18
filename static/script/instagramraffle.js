function onFollowChange() {
    var key = window.event.keyCode;

    if (key === 13) {
        document.getElementById("id_followlist").value = document.getElementById("id_followlist").value + ",";
        return false;
    } else {
        return true;
    }
}

function onTextChange() {
    var key = window.event.keyCode;

    if (key === 13) {
        document.getElementById("id_textlist").value = document.getElementById("id_textlist").value + ",";
        return false;
    } else {
        return true;
    }
}

$(document).ready(function() {
    $("#total-comment").hide()
    $(".load-container").hide()
    $("#spinner").hide()
    csrf = $("input[name=csrfmiddlewaretoken]").val();
    $(".get-btn").click(function(event) {
        event.preventDefault()
        $('#get-comments').addClass('disabled')
        $("#spinner").show()
        username = $("input[id=id_username]").val()
        posturl = $("input[id=id_posturl]").val()
        if (username.length != 0 && posturl.length != 0) {
            $.ajax({
                url: '/raffle/instagram-raffle/total-comment/',
                type: 'post',
                data: {
                    'username': username,
                    'posturl': posturl,
                    'csrfmiddlewaretoken': csrf
                },
                success: function(data) {
                    setTimeout(() => {
                        $("#spinner").hide()
                        $("#total-comment").show()
                        $('#alert-total').text(data.totalcomment)
                        if (data.totalcomment.length > 8) {
                            $('#get-comments').removeClass('disabled')
                            $('#total-comment').addClass('alert-danger')
                        } else {
                            $("#get-comments").hide()
                            $('#total-comment').removeClass('alert-danger').addClass('alert-success')
                        }


                    }, 500);

                },
                dataType: 'json',
            });
        } else {
            setTimeout(() => {
                $('#get-comments').removeClass('disabled')
                $('#spinner').hide()
                $('#total-comment').show()
                $('#alert-total').text('"Username" ya da "Gönderi Link" bilgilerini girmediniz.')
                $('#total-comment').addClass('alert-danger')
            }, 200);
        }
    });

    $(document).on('submit', '#raffleinstagram', function(event) {
        event.preventDefault();
        title = $('#id_title').val()
        username = $('#id_username').val()
        posturl = $('#id_posturl').val()
        member = $('#id_members').val()
        tag = $('#id_tags').val()
        follow = $('#id_followlist').val()
        text = $('#id_textlist').val()
        useracount = $('#id_usercount:checked').val()
        backup = $('#id_backup').val()
        console.log(backup)
        winner = $('#id_winner').val()
        animate = $('#id_animate').val()

        if (member == 'Bir Paket Seçin') {
            $('#total-comment').show()
            $('#alert-total').text('Lütfen paket seçiniz...!')
            $('#total-comment').addClass('alert-danger')
            document.querySelector('#id_username').scrollIntoView({ behavior: 'smooth' })
        } else {
            $('.raffle-btn').prop('disabled', true)
            $('.load-container').show()
            $("html, body").animate({ scrollTop: 0 }, "slow");
            $('.raffle-form').hide()

            $.ajax({
                url: '/raffle/instagram-raffle/',
                type: 'POST',
                data: {
                    'title': title,
                    'username': username,
                    'posturl': posturl,
                    'member': member,
                    'tag': tag,
                    'follow': follow,
                    'text': text,
                    'useracount': useracount,
                    'backup': backup,
                    'winner': winner,
                    'animate': animate,
                    'csrfmiddlewaretoken': csrf,
                },
                success: function(data) {
                    if (data.status == true) {
                        if (data.winner.length == 0) {
                            $('.raffle-form').show()
                            $('.load-container').hide()
                            $('.raffle-btn').prop('disabled', false)
                            $('#alert-total').text(data.info)
                            $('#total-comment').addClass('alert-danger')
                            document.querySelector('#id_username').scrollIntoView({ behavior: 'smooth' })

                        } else {
                            $('#load-container-text').text('Sonuçlar için yönlendiriliyorsunuz. Lütfen bekleyiniz..')
                            setTimeout(() => {
                                location.assign('/raffle/instagram-raffle/result/' + data.raffleid + '/')
                            }, 2000);
                        }

                    } else {
                        $('.load-container').hide()
                        $('.raffle-form').show()
                        $('#total-comment').show()
                        $('#alert-total').text('EROR 500! Lütfen bir süre bekleyip tekrar deneyiniz..')
                        $('#total-comment').addClass('alert-danger')
                        document.querySelector('#id_username').scrollIntoView({ behavior: 'smooth' })
                    }

                },
            });
        }
    });
});