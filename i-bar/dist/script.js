var map = L.map("map", {
  center: [25.040959, 121.553324],
  zoom: 20
});



var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);



// ------------------------------------------------
// // setView 可以設定地圖座標
// // watch 則是持續監聽使用者的位置
// map.locate({setView: true, watch: true});
// // 成功監聽到使用者的位置時觸發
// map.on('locationfound', onLocationFound);
// // 失敗時觸發
// map.on('locationerror', onLocationError);
// function onLocationFound(e) {
// }
// function onLocationError(e) {
// }

// function onLocationFound(e) {
//   var myLocation = e.latlng // 使用者位置
// 　var bookstore = L.latLng(25.129836537742896, 121.74017250433087) // 書店
//   console.log(myLocation.distanceTo(bookstore)) // 計算使用者和書店的距離
// }

// -----------------------------------------



    var circle = L.circle([25.040959, 121.553324],   // 圓心座標
     1000,                // 半徑（公尺）
      {
          color: 'skyblue',      // 線條顏色
          fillColor: '#00298a', // 填充顏色
          fillOpacity: 0.1   // 透明度
      }
    ).addTo(map);


var Icon1 = new L.Icon({
  iconUrl: 'https://github.com/Han-lai/i-bar_map/blob/master/icons8-cocktail1.png?raw=true',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [200, 200],
  iconAnchor: [43, 86],
  popupAnchor: [1, -86],
  shadowSize: [10, 10]
});

var Icon2 = new L.Icon({
  iconUrl: 'https://github.com/Han-lai/i-bar_map/blob/master/icons8-cocktail2.png?raw=true',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [200, 200],
  iconAnchor: [43, 86],
  popupAnchor: [1, -86],
  shadowSize: [10, 10]
});

var Icon3 = new L.Icon({
    iconUrl: 'https://github.com/Han-lai/i-bar_map/blob/master/icons8-cocktail3.png?raw=true',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [200, 200],
    iconAnchor: [43, 86],
    popupAnchor: [1, -86],
    shadowSize: [10, 10]
});

var blackIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [86, 86],
    iconAnchor: [43, 86],
    popupAnchor: [1, -86],
    shadowSize: [10, 10]
});

var markers = new L.MarkerClusterGroup().addTo(map);;
//在中心座標，放上黑色定位圖標
//L.marker([25.037801, 121.548855], { icon: blackIcon }).addTo(map);


var xhr = new XMLHttpRequest();
xhr.open('get', 'https://raw.githubusercontent.com/Han-lai/i-bar_map/master/taipei_bar.json');
xhr.send();
xhr.onload = function () {
    var data = JSON.parse(xhr.responseText).results;
    for (var i = 0; i < data.length; i++) {

        //將酒吧星級標記不同顏色的圖標
        var imageIcon = blackIcon;
        if (data[i].rating >= 4.5)
            imageIcon = Icon1;
        else if (data[i].rating > 4.0)
            imageIcon = Icon2;
        else if (data[i].rating > 3.0)
            imageIcon = Icon3;
        
        //設定藥局經緯度和 Popup 內容
        var mark = L.marker([
            data[i].geometry.location.lat,
            data[i].geometry.location.lng
        ], { icon: imageIcon }
        ).bindPopup(
            '<h1 class="popup-name"> ' + 
                data[i].name + '<h1/>' +
            '<h1 class="popup-star">  [ 星級 ] ' + 
                data[i].rating + '<h1/>' +
            '<h1 class="popup-address">[ 地址 ] ' + 
                data[i].vicinity + '<h1/>', { minWidth:600 ,maxHeight: 500});
        //將圖標加入圖層
        markers.addLayer(mark);
    }
    map.addLayer(markers);
};