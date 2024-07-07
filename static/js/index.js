function fetchProducts() {
    return fetch('/products/get-products')
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                return data;
            } else {
                throw new Error('Некорректный формат данных');
            }
        });
}

function displayProducts(products) {
    const productsContainer = document.querySelector('.products');
    productsContainer.innerHTML = ''; // Очистить контейнер перед добавлением новых товаров

    products.forEach(product => {
        const productElement = document.createElement('div');
        productElement.classList.add('product');
        productElement.innerHTML = `
            <a href="/products/${product.id_}">
                <img src="/static/img/products/${product.img_path}" alt="${product.name}" class="product-img">
                <h3>${product.name}</h3>
                <p>Цена: ${product.price} баллов</p>
            </a>
        `;
        productsContainer.appendChild(productElement);
    });
}


// Вызов функции для получения и отображения товаров при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    fetchProducts()
        .then(products => displayProducts(products))
        .catch(error => console.error('Ошибка получения товаров:', error));
});
