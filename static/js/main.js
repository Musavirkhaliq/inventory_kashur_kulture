// Function to handle form submissions
async function submitForm(formId, endpoint, method = "POST") {
    const form = document.getElementById(formId);
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
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
                window.location.reload(); // Reload the page to reflect changes
            } else {
                alert("Something went wrong!");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
}

// Example: Handle product form submission
document.addEventListener("DOMContentLoaded", () => {
    submitForm("productForm", "/products/");
    submitForm("saleForm", "/sales/");
    submitForm("restockForm", "/restocks/");
    submitForm("invoiceForm", "/invoices/");
});


// Function to handle edit form submission
async function submitEditForm(formId, endpoint, method = "PUT") {
    const form = document.getElementById(formId);
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
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
                alert("Product updated successfully!");
                window.location.href = "/products"; // Redirect to products page
            } else {
                alert("Something went wrong!");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
}

// Handle edit product form submission
document.addEventListener("DOMContentLoaded", () => {
    submitEditForm("editProductForm", `/products/${document.getElementById("id").value}`);
});