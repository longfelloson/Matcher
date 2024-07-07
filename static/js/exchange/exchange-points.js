let tg = window.Telegram.WebApp;

tg.ready(function () {
    document.getElementById('exchange-button').addEventListener('click', exchangePoints);

    function exchangePoints() {
        const points = document.getElementById('points').value;
        const details = document.getElementById('details').value;
        const destination = document.getElementById('destination').value;

        if (points && details && destination) {
            const requestData = {
                user_id: tg.initDataUnsafe.user.id,
                points: points,
                details: details,
                destination: destination
            };

            fetch('/exchange-points', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            })
                .then(response => {
                    if (response.ok) {
                        document.getElementById('result-message').textContent = 'Успешно обменяно';
                    } else {
                        document.getElementById('result-message').textContent = 'Ошибка при обмене';
                        document.getElementById('result-message').style.color = 'red';
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    document.getElementById('result-message').textContent = 'Ошибка при обмене';
                    document.getElementById('result-message').style.color = 'red';
                });
        } else {
            alert('Пожалуйста, введите сумму, реквизиты и выберите платежную систему.');
        }
    }
});