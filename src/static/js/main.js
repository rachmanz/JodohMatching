document.addEventListener("DOMContentLoaded", function () {
  // === 1. LOGIC LIVE PREVIEW (Halaman Utama) ===
  const setupPreview = (inputId, imgId, textId) => {
    const input = document.getElementById(inputId);
    const img = document.getElementById(imgId);
    const text = document.getElementById(textId);

    if (input) {
      input.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function (e) {
            img.src = e.target.result;
            img.classList.remove("d-none");
            text.classList.add("d-none");
          };
          reader.readAsDataURL(file);
        }
      });
    }
  };

  setupPreview("inputUser", "previewUser", "textUser");
  setupPreview("inputTarget", "previewTarget", "textTarget");

  // === 2. ANIMASI LOADING SAAT SUBMIT FORM ===
  const form = document.getElementById("matchForm");
  if (form) {
    form.addEventListener("submit", function () {
      document.getElementById("btnSubmit").disabled = true;
      document.getElementById("loadingState").classList.remove("d-none");
    });
  }

  // === 3. ANIMASI COUNTER SKOR & PROGRESS BAR (Halaman Hasil) ===
  const scoreTextEl = document.querySelector(".score-text");
  if (scoreTextEl) {
    const targetScore = parseInt(scoreTextEl.getAttribute("data-target")) || 0;
    const liveScoreEl = document.getElementById("liveScore");
    const progressBar = document.getElementById("progressBar");

    let currentScore = 0;
    // Kecepatan hitung naik, makin kecil makin cepat durasinya
    const duration = 1500;
    const increment = targetScore / (duration / 16);

    const updateScore = () => {
      currentScore += increment;
      if (currentScore >= targetScore) {
        liveScoreEl.innerText = targetScore;
        progressBar.style.width = targetScore + "%";
      } else {
        liveScoreEl.innerText = Math.floor(currentScore);
        progressBar.style.width = Math.floor(currentScore) + "%";
        requestAnimationFrame(updateScore);
      }
    };

    // Mulai animasi
    setTimeout(() => {
      requestAnimationFrame(updateScore);
    }, 200);
  }
});
