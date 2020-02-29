window.onload = function () {

    let xhrOnProgress = function (fun) {
        xhrOnProgress.onprogress = fun;
        return function () {
            var xhr = $.ajaxSettings.xhr();
            if (typeof xhrOnProgress.onprogress !== 'function')
                return xhr;
            if (xhrOnProgress.onprogress && xhr.upload) {
                xhr.upload.onprogress = xhrOnProgress.onprogress;
            }
            return xhr;
        }
    };

    $('body').on('change', '#upLoad', function (e) {
            $("#display-1").css("display", "none");
            $("#display-2").css("display", "");

            let formData = new FormData();
            let fileList = $('#upLoad')[0].files;
            for (var i = 0; i < fileList.length; i++) {
                formData.append('files', fileList[i]);
            }

            $.ajax({
                type: 'POST',
                url: '/upload',
                data: formData,
                processData: false,
                contentType: false,
                dataType: "json",
                xhr: xhrOnProgress(function (e) {
                    let percent = Math.floor(e.loaded / e.total * 100) + "%";//计算百分比
                    document.getElementById("progress").style.width = percent;
                    document.getElementById("progress").innerText = percent;

                }),
                success: function (data) {
                    for (var i = 0; i < data.length; i++) {
                        $("#format").append("<div >\n" +
                            "                <label>Link: <code>" + data[i].name + "</code> </label>\n" +
                            "                <pre id=\"Link\">" + data[i].path + "</pre>\n" +
                            "            </div>");
                    }
                }
                , error: function (data) {
                    console.log('错误');
                }
            });
        }
    )
};