$("#seeking_talent").change(function() {
    if (this.checked) {
        alert(this.checked)
        this.value = true
    } else this.value = false
});
//create venue
$("#createVenue").on("click", function(e) {
    //document.getElementById('create-venue-form').onsubmit = function(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const city = document.getElementById('city').value;
    const state = document.getElementById('state').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    const image_link = document.getElementById('image_link').value;
    const facebook_link = document.getElementById('facebook_link').value;
    var seekingbox = document.getElementById('seeking_talent');
    var seeking_talent = true;
    if (seekingbox.checked) {
        seeking_talent = true;
    } else { seeking_talent = false; }
    // alert("seeking_talent")
    const website = document.getElementById('website').value;
    // const genres = document.getElementById('genres').value;
    var genres = [];
    $("#genres :selected").each(function() {
        genres.push($(this).val());
    });
    fetch('/venues/create', {
            method: 'POST',
            body: JSON.stringify({
                'name': name,
                'city': city,
                'state': state,
                'address': address,
                'phone': phone,
                'image_link': image_link,
                'facebook_link': facebook_link,
                'seeking_talent': seeking_talent,
                'website': website,
                'genres': genres
            }),
            headers: {
                'Content-Type': 'application/json',
            }
        })
        // .then(response => response.json())
        // .then(jsonResponse => {
        //     console.log(jsonResponse);
        // })
        .catch(function(error) {
            console.log(error);
        });
})

//create artist
// function createArtist(e) {
//     //document.getElementById('create-artist-form').onsubmit = function(e) {
//     e.preventDefault();
//     const name = document.getElementById('name').value;
//     const city = document.getElementById('city').value;
//     const state = document.getElementById('state').value;
//     const address = document.getElementById('address').value;
//     const phone = document.getElementById('phone').value;
//     const genres = document.getElementById('genres').value;
//     const image_link = document.getElementById('image_link').value;
//     const facebook_link = document.getElementById('facebook_link').value;

//     fetch('/artists/create', {
//             method: 'POST',
//             body: JSON.stringify({
//                 'name': name,
//                 'city': city,
//                 'state': state,
//                 'address': address,
//                 'phone': phone,
//                 'genres': genres,
//                 'image_link': image_link,
//                 'facebook_link': facebook_link
//             }),
//             headers: {
//                 'Content-Type': 'application/json',
//             }
//         })
//         .then(response => response.json())
//         .then(jsonResponse => {
//             console.log(jsonResponse);
//         })
//         .catch(function(e) {
//             console.log('Error occurred ');
//         });
// }

// //create show
// function createShow(e) {
//     //document.getElementById('create-show-form').onsubmit = function(e) {
//     e.preventDefault();
//     const venue_id = document.getElementById('venue_id').value;
//     const artist_id = document.getElementById('artist_id').value;
//     fetch('/shows/create', {
//             method: 'POST',
//             body: JSON.stringify({
//                 'venue_id': venue_id,
//                 'artist_id': artist_id,
//             }),
//             headers: {
//                 'Content-Type': 'application/json',
//             }
//         })
//         .then(response => response.json())
//         .then(jsonResponse => {
//             console.log(jsonResponse);
//         })
//         .catch(function(e) {
//             console.log('Error occurred ');
//         });
// }


// // delete venue
// function deleteItem(e) {
//     console.log("ok " + $(e).attr("data-id"));
//     // const venueId = e.target.dataset['id'];
//     // fetch('/venues/' + venueId, {
//     //         method: 'DELETE'
//     //     })
//     //     .then(function() {
//     //         const item = e.target.parentElement;
//     //         item.remove();
//     //     })
// }