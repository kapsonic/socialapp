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
            $("#email-form").hide();
            $("#p1").hide();
            var u = $("#exampleInputEmail1").val();
            if(u) {
                $("#username").text(u.split('@')[0]);
            }
            $("#p2").show();
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
                clearInterval(clear);
                dfd.resolve(false);
            } else if (response.sessionStatus === "SUCCESS") {
                clearInterval(clear);
                dfd.resolve(true);
            }
            
        });
    }, 5000);

    return dfd.promise();
}
