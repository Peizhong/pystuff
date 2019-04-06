// import * as $ from "jquery";
class Student {
    constructor(firstName, middleInitial, lastName) {
        this.firstName = firstName;
        this.middleInitial = middleInitial;
        this.lastName = lastName;
        this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
}
function greeter(person) {
    return "Hello, " + person.firstName + " " + person.lastName;
}

let map, searchService, latlngBounds = {}
let markers = []

// 取代模板中的搜索
function takeOverSearch(){
    $("#btnSearchAll").attr("type","button");
    $("#btnSearchAll").click(searchLocation);
}

function setContentSwitch(){
    $("#option1").change(function(){
        $("#qqmap").attr("hidden",false);
        $("#mycanvas").attr("hidden",true);
    });
    $("#option3").change(function(){
        $("#qqmap").attr("hidden",true);
        $("#mycanvas").attr("hidden",false);
    });
}

function drawWave(data){
    const canvas = document.getElementById("mycanvas");
    const waves = new Array(1000)
    
    for(let i =0; i<1000;i++){
        waves[i] = Math.sin(i*0.1)*2048+2048
    }
    var myChart = echarts.init(document.getElementById('mycanvas'));
    let i = 0;
    // 指定图表的配置项和数据
    var option = {
        xAxis: {
            type: 'value',           
            data: waves.map(function (item) {
                return i++;
            })
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            type: 'line',
            data: waves,
            smooth: true
        }]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function setUploadFile(){
    $("#inputGroupFile03").change(function(){
        const v = $(this).val()
        if (v){
            $("#inputGroupFile03 +").html(v)
            $('#inputGroupFileAddon03').attr("disabled",false)
        }
    })
    $("#inputGroupFileAddon03").attr("disabled",true)
    $("#inputGroupFileAddon03").click(function(){
        const selectedFile = document.getElementById("inputGroupFile03").files[0]
        var reader = new FileReader();
        reader.onload = function () {
            // 当读取完成后回调这个函数,然后此时文件的内容存储到了result中,直接操作即可
            // console.log(this.result);
            drawWave(this.result)
        }
        reader.readAsText(selectedFile);//读取文件的内容,也可以读取文件的URL
    })
}

function initChart() {

}

function initMap() {
    const center = new qq.maps.LatLng(39.936273, 116.44004334);
    const container = $("#qqmap")[0]
    map = new qq.maps.Map(container, {
        center: center,
        zoom: 13
    });
    var latlngBounds = new qq.maps.LatLngBounds();
    searchService = new qq.maps.SearchService({
        complete: function (results) {
            markers = [];
            var pois = results.detail.pois;
            for (var i = 0, l = pois.length; i < l; i++) {
                var poi = pois[i];
                latlngBounds.extend(poi.latLng);
                var marker = new qq.maps.Marker({
                    map: map,
                    position: poi.latLng
                });
                marker.setTitle(i + 1);

                markers.push({...marker,...poi});
            }
            setResult();
            map.fitBounds(latlngBounds);
        }
    });
    return "OK"
}

function searchLocation() {
    const keyword = $("#txtSearchAll").val();
    const region = new qq.maps.LatLng(39.936273, 116.44004334);

    searchService.setPageCapacity(5);
    searchService.searchNearBy(keyword, region, 2000);//根据中心点坐标、半径和关键字进行周边检索。
    console.log(`keyword is ${keyword}`);
}

function setResult() {
    const rightResult = $("#rightResult");
    rightResult.empty();
    markers.map(mk => {
        rightResult.append(`<li class='list-group-item'>${mk.name}</li>`);
    })
}
