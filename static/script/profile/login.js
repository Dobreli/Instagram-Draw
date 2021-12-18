function check() {
    $.ajax({
        type: "post",
        url: "{% url 'istek_yollanacak_url'  %}",
        dataType: 'json',
        data: {

        },
        success: function(response) {
            if (response.result) {
                sweetAlert("İşlem Başarılı", response.message, "success");
            } else {
                sweetAlert("Hata!", response.message, "error");
            }
        },
    });
}