function returnSignupInfo(url) {

    const fd = new FormData(document.getElementById('signupForm'));

    if (fd.get('password') != fd.get('confPassword')) {
        // show message to the user about passwords not matching
        console.error("passwords dont match");
    } else {

        fd.set('password', sha256(fd.get('password')))
        fd.delete('confPassword')

        const request = new Request(url, {
            method:"PUT",
            body:fd
        });

        fetch(request).then(response => {
            if (response.status == 201) {
                fetch("/home").then(response => {
                    window.location.href = response.url
                })
            } else {
                // show message to the user about email being taken
                
            }
        });
    }
}