// // Function to handle form submissions
// async function submitForm(formId, endpoint, method = "POST") {
//     const form = document.getElementById(formId);
//     if (!form) return; // Exit if form doesn't exist

//     // Remove any existing event listeners to prevent duplicates
//     form.removeEventListener("submit", handleSubmit);

//     // Define the submit handler
//     async function handleSubmit(e) {
//         e.preventDefault();

//         // Disable the submit button to prevent multiple submissions
//         const submitButton = form.querySelector("button[type='submit']");
//         if (submitButton) {
//             submitButton.disabled = true;
//             submitButton.textContent = "Submitting...";
//         }

//         const formData = new FormData(form);
//         const data = Object.fromEntries(formData.entries());

//         try {
//             const response = await fetch(endpoint, {
//                 method: method,
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body: JSON.stringify(data),
//             });

//             if (response.ok) {
//                 alert("Operation successful!");
//                 window.location.reload(); // Reload the page to reflect changes
//             } else {
//                 const errorData = await response.json();
//                 alert(`Error: ${errorData.detail || "Something went wrong!"}`);
//             }
//         } catch (error) {
//             console.error("Error:", error);
//             alert("An error occurred. Please try again.");
//         } finally {
//             // Re-enable the submit button
//             if (submitButton) {
//                 submitButton.disabled = false;
//                 submitButton.textContent = "Submit";
//             }
//         }
//     }

//     // Attach the event listener
//     form.addEventListener("submit", handleSubmit);
// }

// // Function to handle edit form submissions
// async function submitEditForm(formId, endpoint, method = "PUT") {
//     const form = document.getElementById(formId);
//     if (!form) return; // Exit if form doesn't exist

//     // Remove any existing event listeners to prevent duplicates
//     form.removeEventListener("submit", handleSubmit);

//     // Define the submit handler
//     async function handleSubmit(e) {
//         e.preventDefault();

//         // Disable the submit button to prevent multiple submissions
//         const submitButton = form.querySelector("button[type='submit']");
//         if (submitButton) {
//             submitButton.disabled = true;
//             submitButton.textContent = "Updating...";
//         }

//         const formData = new FormData(form);
//         const data = Object.fromEntries(formData.entries());

//         try {
//             const response = await fetch(endpoint, {
//                 method: method,
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body: JSON.stringify(data),
//             });

//             if (response.ok) {
//                 alert("Update successful!");
//                 window.location.href = "/products"; // Redirect to products page
//             } else {
//                 const errorData = await response.json();
//                 alert(`Error: ${errorData.detail || "Something went wrong!"}`);
//             }
//         } catch (error) {
//             console.error("Error:", error);
//             alert("An error occurred. Please try again.");
//         } finally {
//             // Re-enable the submit button
//             if (submitButton) {
//                 submitButton.disabled = false;
//                 submitButton.textContent = "Update";
//             }
//         }
//     }

//     // Attach the event listener
//     form.addEventListener("submit", handleSubmit);
// }

// // Initialize form submissions when the DOM is fully loaded
// document.addEventListener("DOMContentLoaded", () => {
//     // Product form
//     submitForm("productForm", "/products/");

//     // Customer form
//     submitForm("customerForm", "/customers/");

//     // Sale form
//     submitForm("saleForm", "/sales/");

//     // Restock form
//     submitForm("restockForm", "/restocks/");

//     // Invoice form
//     submitForm("invoiceForm", "/invoices/");

//     // Edit product form (if it exists on the page)
//     const editProductForm = document.getElementById("editProductForm");
//     if (editProductForm) {
//         const productId = document.getElementById("id").value;
//         submitEditForm("editProductForm", `/products/${productId}`, "PUT");
//     }
// });


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