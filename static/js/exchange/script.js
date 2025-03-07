async function fetchExchangeRate() {
    try {
        const response = await fetch('/points/exchange-rate');
        const data = await response.json();
        return data['rate'];
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
    const selectedImage = document.getElementById(id);

    document.querySelectorAll('.carousel-inner img').forEach(img => img.classList.remove('selected'));

    if (!selectedImage.classList.contains('selected')) {
        selectedImage.classList.add('selected');
    }
}


async function exchangePoints() {
    const exchangeRate = await fetchExchangeRate();
    const pointsInput = document.getElementById('points').value;
    const accountDetails = document.getElementById('account-details').value;
    
    // Get the selected image (bank)
    const selectedImage = document.querySelector('.carousel-item.selected');
    const bankId = selectedImage ? selectedImage.id : '';

    if (pointsInput && bankId && accountDetails) {
        try {
            const balanceResponse = await fetch(`/points`);
            if (!balanceResponse.ok) {
                const errorData = await balanceResponse.json();
                alert('Ошибка при получении баланса: ' + (errorData.message || 'Ошибка.'));
                return;
            }

            const balanceData = await balanceResponse.json();
            const userPoints = balanceData.user_points;
            const pointsValue = parseFloat(pointsInput);
            const amount = pointsValue / exchangeRate;

            if (pointsValue > userPoints) {
                alert('Недостаточно баллов для обмена');
                return;
            }

            const requestData = {
                points: pointsValue,
                rate: exchangeRate,
                destination: bankId,
                account: accountDetails,
                amount: amount,
                bank_id: bankId
            };

            const exchangeResponse = await fetch('/exchanges', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData),
            });

            if (exchangeResponse.ok) {
                alert("Вы успешно обменяли баллы!");

                document.getElementById('points').value = '';
                document.getElementById('account-details').value = '';
                document.getElementById('money').value = '';

                document.querySelectorAll('.carousel-item').forEach(item => item.classList.remove('selected'));
            } else {
                const errorData = await exchangeResponse.json();
                alert(errorData.detail?.msg || 'Ошибка при обмене баллов');
            }
        } catch (error) {
            alert('Произошла ошибка: ' + error.message);
        }
    } else {
        alert('Пожалуйста, введите сумму, реквизиты и выберите платежную систему');
    }
}
