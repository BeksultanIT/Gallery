function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addPhotoToFavorites(photoId) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/api/v1/photo/${photoId}/favorites/add/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const addBtn = document.getElementById(`add-photo-${photoId}`);
            if (addBtn) {
                addBtn.style.display = 'none';
            }

            const removeBtn = document.getElementById(`remove-photo-${photoId}`);
            if (removeBtn) {
                removeBtn.style.display = 'inline-block';
            }

            const countElement = document.getElementById(`photo-count-${photoId}`);
            if (countElement) {
                countElement.textContent = data.favorites_count;
            }

            console.log(data.message);
        } else {
            console.error('Ошибка при добавлении в избранное:', data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка запроса:', error);
    });
}

function removePhotoFromFavorites(photoId) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/api/v1/photo/${photoId}/favorites/remove/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const addBtn = document.getElementById(`add-photo-${photoId}`);
            if (addBtn) {
                addBtn.style.display = 'inline-block';
            }

            const removeBtn = document.getElementById(`remove-photo-${photoId}`);
            if (removeBtn) {
                removeBtn.style.display = 'none';
            }

            const countElement = document.getElementById(`photo-count-${photoId}`);
            if (countElement) {
                countElement.textContent = data.favorites_count;
            }

            console.log(data.message);
        } else {
            console.error('Ошибка при удалении из избранного:', data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка запроса:', error);
    });
}

function addAlbumToFavorites(albumId) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/api/v1/album/${albumId}/favorites/add/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const addBtn = document.getElementById(`add-album-${albumId}`);
            if (addBtn) {
                addBtn.style.display = 'none';
            }

            const removeBtn = document.getElementById(`remove-album-${albumId}`);
            if (removeBtn) {
                removeBtn.style.display = 'inline-block';
            }

            const countElement = document.getElementById(`album-count-${albumId}`);
            if (countElement) {
                countElement.textContent = data.favorites_count;
            }

            console.log(data.message);
        } else {
            console.error('Ошибка при добавлении альбома в избранное:', data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка запроса:', error);
    });
}

function removeAlbumFromFavorites(albumId) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/api/v1/album/${albumId}/favorites/remove/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Показываем кнопку "Добавить в избранное"
            const addBtn = document.getElementById(`add-album-${albumId}`);
            if (addBtn) {
                addBtn.style.display = 'inline-block';
            }

            const removeBtn = document.getElementById(`remove-album-${albumId}`);
            if (removeBtn) {
                removeBtn.style.display = 'none';
            }

            const countElement = document.getElementById(`album-count-${albumId}`);
            if (countElement) {
                countElement.textContent = data.favorites_count;
            }

            console.log(data.message);
        } else {
            console.error('Ошибка при удалении альбома из избранного:', data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка запроса:', error);
    });
}