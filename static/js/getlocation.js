
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    window.location.href = `/?latitude=${latitude}&longitude=${longitude}`;
}
function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        latitude: params.get('latitude'),
        longitude: params.get('longitude')
    };
}
window.onload = function() {
    const { latitude, longitude } = getQueryParams();
    if (!latitude || !longitude) {
        getLocation();
    }};
