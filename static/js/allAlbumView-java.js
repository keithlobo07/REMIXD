import { album_card } from "/static/js/components/album_card.js";

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

fetch('/api/album/search?query=riot')
    .then(response => {
        if (!response.ok){
            throw new Error('HTTP error - currrent status ${response.status}');       
        }
        console.log("yippe")
        return response.json();
    })
    .then(data => {
        const container = document.getElementById("albumList");

        data.forEach(album => {
            container.appendChild(album_card(album));
        });

    })
    .catch(error => {
        console.error('Error fetching data', error);
        alert('failed to gather data, please try again later')
    });
