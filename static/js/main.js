// Function to handle form submissions
async function submitForm(formId, endpoint, method = "POST") {
    const form = document.getElementById(formId);
    if (!form) return;

    form.removeEventListener("submit", handleSubmit);

    async function handleSubmit(e) {
        e.preventDefault();

        const submitButton = form.querySelector("button[type='submit']");
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Submitting...";
        }

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(endpoint, {
                method: method,
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert("Operation successful!");
                window.location.reload();
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail || "Something went wrong!"}`);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = "Submit";
            }
        }
    }

    form.addEventListener("submit", handleSubmit);
}

// Initialize form submissions when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    submitForm("productForm", "/products/");
    submitForm("customerForm", "/customers/");
    submitForm("saleForm", "/sales/");
    submitForm("restockForm", "/restocks/");
    submitForm("invoiceForm", "/invoices/");

    const editProductForm = document.getElementById("editProductForm");
    if (editProductForm) {
        const productId = document.getElementById("id").value;
        submitForm("editProductForm", `/products/${productId}`, "PUT");
    }
});

// document.addEventListener("DOMContentLoaded", () => {
//     submitForm("restockForm", "/restocks/");
// });



// Add this to your main.js file or create a new sales.js file

let saleItems = [];

function updateTotalAmount() {
    const total = saleItems.reduce((sum, item) => sum + (item.quantity * item.price), 0);
    document.getElementById('total-amount').textContent = total.toFixed(2);
    
    // Update balance
    const amountReceived = parseFloat(document.getElementById('amount_received').value) || 0;
    const balance = total - amountReceived;
    document.getElementById('balance-amount').textContent = balance.toFixed(2);
}

function validateStock(productId, quantity) {
    const option = document.querySelector(`#product_id option[value="${productId}"]`);
    const availableStock = parseInt(option.dataset.stock);
    return quantity <= availableStock;
}

document.getElementById('add-item').addEventListener('click', function() {
    const productSelect = document.getElementById('product_id');
    const quantity = parseInt(document.getElementById('quantity').value);
    const price = parseFloat(document.getElementById('selling_price').value);
    
    const productId = parseInt(productSelect.value);
    const productName = productSelect.options[productSelect.selectedIndex].text;
    
    if (!productId || !quantity || !price) {
        alert('Please fill in all fields');
        return;
    }

    if (!validateStock(productId, quantity)) {
        alert('Insufficient stock available');
        return;
    }
    
    saleItems.push({
        product_id: productId,
        quantity: quantity,
        price: price,
        product_name: productName
    });
    
    updateSaleItemsTable();
    updateTotalAmount();
    
    // Reset input fields
    document.getElementById('quantity').value = '1';
    document.getElementById('product_id').dispatchEvent(new Event('change'));
});

function updateSaleItemsTable() {
    const tbody = document.getElementById('sale-items-tbody');
    tbody.innerHTML = '';
    
    saleItems.forEach((item, index) => {
        const tr = document.createElement('tr');
        const subtotal = item.quantity * item.price;
        
        tr.innerHTML = `
            <td>${item.product_name}</td>
            <td>${item.quantity}</td>
            <td>${item.price.toFixed(2)}</td>
            <td>${subtotal.toFixed(2)}</td>
            <td>
                <button type="button" onclick="removeSaleItem(${index})" class="btn btn-danger btn-sm">Remove</button>
                <button type="button" onclick="editSaleItem(${index})" class="btn btn-primary btn-sm">Edit</button>
            </td>
        `;
        
        tbody.appendChild(tr);
    });
}

function removeSaleItem(index) {
    saleItems.splice(index, 1);
    updateSaleItemsTable();
    updateTotalAmount();
}

function editSaleItem(index) {
    const item = saleItems[index];
    document.getElementById('product_id').value = item.product_id;
    document.getElementById('quantity').value = item.quantity;
    document.getElementById('selling_price').value = item.price;
    
    removeSaleItem(index);
}

document.getElementById('amount_received').addEventListener('input', updateTotalAmount);

document.getElementById('saleForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (saleItems.length === 0) {
        alert('Please add at least one item to the sale');
        return;
    }
    
    const formData = {
        customer_id: parseInt(document.getElementById('customer_id').value),
        items: saleItems,
        amount_received: parseFloat(document.getElementById('amount_received').value) || 0
    };
    
    try {
        const response = await fetch('/sales/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            alert('Sale recorded successfully!');
            window.location.reload();
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while recording the sale');
    }
});

// View sale details
document.querySelectorAll('.view-details').forEach(button => {
    button.addEventListener('click', async function() {
        const saleId = this.dataset.saleId;
        try {
            const response = await fetch(`/sales/${saleId}/details`);
            if (response.ok) {
                const details = await response.json();
                showSaleDetails(details);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

function showSaleDetails(details) {
    const modal = new bootstrap.Modal(document.getElementById('saleDetailsModal'));
    const content = document.getElementById('saleDetailsContent');
    
    let itemsHtml = details.items.map(item => `
        <tr>
            <td>${item.product_name}</td>
            <td>${item.quantity}</td>
            <td>${item.price.toFixed(2)}</td>
            <td>${(item.quantity * item.price).toFixed(2)}</td>
        </tr>
    `).join('');
    
    content.innerHTML = `
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    ${itemsHtml}
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="3" class="text-end"><strong>Total:</strong></td>
                        <td>${details.total_amount.toFixed(2)}</td>
                    </tr>
                </tfoot>
            </table>
        </div>
    `;
    
    modal.show();
}



// Store JWT token in localStorage
function storeToken(token) {
    localStorage.setItem('token', token);
}

// Get JWT token from localStorage
function getToken() {
    return localStorage.getItem('token');
}

// Remove JWT token from localStorage
function removeToken() {
    localStorage.removeItem('token');
}

// Check if user is logged in
function isLoggedIn() {
    return getToken() !== null;
}

// Update navigation bar based on login status
function updateNavbar() {
    const loginLink = document.getElementById('login-link');
    const registerLink = document.getElementById('register-link');
    const logoutLink = document.getElementById('logout-link');

    if (isLoggedIn()) {
        loginLink.style.display = 'none';
        registerLink.style.display = 'none';
        logoutLink.style.display = 'inline';
    } else {
        loginLink.style.display = 'inline';
        registerLink.style.display = 'inline';
        logoutLink.style.display = 'none';
    }
}

// Handle login form submission
document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    });

    if (response.ok) {
        const data = await response.json();
        storeToken(data.access_token);
        updateNavbar();
        window.location.href = '/';
    } else {
        document.getElementById('login-message').textContent = 'Login failed. Please check your credentials.';
    }
});

// Handle registration form submission
document.getElementById('register-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
    });

    if (response.ok) {
        document.getElementById('register-message').textContent = 'Registration successful. Please login.';
    } else {
        document.getElementById('register-message').textContent = 'Registration failed. Please try again.';
    }
});

// Handle logout
document.getElementById('logout-link')?.addEventListener('click', (e) => {
    e.preventDefault();
    removeToken();
    updateNavbar();
    window.location.href = '/';
});

// Update navbar on page load
updateNavbar();