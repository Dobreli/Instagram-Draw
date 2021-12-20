$(document).ready(function() {

    $('#spinner').hide()

    $(document).on('submit', '#query-raffle', function(event) {
        $('.reference-query-alert').hide()
        event.preventDefault();
        $('#spinner').show()
        var raffleid = $('#id_raffleid').val()
        var csrf = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: '/raffle/instagram-raffle/raffle-query/',
            type: 'post',
            data: {
                'raffleid': raffleid,
                'csrfmiddlewaretoken': csrf,
            },
            success: function(data) {
                setTimeout(() => {
                    $('#spinner').hide()
                    if (data.status == true) {
                        if (data.rafflestatus == false) {
                            $('.reference-query-alert').show()
                            winhtml = ` 
                            <div class="col-12 text-center alert query-alert" role="alert">
                                <p id="query-alert"></p>
                            </div>`
                            $('.reference-query-alert').html(winhtml)
                            $('.reference-query-alert').text('Çekiliş sahibi yayından kaldırdı.')
                            $('.reference-query-alert').addClass('alert-warning')
                        } else {
                            winhtml = ` 
                        <div class="d-flex flex-wrap bd-highlight d-sm-flex mb-3 justify-content-center">
                        <div class="p-3 bd-highlight">
                        <div class="card-form" style="width: 15rem;">
                                        <div class="card-body text-center">
                                            <a id="ref-href-pic" target="_blank" href="">
                                                <img src="" class="card-img-top query-img" alt="profil pictures" style="width: 75px !important;border-radius:50%"></a>
                                            <h5 class="card-text query-card-username pt-2"></h5>
                                            <p class="card-text card-post">Gönderi Link :<a class="link-href query-href-post" target="_blank" rel="noopener noreferrer" href=""><i class="fas fa-external-link-alt"></i> </a></p>
                                            
                                            <p class="card-text query-card-winner">Kazanan : </p>
                                            <p class="card-text text-dark query-card-date text-secondary"></p>
                                            <a href="" class=" card-text btn query-btn get-btn">İncele</a>
                                        </div>
                                    </div>
                                </div>
                                </div>                               
                                `
                                /*<p class="card-text query-card-validlist">Katılımcı :</p>
                                     $('.query-card-validlist').text('Toplam Katılımcı :' + data.mainlist)
                                */
                            $('#query-result').html(winhtml)
                            $('#ref-href-pic').attr('href', data.post_url)
                            $('.query-img').attr('src', '/static/profilepic/' + raffleid + '/' + data.username + '.jpg')
                            $('.query-href-post').attr('href', data.post_url)
                            $('.query-card-username').text(data.username)

                            $('.query-card-winner').text('Kazanan :' + data.winner)
                            $('.query-card-date').text(data.date)
                            $('.query-btn').attr('href', 'http://127.0.0.1:8000/raffle/instagram-raffle/result/' + data.id + '/')
                        }


                    } else {
                        $('.reference-query-alert').show()
                        winhtml = ` 
                        <div class="col-12 text-center alert query-alert" role="alert">
                            <p id="query-alert"></p>
                        </div>`
                        $('.reference-query-alert').html(winhtml)
                        $('.reference-query-alert').text('Bu numaraya ait bir çekiliş bulunamadı.')
                        $('.reference-query-alert').addClass('alert-warning')

                    }
                }, 1000);
            }
        })

    })
});