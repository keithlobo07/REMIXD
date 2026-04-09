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