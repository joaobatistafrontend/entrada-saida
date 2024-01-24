const video = document.getElementById('video');

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('../models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('../models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('../models'),
  faceapi.nets.faceExpressionNet.loadFromUri('../models')
]).then(startVideo);

function startVideo() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error(err));
}

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.body.append(canvas);
  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);

  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedDetections);
    //faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
    //faceapi.draw.drawFaceExpressions(canvas, resizedDetections);

    if (detections[0] && detections[0].expressions) {
      const myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      const raw = JSON.stringify({
        "local_name": "test",
        "created_at": "2021-07-09T20:48:09.859650Z",
        "angry": detections[0].expressions.angry,
        "disgusted": detections[0].expressions.disgusted,
        "fearful": detections[0].expressions.fearful,
        "happy": detections[0].expressions.happy,
        "neutral": detections[0].expressions.neutral,
        "sad": detections[0].expressions.sad,
        "surprised": detections[0].expressions.surprised
      });

      const requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
      };

      fetch("http://127.0.0.1:8000/facial/", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
    }

  }, 100);
});







document.addEventListener("DOMContentLoaded", function () {
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const captureBtn = document.getElementById("capture-btn");
  const imageInput = document.getElementById("image-input");

  // Função para inicializar a câmera
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

  // Inicializar a câmera ao carregar a página
  initializeCamera();

      captureBtn.addEventListener("click", function () {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);

          canvas.toBlob(function (blob) {
              const formData = new FormData();

              if (blob) {
                  const file = new File([blob], "snapshot.png", { type: "image/png" });
                  formData.append("image", file);

                  // Submeta o formulário
                  submitForm(formData);
              } else {
                  console.log("Erro ao capturar a foto. Nenhum blob disponível.");
              }
          }, "image/png");
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
          return response.text(); // Alterado para response.text() para lidar com a resposta HTML
      })
      .then((html) => {
          document.body.innerHTML = html; // Atualiza o conteúdo do corpo da página com a resposta HTML

          // Reinicialize a câmera após a verificação
          initializeCamera();

          // Agende um redirecionamento/recarregamento após 5 segundos
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


  
  Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('../models'),
    faceapi.nets.faceLandmark68Net.loadFromUri('../models'),
    faceapi.nets.faceRecognitionNet.loadFromUri('../models'),
    faceapi.nets.faceExpressionNet.loadFromUri('../models')
  ]).then(startVideo);

  
  video.addEventListener('play', () => {
    const canvas = faceapi.createCanvasFromMedia(video);
    document.body.append(canvas);
    const displaySize = { width: video.width, height: video.height };
    faceapi.matchDimensions(canvas, displaySize);
  
    setInterval(async () => {
      const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
      const resizedDetections = faceapi.resizeResults(detections, displaySize);
      canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
      faceapi.draw.drawDetections(canvas, resizedDetections);
      //faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
      //faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
  
      if (detections[0] && detections[0].expressions) {
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
  
        const raw = JSON.stringify({
          "local_name": "test",
          "created_at": "2021-07-09T20:48:09.859650Z",
          "angry": detections[0].expressions.angry,
          "disgusted": detections[0].expressions.disgusted,
          "fearful": detections[0].expressions.fearful,
          "happy": detections[0].expressions.happy,
          "neutral": detections[0].expressions.neutral,
          "sad": detections[0].expressions.sad,
          "surprised": detections[0].expressions.surprised
        });
  
        const requestOptions = {
          method: 'POST',
          headers: myHeaders,
          body: raw,
          redirect: 'follow'
        };
  
        fetch("http://127.0.0.1:8000/facial/", requestOptions)
          .then(response => response.text())
          .then(result => console.log(result))
          .catch(error => console.log('error', error));
      }
  
    }, 100);
  });
  
  
  

});

