var apigClient = apigClientFactory.newClient({
    // defaultContentType:'image/jpeg',
    apiKey: 'bZcji7Nw3l98C8EOWKiOW6TVjamNXHSL8Bj3pSzj'
});



$(function (param) {
    FilePond.registerPlugin(

        // encodes the file as base64 data
        FilePondPluginFileEncode,

        // // validates the size of the file
        // FilePondPluginFileValidateSize,

        // // corrects mobile image orientation
        // FilePondPluginImageExifOrientation,

        // // previews dropped images
        // FilePondPluginImagePreview
    );

    $('#input').filepond({
        allowFileEncode: true,
    });
    $("#input").on('FilePond:addfile', function (e) {
        var encodedChecker = null;
        if (encodedChecker !== null) {
            clearInterval(encodedChecker); // perfectly safe to clear null, but we don't need to do that.
            encodedChecker = null; // just to be safe
        }
        encodedChecker = setTimeout(function () {
            // Now the element exists and the value is accessible
            console.log($('input[name="filepond"]'));
            if ($('input[name="filepond"]').get(0).value !== "") {
                var data = JSON.parse($("input[name='filepond']").get(0).value);
                var params = {
                    //This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
                    folder: 'photos-cs9223',
                    item: data.name,
                    // "Content-Type": data.type,
                    "Content-Type": 'text/plain',
                    // "Accept": "image/jpeg"
                    // 'accept':'image/jpeg'
                };
                var additionalParams = {
                    //If there are any unmodeled query parameters or headers that need to be sent with the request you can add them here
                    headers: {
                        "Content-Encoding": "base64"
                    }
                };
                console.log(data.data);
                apigClient.photosFolderItemPut(params, data.data, {})
                    .then(function (result) {
                        //This is where you would put a success callback
                        $(".upload-success").addClass("show");
                        $("#input").filepond('removeFiles');
                    }).catch(function (result) {
                        //This is where you would put an error callback
                        $(".upload-fail").addClass("show");
                        console.log(result);
                    });
                clearInterval(encodedChecker);
            }

        }, 5000);
        // var file = $(this).filepond('getFiles')[0];
        // console.log(file.filename);
        // console.log(file);
        // console.log(file.file);
    });


})


$("#search").on('keydown', (event) => {
    if (event.which == 13) {
        var params = {
            q: $("#search").val()
        }
        apigClient.searchGet(params, {}, {}).then((result) => {
            console.log(result);
            var album = $(".album");
            album.empty();
            $.each(result.data.hits.results, function (i, v) {
                console.log(v);
                album.append('<div class="box"\>\ <img src="' + v.url + '" class="img-thumbnail"> </div>');
            });
        }).catch((err) => {
            console.log(err);
        })
    }
})
