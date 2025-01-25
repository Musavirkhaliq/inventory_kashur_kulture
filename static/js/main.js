/* static/js/main.js */
async function addProduct() {
    const form = document.getElementById('addProductForm');
    const formData = new FormData(form);
    
    const product = {
        sku: formData.get('sku'),
        name: formData.get('name'),
        quantity: parseInt(formData.get('quantity')),
        price: parseFloat(formData.get('price'))
    };

    try {
        const response = await fetch('/api/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(product)
        });

        if (response.ok) {
            window.location.reload();
        } else {
            alert('Error adding product');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding product');
    }
}


// static/js/main.js
async function addProduct() {
    const form = document.getElementById('addProductForm');
    const formData = new FormData(form);

    const product = {
        sku: formData.get('sku'),
        name: formData.get('name'),
        quantity: parseInt(formData.get('quantity')),
        price: parseFloat(formData.get('price'))
    };

    try {
        const response = await fetch('/api/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(product)
        });

        if (response.ok) {
            window.location.reload();
        } else {
            alert('Error adding product');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding product');
    }
}

async function addSale() {
    const form = document.getElementById('addSaleForm');
    const formData = new FormData(form);

    const sale = {
        product_id: parseInt(formData.get('product_id')),
        quantity: parseInt(formData.get('quantity')),
        customer_name: formData.get('customer_name')
    };

    try {
        const response = await fetch('/api/sales', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sale)
        });

        if (response.ok) {
            window.location.reload();
        } else {
            alert('Error adding sale');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding sale');
    }
}