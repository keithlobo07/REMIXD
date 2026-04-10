export function album_card(album) {
    const card = document.createElement("div");
    card.className = "album-card container-fluid";
    card.id = album.idAlbum;
    card.innerHTML =`<div class="card" id="card">
                        <div class="card-body">
                            <div class = "container">
                                <div class="row">
                                    <div class="col-3">
                                        <img src="${album.coverArt}" alt="album cover" style="width: clamp(100px, 13vw, 200px); padding :5px;">
                                    </div>
                                    <div class="col-9" style="padding-left: 5%;">
                                        <div class="row">
                                            <div class="col-5">
                                                <h5 id="${album.albumName}">${album.albumName}</h5>
                                            </div>
                                            <div class="col-7 text-right">
                                                <div class="starRating">
                                                </div>          
                                            </div>
                                        </div>
                                        <p id="${album.artist}">${album.artist}</p>
                                        <p id="${album.releaseDate}">${album.releaseDate}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`;

    return card
}