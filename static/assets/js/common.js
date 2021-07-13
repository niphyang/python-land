$(function () {
    fn_change_sido_event();
    $("html").css("width","100%");


});

$(document).on({
    ajaxStart: function(){
        fn_loading_start();
    },
    ajaxStop: function(){
        fn_loading_stop();
    }
})

function fn_change_sido_event() {

    $("#sido").unbind("change").bind("change", function () {
        var sidoCd = $(this).val();

        $("#gungu").empty()
        $("#gungu").append("<option value=\"\" selected>군/구</option>");
        $("#dong").empty();
        $("#dong").append("<option value=\"\" selected>동</option>");

        if (sidoCd == "") {
            return;
        }

        var url = "/complexes/getGunguInfo/" + sidoCd;

        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            success: function (data, status, request) {

                var gungu = data.result;
                $("#gungu").empty();
                $("#gungu").append("<option value=\"\" selected>군/구</option>");
                for (var i = 0; i < gungu.length; i++) {
                    $("#gungu").append("<option value=\"" + gungu[i].cortarNo + "\">" + gungu[i].cortarName + "</option>");
                }
                fn_change_gungu_event();
            },
            error: function (data, status) {

            }
        })
    });
}

function fn_change_gungu_event() {

    $("#gungu").unbind("change").bind("change", function () {
        var gunguCd = $(this).val();


        $("#dong").empty();
        $("#dong").append("<option value=\"\" selected>동</option>");

        if (gunguCd == "") {
            return;
        }

        var url = "/complexes/getDongInfo/" + gunguCd;

        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            success: function (data, status, request) {

                var dong = data.result;
                $("#dong").empty();
                $("#dong").append("<option value=\"\" selected>동</option>");
                for (var i = 0; i < dong.length; i++) {
                    $("#dong").append("<option value=\"" + dong[i].cortarNo + "\">" + dong[i].cortarName + "</option>");
                }
                fn_change_dong_event();
            },
            error: function (data, status) {

            }
        })
    });
}


function fn_change_dong_event() {

    $("#dong").unbind("change").bind("change", function () {
        var dongCd = $(this).val();

        if (dongCd == "") {
            return;
        }

        var url = "/complexes/getAptList/" + dongCd;

        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            success: function (data, status, request) {
                var apt = data.complexList;

                $("#searchData").empty();
                for (var i = 0; i < apt.length; i++) {
                    var tr = "<tr id='" +apt[i].complexNo+ "'>";
                    tr += "<td>" + (apt.length-i) + "</td>";
                    tr += "<td>" + apt[i].complexName + "</td>";
                    tr += "<td>" + apt[i].cortarAddress + " " + apt[i].detailAddress + "</td>";
                    tr += "<td>" + apt[i].lowFloor + "/" + apt[i].highFloor + "</td>";
                    tr += "<td>" + apt[i].totalHouseholdCount + "</td>";

                    if(apt[i].useApproveYmd.length >= 4){
                        tr += "<td>" + apt[i].useApproveYmd.substr(0, 4) + "-" + apt[i].useApproveYmd.substr(4, 2)  /*apt[i].useApproveYmd.substr(6, 2)*/ + "</td>";
                    }else{
                        tr += "<td>-</td>"
                    }

                    tr += "</td>";

                    $("#searchData").append(tr);
                }

                $("#searchData tr").unbind("click").bind("click",function(){
                    var aptCd = $(this).attr("id");
                    fn_apt_click_event(aptCd);
                });

            },
            error: function (data, status) {

            }
        })
    });
}
function fn_apt_click_event(aptCd){


        var url = "/complexes/getAptInfo/" + aptCd;

        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            success: function (data, status, request) {

                console.log(data);
            },
            error: function (data, status) {

            }
        })

}
function fn_loading_start(){
    var loading = '<div id="loading" style="position: absolute;width:100%;height:100%;top: 0;left: 0;">'
                +'<img src="/assets/img/loading.gif" style="position:absolute;width:200px;left: calc(50% - 100px);top: calc(50% - 100px);">'
                +'<div style="position:relative;width: 100%;height:100%;opacity:0.3;background-color: black">'
                +'</div>'
                +'</div>';

    $("#loading").remove();
    $("html").append(loading);
}
function fn_loading_stop(){
    $("#loading").remove();
}