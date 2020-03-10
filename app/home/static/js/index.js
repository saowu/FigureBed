/*Figure bed*/

window.onload = function () {
    /**
     * 上传进度监听
     * @param fun
     * @returns {function(...[*]=)}
     */
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

    /**
     * 上传函数
     * @param fileList
     */
    function upload(fileList) {
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
                    $(".alert-danger").css("display", "none");
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
                    $("#upLoad").val("");
                    $("#display-1").css("display", "");
                    $("#display-2").css("display", "none");
                    $(".alert-danger").css("display", "");
                }
            });
        } else {
            alert("选中文件数量超出")
        }

    }

    /*取消默认拖动效果*/
    document.addEventListener("drop", function (e) {  //拖离
        e.preventDefault();
    });
    document.addEventListener("dragleave", function (e) {  //拖后放
        e.preventDefault();
    });
    document.addEventListener("dragenter", function (e) {  //拖进
        e.preventDefault();
    });
    document.addEventListener("dragover", function (e) {  //拖来拖去
        e.preventDefault();
    });

    /**
     * 监听文件拖动
     */
    document.getElementById('dropzone').addEventListener("drop", function (e) {
        let fileList = e.dataTransfer.files;
        //检测是否是拖拽文件到页面的操作
        upload(fileList);
    }, false);
    /**
     * 监听选中状态
     */
    $('body').on('change', '#upLoad', function (e) {
        let fileList = $('#upLoad')[0].files;
        upload(fileList);
    });

};