function toggleNavbar() {
    const navbar = document.querySelector('.navbar');
    const mainContent = document.querySelector('.main-content');
    navbar.classList.toggle('collapsed');
}

document.querySelectorAll('.message-thread').forEach(item => {
    item.addEventListener('mouseover', () => {
        item.style.transform = 'translateX(5px)';
    });
    item.addEventListener('mouseout', () => {
        item.style.transform = 'translateX(0)';
    });
});

// Keep only one version of toggleNotifications
function toggleNotifications() {
    const notificationContainer = document.querySelector('.right-content');
    if (window.innerWidth <= 768) {
        const navbar = document.querySelector('.navbar');
        navbar.classList.add('collapsed');
        document.querySelector('.navbar-overlay').style.display = 'none';
        notificationContainer.classList.toggle('active');
    } else {
        if (notificationContainer.style.opacity === '0' || notificationContainer.style.opacity === '') {
            notificationContainer.style.display = 'block';
            setTimeout(() => {
                notificationContainer.style.opacity = '1';
                notificationContainer.style.visibility = 'visible';
            }, 10);
        } else {
            notificationContainer.style.opacity = '0';
            notificationContainer.style.visibility = 'hidden';
            setTimeout(() => {
                notificationContainer.style.display = 'none';
            }, 300);
        }
    }
}

function toggleSave(saveIcon) {
    saveIcon.classList.toggle('far');
    saveIcon.classList.toggle('fas');
    saveIcon.classList.toggle('saved');
}

document.getElementById('postImage').addEventListener('change', function(e) {
    document.getElementById('fileName').textContent = this.files[0]?.name || '';
});



document.getElementById('articleSearch').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const articles = document.querySelectorAll('.article-card');

    articles.forEach(article => {
        const title = article.querySelector('.article-title').textContent.toLowerCase();
        article.style.display = title.includes(searchTerm) ? 'block' : 'none';
    });
});

function showArticleForm() {
    console.log('Show article form modal');
}

function toggleLike(event, postId) {
    event.preventDefault();

    const likeButton = event.target;
    const likeCountElement = likeButton.closest('.post-container').querySelector('.post-likes');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/post/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'post_id': postId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.liked !== undefined) {
                if (data.liked) {
                    likeButton.classList.remove("far");
                    likeButton.classList.add("fas");
                } else {
                    likeButton.classList.remove("fas");
                    likeButton.classList.add("far");
                }

                likeCountElement.textContent = `${data.like_count} likes`;
            }
        })
        .catch(error => console.error('Error:', error));
}


function toggleBookmark(event, postId) {
    event.preventDefault();

    const bookmarkButton = event.target;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/post/bookmark/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'post_id': postId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.bookmarked !== undefined) {
                if (data.bookmarked) {
                    bookmarkButton.classList.add('fas');
                    bookmarkButton.classList.remove('far');
                } else {
                    bookmarkButton.classList.remove('fas');
                    bookmarkButton.classList.add('far');
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

function UpdateSearch() {
    const urlParams = new URLSearchParams(window.location.search);
    const searchValue = urlParams.get("search");

    if (searchValue) {
        document.getElementById("search").value = searchValue;
    }
}

window.onload = UpdateSearch;

document.getElementById("search").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        const searchInput = document.getElementById("search").value;
        const urlParams = new URLSearchParams(window.location.search);

        if (searchInput) {
            urlParams.set("search", searchInput);
        } else {
            urlParams.delete("search");
        }

        document.getElementById("searchForm").action = `${window.location.pathname}?${urlParams.toString()}`;

        document.getElementById("searchForm").submit();
    }
});


function toggleMobileMenu() {
    const navbar = document.querySelector('.navbar');
    const overlay = document.querySelector('.navbar-overlay');

    navbar.classList.toggle('collapsed');
    overlay.style.display = navbar.classList.contains('collapsed') ? 'none' : 'block';
}

function toggleNotifications() {
    const navbar = document.querySelector('.navbar');
    const notifications = document.querySelector('.right-content');

    if (window.innerWidth <= 768) {
        navbar.classList.add('collapsed');
        document.querySelector('.navbar-overlay').style.display = 'none';
        notifications.classList.toggle('active');
    } else {
        notifications.style.display = notifications.style.display === 'block' ? 'none' : 'block';
    }
}

document.querySelector('.navbar-overlay').addEventListener('click', () => {
    toggleMobileMenu();
});

window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        document.querySelector('.navbar').classList.remove('collapsed');
        document.querySelector('.right-content').classList.remove('active');
    }
});