$(document).ready(function() {
    csrf = $("input[name=csrfmiddlewaretoken]").val()
    raffleid = $('#result-raffleid').text()
    $.ajax({
        url: '/raffle/instagram-raffle/result/' + raffleid + '/',
        type: 'post',
        data: {
            'csrfmiddlewaretoken': csrf
        },
        success: function(data) {

            var pic = $('#profile-pic-main').attr('src')
            $('#profile-pic-main').attr('src', '/static/profilepic/' + raffleid + '/' + data.username + '.jpg')
            $('#result-title').text(data.title)
            $('#result-username').text(data.username)
            $('#validlist').text(`Geçerli yorum sayısı : ${data.validlist.length}`)
            $('#raffle-href').attr('href', data.url)
            let html = ''
            for (let i = 0; i < data.validlist.length; i++) {
                html += `<p id="modal-body-p"></p>`
            }
            $('.modal-body-user-list').html(html)
            var winhref = document.querySelectorAll("#modal-body-p")

            for (let i = 0; i < data.validlist.length; i++) {
                winhref[i].innerHTML = data.validlist[i].username
            }
            let winhtml = ''
            let backwinhtml = ''
            for (let i = 0; i < data.winner.length; i++) {
                winhtml +=
                    `<div class="p-3 px-3 bd-highlight position-relative"> 
            <div class="follow-result" style="display: none;">
            
            </div>

            
            <div class="winraffle-card" style="display: none;">
                <div class="text-center winner-card-bg ">
                    <div class="card-body-start pt-2 card-won">
                        <a class="win-href" target="_blank" rel="noopener noreferrer">
                            <img id='profile-pic' class="card-img-top winner-img" src="/static/img/avatar.png" alt="profil">
                        </a>
                    </div>
                    <div class="card-body-center card-won">
                        <h5 class="raffle-card-text win-username"></h5>
                    </div>
                    <div class="card-body-end my-auto">
                        <p class="number pt-1"></p>
                    </div>
                </div>
            </div>
        </div>`
            }
            $('.result-card').html(winhtml)

            if (data.backup.length > 0) {
                for (let i = 0; i < data.backup.length; i++) {
                    backwinhtml +=
                        `<div class="p-3 px-3 bd-highlight position-relative">
                    <div class="follow-result" style="display: none;">
                   
                    </div>
                    <div class="backraffle-card" style="display: none;">
                        <div class="text-center pt-2 backup-card-bg">
                            <div class="card-body-start backcard-won">
                                <a class="backwin-href" target="_blank" rel="noopener noreferrer">
                                <img id='profile-pic' class="card-img-top backup-img" src="/static/img/avatar.png" alt="profil">
                                </a>
                            </div>
                            <div class="card-body-center">
                                <h5 class="raffle-card-text backup-username"></h5>
                            </div>
                            <div class="card-body-end ">
                                <p class="backnumber pt-1"></p>
                            </div>
                        </div>
                    </div>
                </div>`
                }
                $('.result-backup-card').html(backwinhtml)

            }
            $('.result-backup-card').hide()
            $('.result-card').hide()

            if (data.follow.length > 0) {
                var followin = document.querySelectorAll(".follow-result")
                const followlist = data.follow
                var followhtml = ""
                for (let i = 0; i < followlist.length; i++) {
                    followhtml +=
                        `<span class="position-absolute translate-middle badge rounded-pill">
                        <img id='profile-pic' class="card-img-top follow-img" src="/static/img/avatar.png" alt="profil" style="width: 25px !important;height: 25px !important;">
                            <span class="follow-ico">                          
                            </span>
                            <span class="visually-hidden">unread messages</span>
                    </span>`
                }
                follow = `<i class="fas fa-check" style="font-size: 12px;"></i>`
                unfollow = `<i class="fas fa-times" style="font-size: 12px;"></i>`
                var winlist = data.winner
                var backlist = data.backup
                const alllist = []
                for (let i = 0; i < winlist.length; i++) {
                    alllist.push(winlist[i])
                }
                for (let i = 0; i < backlist.length; i++) {
                    alllist.push(backlist[i])
                }
                var countlist = winlist.length + backlist.length

                for (var m = 0; m < countlist; m++) {
                    followin[m].innerHTML = followhtml
                    var badge = followin[m].querySelectorAll(".badge")
                    var t = 10
                    for (let i = 0; i < badge.length; i++) {
                        badge[i].style.left = "100%"
                        badge[i].style.top = t + "%"
                        badge[i].style.display = "block"
                        t += 15
                        for (let f = 0; f < followlist.length; f++) {
                            if (alllist[m][followlist[f]] == "True") {
                                badge[i].classList.add("bg-success");
                            } else {
                                badge[i].classList.add("bg-danger");
                            }
                        }
                        var followimg = badge[i].querySelectorAll(".follow-img")
                        var ico = badge[i].querySelectorAll(".follow-ico")
                        for (let i = 0; i < followimg.length; i++) {
                            for (let f = 0; f < followlist.length; f++) {
                                followimg[i].src = ('/static/profilepic/' + raffleid + '/' + followlist[f] + '.jpg')

                            }

                        }
                        for (let i = 0; i < ico.length; i++) {
                            for (let f = 0; f < followlist.length; f++) {
                                if (alllist[m][followlist[f]] == "True") {
                                    ico[i].innerHTML = follow
                                } else {
                                    ico[i].innerHTML = unfollow
                                }
                            }

                        }
                    }
                }
            }


            var followwin = document.querySelectorAll(".follow-result")
            var winhref = document.querySelectorAll(".win-href")
            var rafflecard = document.querySelectorAll(".winraffle-card")
            var cardbg = document.querySelectorAll(".winner-card-bg")
            var card = document.querySelectorAll(".card-won")
            var win = document.querySelectorAll(".win-username");
            var number = document.querySelectorAll(".number");
            var winnerimg = document.querySelectorAll(".winner-img")

            var backwinhref = document.querySelectorAll(".backwin-href")
            var backrafflecard = document.querySelectorAll(".backraffle-card")
            var backcardbg = document.querySelectorAll(".backup-card-bg")
            var backcard = document.querySelectorAll(".backcard-won")
            var backwin = document.querySelectorAll(".backup-username");
            var backnumber = document.querySelectorAll(".backnumber");
            var backupimg = document.querySelectorAll(".backup-img")

            if (data.backup.length == 0) {
                $('.result-backup').hide()
                $('.result-backup-card').hide()
            } else {
                $('.result-backup').show()
                $('.result-backup-card').show()
            }
            $('.result-card').show()

            if (data.status == true) {

                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }
                async function winnerfunction() {
                    var animate = parseFloat(data.animate)
                    animate = animate * 10

                    document.querySelector('#validlist').scrollIntoView({
                        behavior: 'smooth'
                    })
                    for (let i = 0; i < win.length; i++) {
                        rafflecard[i].style = "display:block;z-index:-1;"
                        for (let a = 0; a < animate; a++) {
                            var text = data.validlist[Math.floor(Math.random() * data.validlist.length)]
                            await sleep(100)
                            win[i].innerHTML = text.username
                        }
                        win[i].innerHTML = data.winner[i].username;
                        winhref[i].href = 'https://www.instagram.com/' + data.winner[i].username + '/'
                        number[i].innerHTML = i + 1
                        winnerimg[i].src = ('/static/profilepic/' + raffleid + '/' + data.winner[i].username + '.jpg')
                        cardbg[i].style.transform = "scale(1.3)";
                        cardbg[i].classList.add("card-bg-after");
                        console.log(win[i].querySelector(".follow-result"))
                        await sleep(300);
                        cardbg[i].style.transform = "scale(1.0)";
                        if (win.length - 1 == i) {
                            if (data.backup.length > 0) {

                                rafflecard[i].scrollIntoView({
                                    behavior: 'smooth'
                                })


                            }
                        }

                    }

                    for (let i = 0; i < backwin.length; i++) {
                        backrafflecard[i].style = "display:block;z-index:-1;"
                        for (let a = 0; a < animate; a++) {
                            var text = data.validlist[Math.floor(Math.random() * data.validlist.length)]
                            await sleep(100)
                            backwin[i].innerHTML = text.username
                        }
                        backwin[i].innerHTML = data.backup[i].username;
                        backwinhref[i].href = 'https://www.instagram.com/' + data.backup[i].username + '/'
                        backnumber[i].innerHTML = i + 1
                        backupimg[i].src = ('/static/profilepic/' + raffleid + '/' + data.backup[i].username + '.jpg')
                        backcardbg[i].style.transform = "scale(1.3)";
                        backcardbg[i].classList.add("card-bg-after");
                        await sleep(300);
                        backcardbg[i].style.transform = "scale(1.0)";

                    }
                    var countwin = data.winner.length + data.backup.length
                    for (let i = 0; i < countwin; i++) {
                        followwin[i].style = "position: relative;display:block;z-index:3;"
                    }

                }
                winnerfunction()

            } else {

                $('.result-card').show()
                $('.result-backup-card').show()


                for (let i = 0; i < win.length; i++) {
                    rafflecard[i].style.display = "block"
                    win[i].innerHTML = data.winner[i].username;
                    winhref[i].href = 'https://www.instagram.com/' + data.winner[i].username + '/'
                    winnerimg[i].src = '/static/profilepic/' + raffleid + '/' + data.winner[i].username + '.jpg'
                    number[i].innerHTML = i + 1
                    cardbg[i].classList.add("card-bg-after");
                }

                for (let i = 0; i < backwin.length; i++) {
                    backrafflecard[i].style.display = "block"
                    backwin[i].innerHTML = data.backup[i].username;
                    backwinhref[i].href = 'https://www.instagram.com/' + data.backup[i].username + '/'
                    backupimg[i].src = ('/static/profilepic/' + raffleid + '/' + data.backup[i].username + '.jpg')
                    backnumber[i].innerHTML = i + 1
                    backcardbg[i].classList.add("card-bg-after");

                }
                if (data.follow.length > 0) {
                    var followwin = document.querySelectorAll(".follow-result")
                    var countwin = data.winner.length + data.backup.length

                    for (let i = 0; i < countwin; i++) {
                        console.log(followwin[i])
                        followwin[i].style.display = "block"
                    }
                }
            }
        }
    })
})