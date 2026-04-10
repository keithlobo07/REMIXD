function menuDrop(){
    document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event){
    if (!event.target.matches('.dropbtn')){
        var dropdowns=this.document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++){
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')){
                openDropdown.classList.remove('show');
            }
        }
    }
}

import {review_card} from "./components/review_card.js";

export function add_reviews(albumid) {
    review_section = document.getElementById("review_section")

    fetch(`/api/album/${albumid}/reviews`).then(response => {
        return response.json()}).then(data => {
            let reviews = data.reviews;
            reviews.forEach(review => {                
                review_section.appendChild(review_card(review))
            });
        })
}


fetch('/api/album/11755c21-2546-4cb3-9b87-392f4f3c2fa2')
    .then(response => {
        if (!response.ok){
            throw new Error('HTTP error - currrent status ${response.status}');       
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("albumTitle").innerText = data.strAlbum;
        document.getElementById("albumCover").src = data.albumArt;
        document.getElementById("albumRelease").innerText = data.intYearReleased;
        document.getElementById("albumArtist").innerText = data.strArtist;
        document.getElementById("albumRating").innerText = data.avgRating;
        document.getElementById("albumRatingNo").innerText = data.numReviews;

        //for the stars
        const rating = parseFloat(data.avgRating);
        const percent = (rating/5) * 100;

        document.getElementById("filledStars").style.width = "60%";

        //for the tracklist
        const list = document.getElementById("tracklist");
        list.innerHTML = TextTrackList.map(track => '<li>${track}</li>').join("");
    })
    .catch(error => {
        console.error('Error fetching data', error);
        alert('failed to gather data, please try again later')
    });
