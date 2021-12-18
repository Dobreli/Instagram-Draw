function onTestChange() {
    var key = window.event.keyCode;

    if (key === 13) {
        document.getElementById("id_list").value = document.getElementById("id_list").value + ",";
        return false;
    } else {
        return true;
    }
}
$(document).ready(function() {

    $(".load-container").hide()
    $(".raffle-result-comment").hide()
    $(".raffle-result-container").hide()
    $(".raffle-backup-container").hide()
    $(".info").hide()


    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $(document).on('submit', '#freeraffleinstagram', function(event) {
        event.preventDefault()
        var title = $("#id_title").val()
        var winner = $("#id_winner").val()
        var list = $("#id_list").val()
        var backup = $("#id_backup").val()

        $.ajax({
            url: '/raffle/free-raffle/',
            type: 'post',
            data: {
                'title': title,
                'winner': winner,
                'list': list,
                'backup': backup,
                'csrfmiddlewaretoken': csrf
            },
            success: function(data) {
                $(".raffle-form").hide()
                $(".load-container").show()
                document.querySelector('.load-container').scrollIntoView({ behavior: 'smooth' })
                setTimeout(() => {
                    $(".load-container").hide()
                    let winhtml = ''
                    let backwinhtml = ''
                    for (let i = 0; i < data.winner.length; i++) {
                        winhtml += `
                        <div class="p-3 px-3 bd-highlight">
                        <div class="draw-card" style="float:none;margin:auto;visibility:hidden">
                                        <div class="text-center winner-card-bg">
                                            <div class="card-body pt-5 card-won">
                                                <h5 class="card-text card-title"> KAZANAN </h5>
                                                <h3 class="card-text win pt-3"></h3>
                                                <p class="number pt-1"></p>
                                            </div>
                                        </div>
                                        </div> 
                                        </div> 
                                        `
                    }
                    document.querySelector('.result-card').innerHTML = winhtml

                    if (data.backupwin.length > 0) {
                        for (let i = 0; i < data.backupwin.length; i++) {
                            backwinhtml += `
                            <div class="p-3 px-3 bd-highlight">
                            <div class="backdraw-card" style="float:none;margin:auto;visibility:hidden">
                        <div class="text-center backup-card-bg">
                            <div class="card-body pt-5 backcard-won">
                                <h5 class="card-text card-title"> Yedek </h5>
                                <h3 class="card-text backwin pt-3"></h3>
                                <p class="backnumber pt-1"></p>
                            </div>
                        </div>
                        </div>
                        </div> `
                        }
                        document.querySelector('.result-backup-card').innerHTML = backwinhtml
                    }
                    $(".raffle-result-comment").show()
                    if (data.backupwin.length > 0) {
                        $(".raffle-backup-container").show()
                    }
                    $(".raffle-result-container").show()
                    document.getElementById('result-title').innerHTML = data.title
                    document.getElementById('result-title-len').innerHTML = 'Toplam :' + data.len + ' kişi arasından'

                    if (data.info != '') {
                        $(".info").show()
                        document.getElementById('info').innerHTML = data.info
                    }

                    function sleep(ms) {
                        return new Promise(resolve => setTimeout(resolve, ms));
                    }

                    async function winnerfunction() {
                        var rafflecard = document.querySelectorAll(".draw-card")
                        var cardbg = document.querySelectorAll(".winner-card-bg")
                        var card = document.querySelectorAll(".card-won")
                        var win = document.querySelectorAll(".win");
                        var number = document.querySelectorAll(".number");

                        var backrafflecard = document.querySelectorAll(".backdraw-card")
                        var backcardbg = document.querySelectorAll(".backup-card-bg")
                        var backcard = document.querySelectorAll(".backcard-won")
                        var backwin = document.querySelectorAll(".backwin");
                        var backnumber = document.querySelectorAll(".backnumber");

                        for (let i = 0; i < win.length; i++) {
                            rafflecard[i].style.visibility = "visible";
                            for (let a = 0; a < 20; a++) {
                                var text = data.raffle_list[Math.floor(Math.random() * data.raffle_list.length)]
                                await sleep(100)
                                win[i].innerHTML = text
                            }
                            win[i].innerHTML = data.winner[i];
                            number[i].innerHTML = i + 1
                            card[i].style.transform = "scale(1.3)";
                            cardbg[i].classList.add("card-bg-after");
                            await sleep(300);
                            card[i].style.transform = "scale(1.0)";
                        }

                        document.querySelector('.result-backup-card').scrollIntoView({ behavior: 'smooth' })

                        for (let c = 0; c < backwin.length; c++) {
                            backrafflecard[c].style.visibility = "visible";
                            for (let d = 0; d < 20; d++) {
                                var text = data.raffle_list[Math.floor(Math.random() * data.raffle_list.length)]
                                await sleep(100)
                                backwin[c].innerHTML = text
                            }
                            backwin[c].innerHTML = data.backupwin[c];
                            backnumber[c].innerHTML = c + 1
                            backcard[c].style.transform = "scale(1.3)";
                            backcardbg[c].classList.add("card-bg-after");
                            await sleep(300);
                            backcard[c].style.transform = "scale(1.0)";
                        }
                    }
                    winnerfunction()

                }, 3000);

            },
            dataType: 'json',
        });
    });
});