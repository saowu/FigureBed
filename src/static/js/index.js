/*Figure bed*/

window.onload = function () {
    //监听上传进度
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

            let fileList = $('#upLoad')[0].files;

            if (fileList.length < 5) {

                $("#display-1").css("display", "none");
                $("#display-2").css("display", "");

                let formData = new FormData();
                for (let i = 0; i < fileList.length; i++) {
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
                        //计算百分比
                        let percent = Math.floor(e.loaded / e.total * 100) + "%";
                        document.getElementById("progress").style.width = percent;
                        document.getElementById("progress").innerText = percent;

                    }),
                    success: function (result) {
                        let fcsv = result.fcsv;
                        let paths = result.paths;

                        $(".alert-success").css("display", "");
                        $(".label.label-info").attr("href", fcsv);

                        for (let i = 0; i < paths.length; i++) {
                            $("#format").append("<div >\n" +
                                "                <label>文件： <code>" + paths[i].name + "</code></label>\n" +
                                "                <pre>" + paths[i].path + "</pre>\n" +
                                "                </div>");
                        }
                    },
                    error: function (result) {
                        $("#display-1").css("display", "");
                        $("#display-2").css("display", "none");
                        $(".alert-danger").css("display", "");
                    }
                });
            } else {
                alert("选中文件数量超出")
            }
        }
    )
};