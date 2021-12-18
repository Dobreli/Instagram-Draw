function check() {
    var check = document.getElementById("accountcontact").checked
    if (check == false) {

        document.getElementById("dmessage").style.visibility = "visible";
        document.getElementById("dmessage").style.color = "red";
        return false

    } else if (check == true) {
        document.getElementById("register").submit();
        return true
    }

}