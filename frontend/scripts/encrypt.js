function previewImage() {
    const fileInput = document.getElementById("dropzone-file");
    const fileSelector = document.getElementById("fileSelector");
    const imageGrid = document.getElementById("imageGrid");
    const originalImage = document.getElementById("originalImage");

    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            originalImage.src = e.target.result;
            imageGrid.style.display = "grid";
            fileSelector.style.display = "none";
        };

        reader.readAsDataURL(file);
    }
}

function uploadImage() {
    const fileInput = document.getElementById("dropzone-file");
    const alertBox = document.getElementById("alert-box");
    const encryptedImage = document.getElementById("encryptedImage");

    alertBox.style.display = "none";

    if (fileInput.files.length === 0) {
        showAlert("Please select an image to upload.", "blue");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    fetch("/encrypt/", {
        method: "POST",
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        encryptedImage.src = imageUrl;
        encryptedImage.style.display = "block";
    })
    .catch(error => showAlert("Error encrypting image. Please try again.", "red"));
}

function showAlert(message, color) {
    const alertBox = document.getElementById("alert-box");
    const alertMessage = document.getElementById("alert-message");

    alertMessage.innerText = message;

    if (color === "blue") {
        alertBox.className = "flex items-center p-4 mb-4 text-sm text-blue-800 rounded-lg bg-blue-50 dark:bg-gray-800 dark:text-blue-400";
    } else if (color === "red") {
        alertBox.className = "flex items-center p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400";
    }

    alertBox.style.display = "flex"; 
}



