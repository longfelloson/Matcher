async function fetchExchangeRate() {
    try {
        const response = await fetch('/exchange/rate');
        const data = await response.json();
        return data['current-rate'];
    } catch (error) {
        console.error('Error fetching exchange rate:', error);
        return null;
    }
}

async function calculateMoney() {
    const points = document.getElementById('points').value;
    const exchangeRate = await fetchExchangeRate();
    if (exchangeRate) {
        const money = points / exchangeRate;
        document.getElementById('money').value = money.toFixed(2);
    } else {
        document.getElementById('money').value = 'Error';
    }
}

async function selectImage(id) {
    const images = document.querySelectorAll('.carousel-item');
    images.forEach(image => image.classList.remove('selected'));

    const selectedImage = document.getElementById(id);
    selectedImage.classList.add('selected');
}

async function exchangePoints() {
    const points = document.getElementById('points').value;
    const selectedImage = document.querySelector('.carousel-item.selected');
    const destination = selectedImage ? selectedImage.id : '';
    const accountDetails = document.getElementById('account-details').value;

    if (points && destination && accountDetails) {
        try {
            const balanceResponse = await fetch(`/exchange/user-points`);
            if (!balanceResponse.ok) {
                const errorData = await balanceResponse.json();
                alert('Ошибка при получении баланса: ' + (errorData.message || 'Ошибка.'));
                return;
            }

            const balanceData = await balanceResponse.json();
            const userPoints = balanceData.user_points;

            if (parseInt(points) >= userPoints) {
                alert('Недостаточно баллов для обмена');
                return;
            }

            const requestData = {
                points: points,
                destination: destination,
                account_details: accountDetails,
            };

            const exchangeResponse = await fetch('/exchange', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            if (exchangeResponse.ok) {
                alert("Вы успешно обменяли баллы!");

                document.getElementById('points').value = '';
                document.getElementById('account-details').value = '';
                document.getElementById('money').value = '';

                const carouselItems = document.querySelectorAll('.carousel-item');
                carouselItems.forEach(item => item.classList.remove('selected'));
            } else {
                const errorData = await exchangeResponse.json();
                alert(errorData.message || 'Ошибка при обмене баллов');
            }
        } catch (error) {
            alert('Произошла ошибка: ' + error.message);
        }
    } else {
        alert('Пожалуйста, введите сумму, реквизиты и выберите платежную систему');
    }
}
