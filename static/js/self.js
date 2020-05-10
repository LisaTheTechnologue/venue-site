// // $("#seeking_talent").change(function() {
// //     if (this.checked) {
// //         alert(this.checked)
// //         this.value = true
// //     } else this.value = false
// // });
// //create venue
// // $("#createVenue").on("click", function(e) {
// //     //document.getElementById('create-venue-form').onsubmit = function(e) {
// //     e.preventDefault();
// //     const name = document.getElementById('name').value;
// //     const city = document.getElementById('city').value;
// //     const state = document.getElementById('state').value;
// //     const address = document.getElementById('address').value;
// //     const phone = document.getElementById('phone').value;
// //     const image_link = document.getElementById('image_link').value;
// //     const facebook_link = document.getElementById('facebook_link').value;
// //     const seeking_description = document.getElementById('seeking_description').value;
// //     var seekingbox = document.getElementById('seeking_talent');
// //     var seeking_talent = true;
// //     if (seekingbox.checked) {
// //         seeking_talent = true;
// //     } else { seeking_talent = false; }
// //     // alert("seeking_talent")
// //     const website = document.getElementById('website').value;
// //     // const genres = document.getElementById('genres').value;
// //     var genres = [];
// //     $("#genres :selected").each(function() {
// //         genres.push($(this).val());
// //     });
// //     fetch('/venues/create', {
// //             method: 'POST',
// //             body: JSON.stringify({
// //                 'name': name,
// //                 'city': city,
// //                 'state': state,
// //                 'address': address,
// //                 'phone': phone,
// //                 'image_link': image_link,
// //                 'facebook_link': facebook_link,
// //                 'seeking_talent': seeking_talent,
// //                 'seeking_description': seeking_description,
// //                 'website': website,
// //                 'genres': genres
// //             }),
// //             headers: {
// //                 'Content-Type': 'application/json',
// //             }
// //         })
// //         .catch(function(error) {
// //             console.log(error);
// //         });
// // })

// //create artist
// // $("#createArtist").on("click", function(e) {
// //     e.preventDefault();
// //     const name = document.getElementById('name').value;
// //     const city = document.getElementById('city').value;
// //     const state = document.getElementById('state').value;
// //     const address = document.getElementById('address').value;
// //     const phone = document.getElementById('phone').value;
// //     const image_link = document.getElementById('image_link').value;
// //     const facebook_link = document.getElementById('facebook_link').value;
// //     const seeking_description = document.getElementById('seeking_description').value;
// //     var seekingbox = document.getElementById('seeking_talent');
// //     var seeking_talent = true;
// //     if (seekingbox.checked) {
// //         seeking_talent = true;
// //     } else { seeking_talent = false; }
// //     // alert("seeking_talent")
// //     const website = document.getElementById('website').value;
// //     // const genres = document.getElementById('genres').value;
// //     var genres = [];
// //     $("#genres :selected").each(function() {
// //         genres.push($(this).val());
// //     });
// //     fetch('/artists/create', {
// //             method: 'POST',
// //             body: JSON.stringify({
// //                 'name': name,
// //                 'city': city,
// //                 'state': state,
// //                 'address': address,
// //                 'phone': phone,
// //                 'image_link': image_link,
// //                 'facebook_link': facebook_link,
// //                 'seeking_talent': seeking_talent,
// //                 'seeking_description': seeking_description,
// //                 'website': website,
// //                 'genres': genres
// //             }),
// //             headers: {
// //                 'Content-Type': 'application/json',
// //             }
// //         })
// //         .then(json)
// //         .catch(function(error) {
// //             console.log(error);
// //         });

// // })

// // //create show
// // $("#createShow").on("click", function(e) {
// //     e.preventDefault();
// //     const venue_id = document.getElementById('venue_id').value;
// //     const artist_id = document.getElementById('artist_id').value;
// //     const start_time = document.getElementById('start_time').value;

// //     fetch('/shows/create', {
// //             method: 'POST',
// //             body: JSON.stringify({
// //                 'venue_id': venue_id,
// //                 'artist_id': artist_id,
// //                 'start_time': start_time
// //             }),
// //             headers: {
// //                 'Content-Type': 'application/json',
// //             }
// //         })
// //         .catch(function(error) {
// //             console.log(error);
// //         });
// // })

// //update venue
// // $("#updateVenue").on("click", function(e) {
// //         e.preventDefault();
// //         const venueid = e.target.dataset['id']
// //             // alert(venueid)
// //         const name = document.getElementById('name').value;
// //         const city = document.getElementById('city').value;
// //         const state = document.getElementById('state').value;
// //         const address = document.getElementById('address').value;
// //         const phone = document.getElementById('phone').value;
// //         const image_link = document.getElementById('image_link').value;
// //         const facebook_link = document.getElementById('facebook_link').value;
// //         const seeking_description = document.getElementById('seeking_description').value;
// //         var seekingbox = document.getElementById('seeking_talent');
// //         var seeking_talent = true;
// //         if (seekingbox.checked) {
// //             seeking_talent = true;
// //         } else { seeking_talent = false; }

// //         const website = document.getElementById('website').value;
// //         // const genres = document.getElementById('genres').value;
// //         var genres = [];
// //         $("#genres :selected").each(function() {
// //             genres.push($(this).val());
// //         });
// //         fetch('/venues/' + venueid + '/edit', {
// //                 method: 'POST',
// //                 body: JSON.stringify({
// //                     'id': venueid,
// //                     'name': name,
// //                     'city': city,
// //                     'state': state,
// //                     'address': address,
// //                     'phone': phone,
// //                     'image_link': image_link,
// //                     'facebook_link': facebook_link,
// //                     'seeking_talent': seeking_talent,
// //                     'seeking_description': seeking_description,
// //                     'website': website,
// //                     'genres': genres
// //                 }),
// //                 headers: {
// //                     'Content-Type': 'application/json'
// //                 }
// //             })
// //             .catch(function(error) {
// //                 console.log(error);
// //             });
// //     })
// // delete venue
// $("#deleteVenue").on("click", function(e) {
//     console.log("ok " + $(e).attr("data-id"));
//     // const venueId = e.target.dataset['id'];
//     // fetch('/venues/' + venueId, {
//     //         method: 'DELETE'
//     //     })
//     //     .then(function() {
//     //         const item = e.target.parentElement;
//     //         item.remove();
//     //     })
// })