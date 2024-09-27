fetch('/header/url/')
    .then(response => response.text())
    .then(data => {
        document.querySelector('header').innerHTML = data;
    })
    .catch(error => console.log('Error fetching header:', error));
