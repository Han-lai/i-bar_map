var map = L.map("map", {
  center: [25.037801, 121.548855],
  zoom: 17
});

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


var blueIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [56, 56],
  iconAnchor: [43, 86],
  popupAnchor: [1, -86],
  shadowSize: [41, 41]
});

var yellowIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [56, 56],
  iconAnchor: [43, 86],
  popupAnchor: [1, -86],
  shadowSize: [41, 41]
});

var redIcon = new L.Icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [56, 56],
    iconAnchor: [43, 86],
    popupAnchor: [1, -86],
    shadowSize: [41, 41]
});

var blackIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [36, 36],
    iconAnchor: [43, 86],
    popupAnchor: [1, -86],
    shadowSize: [41, 41]
});

var imageClass = [" blackIcon", "redIcon", "yellowIcon", "blueIcon"];
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
            imageIcon = redIcon;
        else if (data[i].rating > 4.0)
            imageIcon = yellowIcon;
        else if (data[i].rating > 3.0)
            imageIcon = blueIcon;

        //設定藥局經緯度和 Popup 內容
        var mark = L.marker([
            data[i].geometry.location.lat,
            data[i].geometry.location.lng
        ], { icon: imageIcon }
        ).bindPopup(
            '<p class="popup-name"> [  店名 ]' + 
                data[i].name + '<p/>' +
            '<p class="popup-phone">  [ 星級 ] ' + 
                data[i].rating + '<p/>' +
            '<p class="popup-address">[ 地址 ] ' + 
                data[i].vicinity + '<p/>');
        //將圖標加入圖層
        markers.addLayer(mark);
    }
    map.addLayer(markers);
};