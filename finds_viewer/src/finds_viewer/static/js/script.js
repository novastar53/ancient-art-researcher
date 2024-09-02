document.addEventListener("DOMContentLoaded", () => {
    const imageGrid = document.getElementById('imageGrid');
    const modal = document.getElementById("imageModal");
    const zoomedImage = document.getElementById("zoomedImage");
    const closeModal = document.getElementsByClassName("close")[0];

    // loop over the images and add them to the grid
    imageArray.forEach((image, i) => {
        const imgElement = document.createElement('div');
        imgElement.className = 'grid-item';
        imgElement.style.backgroundImage = `url(${image.url})`; // Placeholder image
        //imgElement.style.backgroundImage = `url('https://placekitten.com/50/50?image=${i % 16}')`; // Placeholder image
        imgElement.style.backgroundSize = 'cover';

        // Click to zoom
        imgElement.addEventListener('click', function() {
            zoomedImage.src = image.url; // Placeholder for zoomed image
            imageTitleLink.href = image.source_url;
            imageTitleLink.textContent = image.title;
            imageDescription.textContent = image.description;
            modal.style.display = 'block';
        });

        imageGrid.appendChild(imgElement);
    });

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
