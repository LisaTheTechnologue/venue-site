//create venue
document.getElementById('create-venue-form').onsubmit = function(e) {
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
        })
        .catch(function(e) {
            console.log('Error occurred ');
        });
}

//create artist
document.getElementById('create-artist-form').onsubmit = function(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const city = document.getElementById('city').value;
    const state = document.getElementById('state').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    const genres = document.getElementById('genres').value;
    const image_link = document.getElementById('image_link').value;
    const facebook_link = document.getElementById('facebook_link').value;

    fetch('/artists/create', {
            method: 'POST',
            body: JSON.stringify({
                'name': name,
                'city': city,
                'state': state,
                'address': address,
                'phone': phone,
                'genres': genres,
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
        })
        .catch(function(e) {
            console.log('Error occurred ');
        });
}

//create show
document.getElementById('create-show-form').onsubmit = function(e) {
    e.preventDefault();
    const venue_id = document.getElementById('venue_id').value;
    const artist_id = document.getElementById('artist_id').value;
    fetch('/shows/create', {
            method: 'POST',
            body: JSON.stringify({
                'venue_id': venue_id,
                'artist_id': artist_id,
            }),
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(jsonResponse => {
            console.log(jsonResponse);
        })
        .catch(function(e) {
            console.log('Error occurred ');
        });
}