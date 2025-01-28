


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