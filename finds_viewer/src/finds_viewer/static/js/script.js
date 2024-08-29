document.addEventListener("DOMContentLoaded", () => {
    const imageGrid = document.getElementById('imageGrid');
    const modal = document.getElementById("imageModal");
    const zoomedImage = document.getElementById("zoomedImage");
    const closeModal = document.getElementsByClassName("close")[0];

    // Create 30x30 grid of images
    for (let i = 0; i < 400; i++) {
        const imgElement = document.createElement('div');
        imgElement.className = 'grid-item';
        imgElement.style.backgroundImage = `url('https://hips.hearstapps.com/hmg-prod/images/cute-cat-photos-1593441022.jpg?crop=0.670xw:1.00xh;0.167xw,0&resize=640:*')`; // Placeholder image
        //imgElement.style.backgroundImage = `url('https://placekitten.com/50/50?image=${i % 16}')`; // Placeholder image
        imgElement.style.backgroundSize = 'cover';

        // Click to zoom
        imgElement.addEventListener('click', function() {
            zoomedImage.src = `https://hips.hearstapps.com/hmg-prod/images/cute-cat-photos-1593441022.jpg?crop=0.670xw:1.00xh;0.167xw,0&resize=640:*`; // Placeholder for zoomed image
            modal.style.display = "block";
        });

        imageGrid.appendChild(imgElement);
    }

    // Close modal
    closeModal.onclick = function() {
        modal.style.display = "none";
    };

    // Close modal when clicking outside the image
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});
