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

// asd
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
    const leftResult = $("#leftResult");
    leftResult.empty();
    const rightResult = $("#rightResult");
    rightResult.empty();
    let index = 0;
    markers.map(mk => {
        if (index++ % 2 == 0) {
            leftResult.append(`<li class='list-group-item'>${mk.name}</li>`);
        } else {
            rightResult.append(`<li class='list-group-item'>${mk.name}</li>`);
        }
    })
}

//# sourceMappingURL=myfunc.js.map