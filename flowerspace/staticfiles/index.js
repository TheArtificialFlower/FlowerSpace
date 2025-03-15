// Toggle Navbar
function toggleNavbar() {
    const navbar = document.querySelector('.navbar');
    const overlay = document.querySelector('.navbar-overlay');
    navbar.classList.toggle('collapsed');
    if (window.innerWidth <= 768) {
        overlay.style.display = navbar.classList.contains('collapsed') ? 'none' : 'block';
    }
}





// Overlay Click to Close Navbar
document.querySelector('.navbar-overlay').addEventListener('click', () => {
    toggleNavbar();
});

// Adjust on Resize
window.addEventListener('resize', () => {
    const navbar = document.querySelector('.navbar');
    const notifications = document.querySelector('.right-content');
    if (window.innerWidth > 768) {
        navbar.classList.remove('collapsed');
        notifications.classList.remove('active');
        document.querySelector('.navbar-overlay').style.display = 'none';
    }
});

// Initial Setup
document.addEventListener('DOMContentLoaded', () => {
    if (window.innerWidth <= 768) {
        document.querySelector('.navbar').classList.add('collapsed');
    }
});

// Keep Your Existing Functions Unchanged
document.querySelectorAll('.message-thread').forEach(item => {
    item.addEventListener('mouseover', () => {
        item.style.transform = 'translateX(5px)';
    });
    item.addEventListener('mouseout', () => {
        item.style.transform = 'translateX(0)';
    });
});

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
        body: JSON.stringify({ 'post_id': postId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.liked !== undefined) {
            likeButton.classList.toggle('fas', data.liked);
            likeButton.classList.toggle('far', !data.liked);
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
        body: JSON.stringify({ 'post_id': postId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.bookmarked !== undefined) {
            bookmarkButton.classList.toggle('fas', data.bookmarked);
            bookmarkButton.classList.toggle('far', !data.bookmarked);
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



function toggleNotifications() {
    const navbar = document.querySelector('.navbar');
    const notificationContainer = document.querySelector('.right-content');
    const overlay = document.querySelector('.navbar-overlay');

    if (window.innerWidth <= 768) { // Mobile (screen width ≤ 768px)
        notificationContainer.classList.toggle('active');
        if (notificationContainer.classList.contains('active')) {
            navbar.classList.add('collapsed'); // Collapse navbar when notifications open
            overlay.style.display = 'none'; // Hide overlay
        } else {
            // Optionally keep navbar collapsed or adjust based on your preference
            // For now, we’ll leave it collapsed unless toggled elsewhere
            overlay.style.display = 'none'; // Ensure overlay stays hidden when closing notifications
        }
    } else { // Desktop (>768px)
        // Toggle display between block and none
        notificationContainer.style.display =
            notificationContainer.style.display === 'block' ? 'none' : 'block';
    }
}


