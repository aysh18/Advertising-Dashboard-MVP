// General utility functions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize any tooltips or other UI elements
});

// Form validation example
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#e74c3c';
            isValid = false;
        } else {
            field.style.borderColor = '';
        }
    });
    
    return isValid;
}

// Image preview for file uploads
function setupImagePreview(input, previewElement) {
    if (input && previewElement) {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewElement.src = e.target.result;
                    previewElement.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        });
    }
}