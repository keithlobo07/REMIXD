import { review_card } from "./components/review_card.js";

function add_reviews(albumid) {
  review_section = document.getElementById("review_section");

  fetch(`/api/album/${albumid}/reviews`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let reviews = data.reviews;
      reviews.forEach((review) => {
        review_section.appendChild(review_card(review));
      });
    });
}

fetch('/api/album/11755c21-2546-4cb3-9b87-392f4f3c2fa2')
    .then(response => {
        if (!response.ok){
            throw new Error('HTTP error - currrent status ${response.status}');       
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("albumTitle").innerText = data.albumName;
        document.getElementById("albumCover").src = data.coverArt;
        document.getElementById("albumRelease").innerText = data.releaseDate;
        document.getElementById("albumArtist").innerText = data.artist;
        document.getElementById("albumRating").innerText = data.avgScore/2;
        document.getElementById("albumRatingNo").innerText = data.numReviews;
fetch("/api/album/11755c21-2546-4cb3-9b87-392f4f3c2fa2")
  .then((response) => {
    if (!response.ok) {
      throw new Error("HTTP error - currrent status ${response.status}");
    }
    return response.json();
  })
  .then((data) => {
    document.getElementById("albumTitle").innerText = data.albumName;
    document.getElementById("albumCover").src = data.coverArt;
    document.getElementById("albumRelease").innerText = data.releaseDate;
    document.getElementById("albumArtist").innerText = data.artist;
    //document.getElementById("albumRating").innerText = data.avgRating;
    //document.getElementById("albumRatingNo").innerText = data.numReviews;

        /*for the stars
        const rating = parseFloat(data.avgRating);
        const percent = (rating / 5) * 100;*/

    //document.getElementById("filledStars").style.width = "60%";

    //for the tracklist
    const tracks = document.getElementById("tracklist");
    data.trackList.forEach((track) => {
      let trackElement = document.createElement("li");
      trackElement.innerText = track.name;
      tracks.appendChild(trackElement);
    });
  })
  .catch((error) => {
    console.error("Error fetching data", error);
    alert("failed to gather data, please try again later");
  });
