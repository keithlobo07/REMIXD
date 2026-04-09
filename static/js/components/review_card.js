export function review_card(review) {
    const card = document.createElement("div");
    card.className = "card container-fluid";
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
                                <div class="col" style="text-align:right;">
                                    <img src="/static/assets/heart.png">
                                    <img src="/static/assets/Flag.png">
                                </div>
                            </div>
                        </div>
                    </div>`
    return card
}