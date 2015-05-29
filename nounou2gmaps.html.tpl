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
        zoom: 13,
        center: new google.maps.LatLng(43.185453, 5.608864),
        mapTypeId: 'terrain'
    };
    map = new google.maps.Map($('#map_canvas')[0], myOptions);

    $.getJSON('/nounous/marker.json', null, function (result) {
        $.each(result.nounous, function (key, nounou) {
          $.getJSON('http://maps.googleapis.com/maps/api/geocode/json?address='+nounou.address+'&sensor=false', null, function (data) {
            if (data.results[0] === undefined) {
              console.log("nounou: " + nounou.title + " don't have a valid address: " + nounou.address);
            }
            else {
              var p = data.results[0].geometry.location;
              var latlng = new google.maps.LatLng(p.lat, p.lng);
              var marker = new google.maps.Marker({
                  position: latlng,
                  map: map,
                  title: nounou.title
              });
              var infowindow = new google.maps.InfoWindow({
                  content: "<h4>" + nounou.title + "</h4></br>" + nounou.address + "</br><strong>" + nounou.phone + "</strong></br>" + nounou.extra 
              });
              google.maps.event.addListener(marker, 'click', function() {
                 infowindow.open(map, marker);
              });
            }
          });
        });
    });

});
    </script>
    <style>
      html, body, #map_canvas {
        height: 100%;
        margin: 0px;
        padding: 0px
      }
    </style>
</head>
<body class="container" ng-app="prelaunchApp">
<div id="map_canvas"></div></body>
</html>
