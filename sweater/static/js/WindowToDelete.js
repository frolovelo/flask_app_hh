const openModalButton = document.getElementById("open-modal-btn");
        const modal = document.getElementById("my-modal");
        const confirmDeleteButton = document.getElementById("confirm-delete-btn");
        const cancelDeleteButton = document.getElementById("cancel-delete-btn");
        const cancelxDeleteButton = document.getElementById("cancel-deletex-btn");

        openModalButton.addEventListener("click", function () {
            modal.style.display = "flex";
        });

        confirmDeleteButton.addEventListener("click", function () {
            // Отправляем POST-запрос на URL '/delete_account'
            fetch("/delete_account", {
                method: "POST",
            })
            .then(response => {
                if (response.status === 200) {
                    // Успешный ответ от сервера
                    window.location.href = "/index";
                } else {
                    // Обработка ошибки, если есть
                    console.error("Произошла ошибка: " + response.status);
                }
            })
            .catch(error => {
                // Обработка ошибок сети или других ошибок
                console.error("Произошла ошибка: " + error);
            });
        });

        cancelDeleteButton.addEventListener("click", function () {
            modal.style.display = "none"; // Закрыть модальное окно при отмене
        });

        cancelxDeleteButton.addEventListener("click", function () {
            modal.style.display = "none"; // Закрыть модальное окно при отмене
        });