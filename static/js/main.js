document.addEventListener("DOMContentLoaded", () => {
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
                    <button type="button" data-index="${index}" class="btn btn-danger btn-sm remove-item-btn">Remove</button>
                    <button type="button" data-index="${index}" class="btn btn-primary btn-sm edit-item-btn">Edit</button>
                </td>
            `;
            
            tbody.appendChild(tr);
        });

        // Attach event listeners to dynamically generated buttons
        attachEventListeners();
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

    // Delegate event listeners for remove and edit buttons
    function attachEventListeners() {
        // Remove item
        const removeButtons = document.querySelectorAll('.remove-item-btn');
        removeButtons.forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                removeSaleItem(index);
            });
        });

        // Edit item
        const editButtons = document.querySelectorAll('.edit-item-btn');
        editButtons.forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                editSaleItem(index);
            });
        });
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
});
