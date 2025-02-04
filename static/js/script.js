// Add event listener to form submit
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/patient', true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log('Patient data submitted successfully!');
            } else {
                console.log('Error submitting patient data!');
            }
        };
        xhr.send(formData);
    });
});
