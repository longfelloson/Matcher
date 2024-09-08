const tg = window.Telegram.WebApp;
tg.ready(function () {
    const userId = tg.initDataUnsafe.user.id;
    document.addEventListener("DOMContentLoaded", function () {
        const pathArray = window.location.pathname.split('/');
        const productId = pathArray[pathArray.length - 1];

        fetch(`/products/get-product?product_id=${productId}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('product-price').textContent = `Price: $${data.price}`;
                document.getElementById('product-name').textContent = `Name: ${data.name}`;
                document.getElementById('product-description').textContent = `Description: ${data.description}`;
                document.getElementById('product-image').src = `/static/img/products/${data.img_path}`;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    function exchangeProduct() {
        const pathArray = window.location.pathname.split('/');
        const productId = pathArray[pathArray.length - 1];
        const points = 100; // Предположим, что у нас есть количество очков

        fetch('/exchange-points', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_id: userId, points: points, product_id: productId})
        })
            .then(response => response.json())
            .then(data => {
                console.log('Exchange Points:', data);
                showSuccessMessage();
            })
            .catch((error) => {
                console.error('Error:', error);
            });

        fetch('/products/add-user-product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_id: userId, product_id: productId})
        })
            .then(response => response.json())
            .then(data => {
                console.log('Add User Product:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    function showSuccessMessage() {
        const successMessage = document.getElementById('success-message');
        successMessage.style.display = 'block';
        setTimeout(() => {
            successMessage.style.display = 'none';
        }, 3000);
    }

    window.exchangeProduct = exchangeProduct; // Expose the function to the global scope
});