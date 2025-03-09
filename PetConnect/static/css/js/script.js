document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            const petId = this.getAttribute('data-pet-id');
            fetch(`/pets/${petId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`like-count-${petId}`).textContent = data.likes;
            });
        });
    });
});