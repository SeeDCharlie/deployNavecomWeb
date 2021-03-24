$(document).ready(function () {

    var activeDiv = 1;
    showDiv(activeDiv);
    var timer = setInterval(changeDiv, 8200);


    function changeDiv() {
        activeDiv++;
        if (activeDiv == 3) {
            activeDiv = 1;
        }
        showDiv(activeDiv);
    }

    function showDiv(num) {
        $('div.dis').hide();
        $('.portada' + num).fadeIn();
    }

});