$(document).ready(function() {
    csrf = $("input[name=csrfmiddlewaretoken]").val()
    var visiblebtn = ''
    var cardno = ''
    var recardno = ''
    var cardstatus = ''
    var rerafflebtn = ''
    $('#alert-raffle').hide()

    function getvissible() {
        if (visiblebtn == '') {
            visiblebtn = document.querySelectorAll("#visibleraffle")
            cardno = document.querySelectorAll(".card-number")
            cardstatus = document.querySelectorAll(".card-status")

        } else {
            visiblebtn = document.querySelectorAll("#visibleraffle")
            cardno = document.querySelectorAll(".card-number")
            cardstatus = document.querySelectorAll(".card-status")

        }
        return visiblebtn
    }

    function reraffle() {
        if (rerafflebtn == '') {
            rerafflebtn = document.querySelectorAll("#reraffle")
            recardno = document.querySelectorAll(".card-number")

        } else {
            rerafflebtn = document.querySelectorAll("#reraffle")
            recardno = document.querySelectorAll(".card-number")

        }
        return rerafflebtn
    }

    var username = $('#user_username').text()
    $('.modal-footer').hide()
    $(document).on('click', reraffle(), function(event) {
        for (let i = 0; i < rerafflebtn.length; i++) {
            if (event.target == rerafflebtn[i]) {
                let no = recardno[i].innerHTML
                let html = `<div class="text-center">
                <p class="modal-no"></p>
                <h5 class="modal-comment">Çekilişi tekrarlamak mı istiyorsunuz ?</h5>
                <small><p class="model-comment">Not : Çekilişi tekrarlamak eski çekiliş kaydının silinmesine sebep olacaktır.</p></small>
                <button id="reraffle-modal" type="button" class="btn usersuccess-btn">Tekrarla</button>
                </div>`

                $('.modal-body').html(html)
                $('.modal-no').text(no)
                $('.modal-footer').show()
            }
        }
    })
    $(document).on('click', '#reraffle-modal', function() {
        let no = $('.modal-no').text()
        let html = `<div class="text-center">
            <div class="spinner-border text-warning" role="status" style="width: 100px;height: 100px; ">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h5 id="load-container-text" class="main-text">Lütfen bekleyiniz... İşleminiz gerçekleştiriliyor!</h5>
        </div>`
        $('.modal-body').html(html)
        $('.modal-footer').hide()
        $.ajax({
            url: '/raffle/re-instagram-raffle/',
            type: 'POST',
            data: {
                'raffleid': no,
                'csrfmiddlewaretoken': csrf
            },
            success: function(data) {
                html = `<div class="text-center">
                        <h5>Çekiliş sonucunu 
                        <a class="btn userraffle-btn result-reraffle">Görüntüle</a>
                        </h5>
                        </div>`
                $('.modal-footer').show()
                $('.modal-body').html(html)
                $('.result-reraffle').attr('href', '/raffle/instagram-raffle/result/' + no + '/')
            }
        })
    })





    $(document).on('click', getvissible(), function(event) {
        for (let i = 0; i < visiblebtn.length; i++) {
            if (event.target == visiblebtn[i]) {

                no = cardno[i].innerHTML
                $.ajax({
                    url: '/user/' + username + '/user-raffle/',
                    type: 'POST',
                    data: {
                        'no': no,
                        'csrfmiddlewaretoken': csrf
                    },
                    success: function(data) {
                        if (data.info == true) {
                            visiblebtn[i].text = 'Yayınlama'
                            cardstatus[i].innerHTML = 'YAYINDA'
                        } else {
                            visiblebtn[i].text = 'Yayınla'
                            cardstatus[i].innerHTML = 'YAYINLANMIYOR'
                        }

                    }
                })
            }
        }
    })
    $('#moreraffle').click(function() {
        var cardmain = document.querySelectorAll(".card-main")

        $.ajax({
            url: '/user/' + username + '/user-raffle/more-raffle/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrf,
                'resultlen': cardmain.length,
            },
            success: function(data) {
                var mediadata = data.info
                if (data.add_status == true) {
                    let win = ''
                    var oldmorecardmain = document.querySelectorAll(".more-card-main").length
                    for (let index = 0; index < mediadata.length; index++) {
                        win += `
                        <div class="p-3 bd-highlight">
                            <div class="card-main more-card-main">
                                <div class="card-body text-center">
                                    <a id="more-userraffle-href" target="_blank" href="">
                                        <img id="more-card-img" src="" class="card-img-top" alt="profil pictures" style="width: 75px !important;border-radius:50%"></a>
                                    <h5 class="card-text more-card-username pt-2"></h5>
                                    <p class="card-text more-card-post">Gönderi Link :
                                        <a id="more-link-href" class="link-href" target="_blank" rel="noopener noreferrer" href="">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-instagram link-href" viewBox="0 0 16 16">
                                                <path
                                                    d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z" />
                                            </svg>
                                        </a>
                                    </p>
                                    <p class="card-text more-card-number card-number"></p>
                                    <p class="card-text more-card-validlist"></p>
                                    <p class="card-text more-card-winner"></p>
                                    <p class="card-text more-card-status card-status"></p>
                                    <p class="card-text more-card-date text-secondary"></p>
                                    <a class="btn userget-btn detail-btn">İncele</a>
                                    <br>
                                    <a id="visibleraffle" class="btn usersubmit-btn more-usersubmit-btn m-2"></a>
                                    <br>
                                    <a id="reraffle" class="btn usersuccess-btn m-2" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Tekrarla</a>
                                    </div>
                                    </div>
                                </div>`
                    }
                    $('#more_raffle').html($('#more_raffle').html() + win)
                    getvissible()
                    reraffle()
                    var morecardmain = document.querySelectorAll(".more-card-main")
                    var cardimghref = document.querySelectorAll("#more-userraffle-href")
                    var cardimg = document.querySelectorAll("#more-card-img")
                    var moreusername = document.querySelectorAll(".more-card-username")
                    var linkhref = document.querySelectorAll("#more-link-href")
                    var number = document.querySelectorAll(".more-card-number")
                    var validlist = document.querySelectorAll(".more-card-validlist")
                    var winner = document.querySelectorAll(".more-card-winner")
                    var status = document.querySelectorAll(".more-card-status")
                    var date = document.querySelectorAll(".more-card-date")
                    var detailbtn = document.querySelectorAll(".detail-btn")
                    var moresubmitbtn = document.querySelectorAll(".more-usersubmit-btn")

                    if (morecardmain.length > mediadata.length) {
                        for (let a = morecardmain.length - mediadata.length; a < morecardmain.length; a++) {
                            cardimghref[a].href = mediadata[a - oldmorecardmain]['post_url']
                            cardimg[a].src = ('/static/profilepic/' + mediadata[a - oldmorecardmain]['id'] + '/' + mediadata[a - oldmorecardmain]['username'] + '.jpg')
                            moreusername[a].innerHTML = mediadata[a - oldmorecardmain]['username']
                            linkhref[a].href = mediadata[a - oldmorecardmain]['post_url']
                            number[a].innerHTML = mediadata[a - oldmorecardmain]['id']
                            validlist[a].innerHTML = 'Toplam Katılımcı : ' + mediadata[a - oldmorecardmain]['mainlist']
                            winner[a].innerHTML = 'Kazanan : ' + mediadata[a - oldmorecardmain]['winner']
                            if (mediadata[a - oldmorecardmain]['status'] == true) {
                                status[a].innerHTML = 'Durum : YAYINDA'
                                moresubmitbtn[a].innerHTML = 'Yayınlama'
                            } else {
                                status[a].innerHTML = 'Durum : YAYINLANMIYOR'
                                moresubmitbtn[a].innerHTML = 'Yayınla'
                            }
                            date[a].innerHTML = mediadata[a - oldmorecardmain]['date']
                            detailbtn[a].href = '/raffle/instagram-raffle/result/' + mediadata[a - oldmorecardmain]['id'] + '/'
                        }

                    } else {
                        for (let a = 0; a < morecardmain.length; a++) {
                            cardimghref[a].href = mediadata[a]['post_url']
                            cardimg[a].src = ('/static/profilepic/' + mediadata[a]['id'] + '/' + mediadata[a]['username'] + '.jpg')
                            moreusername[a].innerHTML = mediadata[a]['username']
                            linkhref[a].href = mediadata[a]['post_url']
                            number[a].innerHTML = mediadata[a]['id']
                            validlist[a].innerHTML = 'Toplam Katılımcı : ' + mediadata[a]['mainlist']
                            winner[a].innerHTML = 'Kazanan : ' + mediadata[a]['winner']
                            if (mediadata[a]['status'] == true) {
                                status[a].innerHTML = 'Durum : YAYINDA'
                                moresubmitbtn[a].innerHTML = 'Yayınlama'
                            } else {
                                status[a].innerHTML = 'Durum : YAYINLANMIYOR'
                                moresubmitbtn[a].innerHTML = 'Yayınla'
                            }
                            date[a].innerHTML = mediadata[a]['date']
                            detailbtn[a].href = '/raffle/instagram-raffle/result/' + mediadata[a]['id'] + '/'
                        }
                    }


                } else {
                    $('#alert-raffle').show()
                    $('#alert-raffle').addClass('alert-warning')
                    $('#alert-raffle-text').text('Tüm veriler yüklendi')

                }
            }

        })

    })
})