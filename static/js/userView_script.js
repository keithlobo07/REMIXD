import {review_card} from "./components/review_card.js";

export function add_reviews(userid) {
    review_section = document.getElementById("review_section")

    fetch(`/api/user/${userid}/reviews`).then(response => {
        return response.json()}).then(data => {
            let reviews = data.reviews;
            reviews.forEach(review => {                
                review_section.appendChild(review_card(review))
            });
        })
}

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