document.addEventListener("DOMContentLoaded", () => {
    const productsContainer = document.querySelector(".row.products");

    async function fetchProducts() {
        try {
            const response = await fetch("/products");
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const products = await response.json();
            displayProducts(products);
        } catch (error) {
            console.error("Ошибка загрузки товаров:", error);
            productsContainer.innerHTML = `<p>Не удалось загрузить товары. Попробуйте позже.</p>`;
        }
    }

    function displayProducts(products) {
        productsContainer.innerHTML = "";

        products.forEach(product => {
            const productBlock = document.createElement("div");
            productBlock.classList.add("block");

            productBlock.innerHTML = `
                <img src="${product.img_url}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p>Цена: ${product.price} ₽</p>
                <button class="button" data-id="${product.id}">Купить</button>
            `;

            productsContainer.appendChild(productBlock);
        });
    }

    fetchProducts();
});
