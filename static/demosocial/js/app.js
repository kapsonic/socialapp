function makeInitSessionCall() {
    $("#qr-img").attr("src", "//s3.amazonaws.com/clickmeter.com/Web/static/small-loader.gif");

    return $.post(urls.initSession, $("#email-form").serialize(), function(response) {
        return response;
    }).then(function(response) {
        if (!response.sessionToken) {
            alert(response.statusMessage);
            $("#qr-img").attr("src", "");
            return $.Deferred().reject(response).promise();
        }
        localStorage.setItem("sessionToken", response.sessionToken);
        return response;
    });
}

function getQRCode() {
    var url = "/QR?w=240&sessionToken=" + localStorage.getItem('sessionToken');
    return $.get(urls.getCode, { sessionToken: localStorage.getItem('sessionToken') }, function(response) {
        if (typeof window.orientation == 'undefined') {
            $("#icon-img").hide();
            $("#qr-img").attr("src", response);
        }
    });
}

function createChallenge() {
    return $.post(urls.createChallenge, { sessionToken: localStorage.getItem('sessionToken') }, function(response) {
        return response;
    });
}

function poll() {
    if (typeof window.orientation !== 'undefined') {
        window.location = "liveensure://localhost/mobile?sessionToken=" + localStorage.getItem('sessionToken') + "&status=https://app23.liveensure.com/live-identity/idr";
    }

    // retrun;
    var dfd = jQuery.Deferred();
    
    clear = setInterval(function() {
       
        $.get(urls.pollStatus, { sessionToken: localStorage.getItem('sessionToken') }, function(response) {
            console.log(response);
            $("#polling-status-ip").val(response.sessionStatus);
            if (response.sessionStatus === "FAILED") {
                $("#qr-img").attr("src", "https://cdn0.iconfinder.com/data/icons/shift-free/32/Error-128.png");
                clearInterval(clear);
                $("#info").text("Sorry, thats not you!");
                dfd.resolve();
            } else if (response.sessionStatus === "SUCCESS") {
                $("#qr-img").attr("src", "https://www.stagecoach.co.uk/Stagecoach/media/images/Parties/Mini%20Width/536x327-pop-party.jpg?width=536&height=326&ext=.jpg");
                $("#info").text("Cool picture");
                clearInterval(clear);
                dfd.resolve();
            }
            
        });
    }, 5000);

    return dfd.promise();
}
