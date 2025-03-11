document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id'); 
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; 

            fetch(`/like-post/${postId}/`, {  
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, 
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                document.getElementById(`like-count-${postId}`).textContent = data.likes;  
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});