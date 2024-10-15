function getLocation() {
    document.getElementById('statusMessage').innerText = "Getting your location!";
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById('location').value = `${latitude}, ${longitude}`;
            document.getElementById('statusMessage').innerText = ""; // Clear message on success
        }, function(error) {
            console.error('Geolocation error:', error);
            document.getElementById('statusMessage').innerText = "Unable to retrieve your location.";
        });
    } else {
        document.getElementById('statusMessage').innerText = "Geolocation is not supported by this browser.";
    }
}

function submit_details() {
    const bloodType = document.getElementById('blood_type').value;
    const location = document.getElementById('location').value;

    const payload = {
        blood_type: bloodType,
        location: location
    };

    fetch('/blood/find_blood_banks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        alert('Details submitted successfully: ' + JSON.stringify(data));
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
