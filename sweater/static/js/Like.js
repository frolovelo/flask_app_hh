// Лайки смена цвета и обновление значения
    document.querySelectorAll('.like-button').forEach(function(likeButton) {
    likeButton.addEventListener('click', function() {
        var postId = this.getAttribute('data-post-id');

        fetch('/like_post/' + postId, {
            method: 'POST'
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            var likeCount = data.likes;
            var isLiked = data.is_liked;

            likeButton.innerHTML = '❤ ' + likeCount;

            // Переключаем класс "liked" на кнопке
            likeButton.classList.toggle('liked', isLiked);
        });
    });
});

    // Чекбокс для показа только моих записей
// function filterVacancies()
//     var checkbox = document.getElementById('myVacanciesCheckbox');
//     if (checkbox.checked)
//        // Если чекбокс отмечен, добавьте параметр my_vacancies=true к текущему URL#}
//        window.location.href = window.location.pathname + '?my_vacancies=true';
//     else
//        // Если чекбокс не отмечен, удалите параметр my_vacancies из текущего URL#}
//        window.location.href = window.location.pathname;


