/*
 * This method is invoked as a callback when maps has finished loading
 */
function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 15
    });
    var infoWindow = new google.maps.InfoWindow({map: map});
    
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            console.log(pos);
            map.setCenter(pos);
            addMarkers(map,position);
        }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }
}

/*
 * Request the stop closest to the given location
 * and add markers to the map for each of them.
 */
function addMarkers(map, position) {
    var xhttp = new XMLHttpRequest();
    xhttp.open('GET', '/location?lat='+position.coords.latitude+'&lon='+position.coords.longitude,true);
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var response = JSON.parse(xhttp.responseText);
            _.each(response, function(location) {
                var p = {
                    lat: location.lat,
                    lng: location.lng
                };
                console.log(p);
                var m = new google.maps.Marker({
                    position: p,
                    map : map,
                    title : location.name
                });
                markerInfo(m,location);
            });
        }
    }
    xhttp.send();
}

/*
 * Setup click handler for markes, request next departures, and update table.
 */
function markerInfo(marker,location) {
    var infowindow = new google.maps.InfoWindow({
        content: location.name
    });
    
    marker.addListener('click', function() {
        infowindow.open(marker.get('map'), marker);

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET', '/departures?id='+location.id,true);
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var response = JSON.parse(xhttp.responseText);
                var table = document.getElementById("departures");
                table.innerHTML = '';
                _.each(response.reverse(), function(departure) {
                    var row = table.insertRow(0);
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    var cell3 = row.insertCell(2);
                    
                    // Add some text to the new cells:
                    cell1.innerHTML = departure.name;
                    cell2.innerHTML = departure.direction;
                    cell3.innerHTML = departure.time;
                });
            }
        };
        xhttp.send();
    });
    
}

/*
 * Show an error message if geolocation was not possible
 */
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
}
