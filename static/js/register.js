// alert("register") to see if this js page is loaded successfully

// 1. Find Send Auth Email button and set a click event
function bindEmailCaptchaClick(){
    $("#captcha-btn").click(function (event) {

        var $this = $(this);
        // block the default event -- block that form is submitted to the server
        // preventDefault seems to be redundant but it's a good practice
        // We can see it as a insurance.
        event.preventDefault();
        // var email = $("#exampleInputEmail1").val();
        var email = $("input[name='email']").val();
        $.ajax({
            // http://127.0.0.1:5000
            url: "/auth/captcha/email?email="+email,
            method: "GET",   // If is OK to use POST，but you have to declare at "blueprint"
            success: function (result) {
                var code = result['code'];
                if ( code == 200 ) {
                    var countdown = 60;
                    // suspend the click event before the timer start
                    $this.off('click');
                    var timer = setInterval(function () {
                        $this.text(countdown);  //.text can fetch the text content above
                        countdown -= 1;
                        if (countdown <= 0) {
                            clearInterval(timer);
                            // clear the timer
                            $this.text("Get Auth Email");
                            // Bind the click event again
                            bindEmailCaptchaClick();
                        }
                    }, 1000) // unit: ms
                    // alert("Email Auth Code has been sent successfully")
                } else {
                    alert(result["message"])
                }
            },
            fail: function (error) {
                console.log(error);
            }
        })
    })
}

// $(function()) => Execute after the whole web page is loaded
$(function () {
    bindEmailCaptchaClick();
})
