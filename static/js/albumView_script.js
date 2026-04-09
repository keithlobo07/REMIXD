console.log("JS is running");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM is ready");

    const el = document.getElementById("reviewContent");
    console.log("reviewContent element:", el);
});



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

fetch('/api/album/11755c21-2546-4cb3-9b87-392f4f3c2fa2/reviews')
    .then(response => {
        if (!response.ok){
            throw new Error(`HTTP error - currrent status ${response.status}`);       
        }
        return response.json();
    })
    .then(data => {
        const review = data.reviews[0];

        document.getElementById("reviewContent").innerHTML = review.content;
        document.getElementById("username").innerText = review.name;
        document.getElementById("userRating").innerText = review.score
    })
    .catch(error => {
        console.error('Error fetching data', error);
        alert('failed to gather data, please try again later')
    });