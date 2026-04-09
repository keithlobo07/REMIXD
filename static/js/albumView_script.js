import {review_card} from "./components/review_card.js";

export function add_reviews(albumid) {
    review_section = document.getElementById("review_section")

    console.log("func run")

    fetch(`/api/album/${albumid}/reviews`).then(response => {
        return response.json()}).then(data => {
            let reviews = data.reviews;
            console.log(reviews);
            reviews.forEach(review => {
                review_section.appendChild(review_card(review))
            });
        })
}


