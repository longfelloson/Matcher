async function fetchExchangeRate() {
    try {
        const response = await fetch('/get-exchange-rate');
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

function selectImage(id) {
    // Remove 'selected' class from all images
    const images = document.querySelectorAll('.carousel-item');
    images.forEach(image => image.classList.remove('selected'));

    // Add 'selected' class to clicked image
    const selectedImage = document.getElementById(id);
    selectedImage.classList.add('selected');
}

function exchangePoints() {
    const points = document.getElementById('points').value;
    const selectedImage = document.querySelector('.carousel-item.selected');
    const destination = selectedImage ? selectedImage.id : '';

    const accountDetails = document.getElementById('account-details').value;

    if (points && destination && accountDetails) {
        const requestData = {
            points: points,
            destination: destination,
            account_details: accountDetails,
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