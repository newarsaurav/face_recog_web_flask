document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("video");
    const captureBtn = document.getElementById("capture");
    const canvas = document.getElementById("canvas");
    const faceDataInput = document.getElementById("face_data");

    // If there is no video element, exit script to prevent errors
    if (!video) {
        console.warn("Webcam elements not found on this page. Skipping script execution.");
        return;
    }

    // Ensure browser supports webcam access
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Webcam not supported in this browser.");
        return;
    }

    // Start the webcam stream
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((err) => {
            console.error("Error accessing webcam: ", err);
            alert("Camera access denied or unavailable.");
        });

    // Capture the face image when button is clicked
    if (captureBtn && canvas && faceDataInput) {
        captureBtn.addEventListener("click", function () {
            const context = canvas.getContext("2d");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Convert image to Base64 and store in hidden input
            faceDataInput.value = canvas.toDataURL("image/jpeg");
            alert("Face captured! Click Register to proceed.");
        });
    }
});
