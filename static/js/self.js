//create venue
document.getElementById('form').onsubmit = function(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const city = document.getElementById('city').value;
    const state = document.getElementById('state').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    const image_link = document.getElementById('image_link').value;
    const facebook_link = document.getElementById('facebook_link').value;

    fetch('/venues/create', {
            method: 'POST',
            body: JSON.stringify({
                'name': name,
                'city': city,
                'state': state,
                'address': address,
                'phone': phone,
                'image_link': image_link,
                'facebook_link': facebook_link
            }),
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(jsonResponse => {
            console.log(jsonResponse);
            document.getElementById('venue-create-msg').innerHTML = "Venue " + jsonResponse["name"] + " created!";
            document.getElementByClassName('success').className = '';
            document.getElementByClassName('error').className = 'hidden';
        })
        .catch(function(e) {
            console.log('Error occurred ');
            document.getElementsByClassName('error').className = '';
        });
}