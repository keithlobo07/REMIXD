export function review_card(review) {
    const card = document.createElement("div");
    card.className = "review-card container-fluid";
    card.id = review.id;
    card.innerHTML =`<div class="card-body">
                        <div class = "container">
                            <div class="row">
                                <div class="col-5">
                                    <!--make link to the usernames profile-->
                                    <!--CHANGE TO USERNAME!!-->
                                    <h5>${review.name}</h5>
                                </div>
                                <div class="col-5 text-right">
                                    <div class="starRating">
                                        <div class="starBackground">★★★★★</div>
                                        <div class="starYellow" style="width: ${review.score * 10}%;">★★★★★</div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <body> ${review.content} </body>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col" style="text-align:right;">` +
                                (review.user_report !== undefined ? `<img src="/static/assets/flag${review.user_report}.png" id="flag-${review.id}" aria-valuenow="${review.user_report}">` : ``) + 
                                (review.is_admin !== undefined ? `<img src="/static/assets/flag0.png" id="admin-${review.id}">` : ``) + 
                                `</div>
                            </div>
                        </div>
                    </div>`
    
    if (review.user_report !== undefined) card.querySelector(`#flag-${review.id}`).addEventListener("mousedown", function(){flag_review(review.albumid, review.id)});


    return card
}

function flag_review(albumid, accountid) {
    const flag = document.getElementById(`flag-${accountid}`)
    flag.ariaValueNow = 1 - flag.ariaValueNow;
    
    const fd = new FormData();
    fd.set('tags', flag.ariaValueNow * 64);

    const r = new Request(`/api/review/${accountid}/${albumid}/tags`, {
        method:"POST",
        body:fd
    });

    fetch(r).then(response => {
        console.log(response)
    });

    flag.src = (flag.ariaValueNow ? "/static/assets/flag0.png" : "/static/assets/flag1.png");
}