$(document).ready(function() {

    // --- Client-side Form Validation for /register ---
    $("#registerForm").submit(function(e) {
        
        // Get trimmed values from the form fields
        let name = $("#name").val().trim();
        let email = $("#email").val().trim();
        let course = $("#course").val().trim();
        let year = $("#year").val().trim();
        let valid = true; // Assume valid initially

        // 1. Check for empty fields
        if (name === "" || email === "" || course === "" || year === "") {
            alert("Please fill in all fields before submitting!");
            valid = false;
        }

        // 2. Simple email format check (only if not already invalid)
        if (valid) {
            // Simple regex for basic email format
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(email)) {
                alert("Please enter a valid email address!");
                valid = false;
            }
        }
        
        // If validation fails, prevent the default form submission.
        if (!valid) {
            e.preventDefault(); 
        }

        // NOTE: If validation succeeds (valid is true), the form submission 
        // proceeds normally to the Flask route '/submit'. The backend handles 
        // saving the data and showing the success message (via flash messages).
    });


    // --- Delete Confirmation for /students ---
    $(".delete-btn").on("click", function(e) {
        if (!confirm("Are you sure you want to delete this record?")) {
            e.preventDefault(); // Block navigation if the user clicks 'Cancel'
        }
    });

});