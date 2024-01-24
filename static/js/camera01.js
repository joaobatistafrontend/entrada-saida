document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("video");
    const canvas = document.createElement("canvas");
    document.body.append(canvas);

    function initializeCamera() {
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
            })
            .catch(function (err) {
                console.log("Erro ao acessar a câmera: ", err);
            });
    }

    initializeCamera();

    video.addEventListener('play', () => {
        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(canvas, displaySize);

        setInterval(async () => {
            const detections = await faceapi.detectSingleFace(video).withFaceLandmarks().withFaceDescriptor();

            if (detections && detections.detection && detections.detection._score > 0.75) {
                console.log("Rosto detectado com confiança superior a 75%. Enviando para o servidor...");

                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

                canvas.toBlob(function (blob) {
                    const formData = new FormData();

                    if (blob) {
                        const file = new File([blob], "snapshot.png", { type: "image/png" });
                        formData.append("image", file);

                        // Adiciona a lógica de reconhecimento de rosto
                        submitForm(formData);
                    } else {
                        console.log("Erro ao capturar a foto. Nenhum blob disponível.");
                    }
                }, "image/png");
            }

        }, 100);
    });

    function submitForm(formData) {
        fetch("/upload/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.text();
            })
            .then((html) => {
                document.body.innerHTML = html;
                initializeCamera();

                setTimeout(function () {
                    location.reload();
                }, 5000);
            })
            .catch((error) => {
                console.error("Erro no envio da imagem: ", error);
            });
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        
        if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
    }

    // Carrega os modelos de reconhecimento facial
    Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri('../models'),
        faceapi.nets.faceLandmark68Net.loadFromUri('../models'),
        faceapi.nets.faceRecognitionNet.loadFromUri('../models'),
    ]).then(() => {
        console.log("Modelos carregados com sucesso.");
    });
});
