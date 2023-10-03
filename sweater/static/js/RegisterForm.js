$(document).ready(function() {
    // Проверка доступности никнейма
    $('#nickname').on('input', function() {
        var nickname = $(this).val();
        if (nickname.length > 0) {
            $.ajax({
                type: 'POST',
                url: '/check_nickname_availability', // URL маршрута для проверки никнейма
                data: {nickname: nickname},
                success: function(data) {
                    var availabilityMessage = $('#nickname-availability-message');
                    if (data.available) {
                        availabilityMessage.text('никнейм доступен').removeClass('unavailable').addClass('available');
                    } else {
                        availabilityMessage.text('никнейм занят').removeClass('available').addClass('unavailable');
                    }
                }
            });
        } else {
            $('#nickname-availability-message').text('').removeClass('available unavailable');
        }
    });

    // Проверка доступности логина
    $('#login').on('input', function() {
        var login = $(this).val();
        if (login.length > 0) {
            $.ajax({
                type: 'POST',
                url: '/check_login_availability', // URL маршрута для проверки логина
                data: {login: login},
                success: function(data) {
                    var availabilityMessage = $('#login-availability-message');
                    if (data.available) {
                        availabilityMessage.text('логин доступен').removeClass('unavailable').addClass('available');
                    } else {
                        availabilityMessage.text('логин занят').removeClass('available').addClass('unavailable');
                    }
                }
            });
        } else {
            $('#login-availability-message').text('').removeClass('available unavailable');
        }
    });
});