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
            $("#qr-img").attr("src", response);
        }
        $("#icon-img").hide();
        $("#email-form").hide();
        $("#p1").text('Scan to authenticate');
        var u = $("#exampleInputEmail1").val();
        if (u) {
            $("#username").text(u.split('@')[0]);
        }
        $("#p2").show();
    });
}

function createChallenge() {
    return $.post(urls.createChallenge, { sessionToken: localStorage.getItem('sessionToken') }, function(response) {
        return response;
    });
}

function poll() {
    if ((typeof window.orientation) !== 'undefined') {
        window.location = "liveensure://localhost/mobile?sessionToken=" + localStorage.getItem('sessionToken') + "&status=https://app23.liveensure.com/live-identity/idr";
    }

    // retrun;
    var dfd = jQuery.Deferred();
    var i = 0;
    var ajx = null;
    var intervalCheck = true;

    clear = setInterval(function() {
        if(ajx && ajx.state() === "pending") {
            return;
        }
        ajx = $.get(urls.pollStatus, { sessionToken: localStorage.getItem('sessionToken') }, function(response) {
            console.log(response);
            
            if (response.sessionStatus === "FAILED") {
                intervalCheck = false;
                clearInterval(clear);
                dfd.resolve(0);
            } else if (response.sessionStatus === "SUCCESS") {
                intervalCheck = false;
                clearInterval(clear);
                dfd.resolve(1);
            }
        });
    }, 5000);

    setTimeout(function() {
        if(intervalCheck) {
            clearInterval(clear);
            console.log(clear);
            dfd.resolve(-1);    
        }
    }, 1000 * 120);

    return dfd.promise();
}
