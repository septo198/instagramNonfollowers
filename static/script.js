let followers = null;
let followings = null;
let currentPage = 1;
const resultsPerPage = 10;
let nonfollowers = [];

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    document.querySelector('#nonfollowers-list').innerHTML = '';
    document.querySelector('#pagination-controls').innerHTML = '';
    document.getElementById('status').innerText = "Attempting to log in...";
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-store'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').innerText = data.message;
        if (data.status === 'success') 
            getFollowers();
    });
}

function getFollowers() {
    fetch('/get_followers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-store'
        }
    })
    .then(response => response.json())
    .then(data => {
        followers = data.followers;
        document.getElementById('status').innerText = 'Fetched followers';
        getFollowings();
    });
}

function getFollowings() {
    fetch('/get_followings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-store'
        }
    })
    .then(response => response.json())
    .then(data => {
        followings = data.followings;
        document.getElementById('status').innerText = 'Fetched followings';
        determineNonfollowers();
    });
}

function determineNonfollowers() {
    fetch('/determine_nonfollowers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-store'
        },
        body: JSON.stringify({ followers: followers, followings: followings })
    })
    .then(response => response.json())
    .then(data => {
        nonfollowers = data.nonfollowers;
        nonfollowers.sort((a, b) => a.username.localeCompare(b.username));
        currentPage = 1;
        displayResults();
        setupPagination();
        document.getElementById('status').innerText = 'Determined non-followers';
        /*
        const list = document.getElementById('nonfollowers-list');
        list.innerHTML = '';
        data.nonfollowers.forEach(user => {
            const li = document.createElement('li');
            li.innerHTML = `<img src="/proxy_image?url=${encodeURIComponent(user.profile_pic_url)}" alt="${user.username}'s profile picture"> <span>${user.username}</span>`;
            li.onclick = () => window.open(`https://www.instagram.com/${user.username}/`, '_blank');
            list.appendChild(li);
        });
        document.getElementById('status').innerText = 'Determined non-followers';
        */
    });
}

function displayResults() {
    const list = document.getElementById('nonfollowers-list');
    list.innerHTML = ''; 

    const start = (currentPage - 1) * resultsPerPage;
    const end = start + resultsPerPage;
    const paginatedResults = nonfollowers.slice(start, end);

    paginatedResults.forEach(user => {
        const li = document.createElement('li');
        li.innerHTML = `<img src="/proxy_image?url=${encodeURIComponent(user.profile_pic_url)}" alt="${user.username}'s profile picture"> <span>${user.username}</span>`;
        li.onclick = () => window.open(`https://www.instagram.com/${user.username}/`, '_blank');
        list.appendChild(li);
    });
}

function setupPagination() {
    const paginationControls = document.getElementById('pagination-controls');
    paginationControls.innerHTML = '';

    const totalPages = Math.ceil(nonfollowers.length / resultsPerPage);

    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.textContent = i;
        pageButton.onclick = () => {
            currentPage = i;
            displayResults();
        };
        paginationControls.appendChild(pageButton);
    }
}