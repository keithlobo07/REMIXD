function writeReview(albumid) {

    const fd = new FormData(document.getElementById('reviewform'));

    fd.set('album_id', albumid)
    fd.set('score', parseInt(fd.get('score')) * 2)

    const request = new Request("/api/review", {
        method:"POST",
        body:fd
    });

    fetch(request).then(response => {
        if (response.ok) {window.location.reload(); return;}
        else console.error("Failed to write review.")
    });
}