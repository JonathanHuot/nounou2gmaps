<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr" dir="ltr">
<head>
    <title>Adresses des Nounous</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
    <script src="http://maps.google.com/maps/api/js?sensor=false&.js"></script>
    <script type="text/javascript">
$(document).ready(function () {
    var map;
    var elevator;
    var myOptions = {
        zoom: 12,
        center: new google.maps.LatLng(43.185453, 5.608864),
        mapTypeId: 'terrain'
    };
    map = new google.maps.Map($('#map_canvas')[0], myOptions);

    $.getJSON('/marker.json', null, function (addresses) {
        $.each(addresses.addresses, function (key, address) {
          if(address !== null) {
          $.getJSON('http://maps.googleapis.com/maps/api/geocode/json?address='+address+'&sensor=false', null, function (data) {
              var p = data.results[0].geometry.location
              var latlng = new google.maps.LatLng(p.lat, p.lng);
              var marker = new google.maps.Marker({
                  position: latlng,
                  map: map,
                  title: addresses.titles[key]
              });
              var infowindow = new google.maps.InfoWindow({
                  content: addresses.titles[key] + "</br>" + address + "</br>" + addresses.phones[key] + "</br>" + addresses.extras[key] 
              });
              google.maps.event.addListener(marker, 'click', function() {
                 infowindow.open(map, marker);
              });
          });
          }
        });
    });

});
    </script>
</head>
<body class="container" ng-app="prelaunchApp">
<div id="map_canvas" style="width: 500px; height: 500px;"></div></body>
</html>
