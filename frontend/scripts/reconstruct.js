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

async function reconstructImage() {
    const fileInput = document.getElementById("dropzone-file");
    const reconstructedImage = document.getElementById("reconstructedImage");

    if (fileInput.files.length === 0) {
        alert("Please select an image first.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        // Request reconstructed image
        let imgResponse = await fetch("http://127.0.0.1:8000/reconstruct/", {
            method: "POST",
            body: formData
        });

        if (!imgResponse.ok) {
            throw new Error("Failed to reconstruct image.");
        }

        let imgBlob = await imgResponse.blob();
        let imgURL = URL.createObjectURL(imgBlob);
        reconstructedImage.src = imgURL;
        reconstructedImage.style.display = "block";

        // Request SSIM & PSNR
        let metricsResponse = await fetch("http://127.0.0.1:8000/metrics/", {
            method: "POST",
            body: formData
        });

        if (!metricsResponse.ok) {
            throw new Error("Failed to fetch image quality metrics.");
        }

        let metricsData = await metricsResponse.json();

        let ssimScore = Math.round(metricsData.ssim * 100);
        document.getElementById("ssimValue").innerText = (metricsData.ssim * 100).toFixed(2) + "%";
        document.getElementById("ssimBar").style.width = ssimScore + "%";

        let psnrScore = Math.min(Math.round(metricsData.psnr / 50 * 100), 100);
        document.getElementById("psnrBar").style.width = psnrScore + "%";
        document.getElementById("psnrValue").innerText = metricsData.psnr + " dB";
        
    } catch (error) {
        alert("Error: " + error.message);
    }
}
