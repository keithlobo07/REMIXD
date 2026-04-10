function menuDrop(){
    document.getElementById("myDropdown").classList.toggle("show");
}

function searchAlbum()
{
    console.log("yayay");
}

document.getElementById("search").addEventListener("search", searchAlbum());

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

fetch('/api/album/11755c21-2546-4cb3-9b87-392f4f3c2fa2')
    .then(response => {
        if (!response.ok){
            throw new Error('HTTP error - currrent status ${response.status}');       
        }
        console.log("yippe")
        return response.json();
    })
    .then(data => {
        document.getElementById("albumTitle").innerText = data.albumName;
        document.getElementById("albumCover").src = data.coverArt;
        document.getElementById("albumRelease").innerText = data.releaseDate;
        document.getElementById("albumArtist").innerText = data.artist;
        //document.getElementById("albumRating").innerText = data.avgRating;
        //document.getElementById("albumRatingNo").innerText = data.numReviews;

        //for the stars
        //const rating = parseFloat(data.avgRating);
        //const percent = (rating/5) * 100;

        document.getElementById("filledStars").style.background = `linear-gradient(90deg, #F9E784 ${percent}%, #ccc ${percent}%)`;
    })
    .catch(error => {
        console.error('Error fetching data', error);
        alert('failed to gather data, please try again later')
    });
