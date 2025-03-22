(function(){
  const testDuration = 300; 
  let submitted = false;
  let timerInterval;

  const timerDisplay = document.getElementById("timerDisplay");
  const quizForm = document.getElementById("quizForm");
  // Get the hidden input field for remaining time
  const remainingTimeInput = document.getElementById("remaining_time");

  // Update quiz state on the server as the user selects an answer
  function updateQuizStateOnServer() {
    const qId = this.name.split("_")[1];
    const answer = this.value;
    const formData = new FormData();
    formData.append('question_id', qId);
    formData.append('answer', answer);
    fetch('/update_quiz_state', {
      method: 'POST',
      body: formData
    });
  }

  document.querySelectorAll('input[type="radio"]').forEach(radio => {
    radio.addEventListener("change", updateQuizStateOnServer);
  });

  if (timerDisplay && quizForm) {
    let timeLeft = (typeof remainingTime !== 'undefined') ? parseInt(remainingTime) : testDuration;
    
    function submitQuiz() {
      if (submitted) return;
      submitted = true;
      
      const submitButton = quizForm.querySelector("button[type='submit']");
      if (submitButton) submitButton.disabled = true;
      
      if (timerInterval) clearInterval(timerInterval);
      
      // Update the hidden field with the current timeLeft
      if(remainingTimeInput) {
        remainingTimeInput.value = timeLeft;
      }
      
      const formData = new FormData(quizForm);
      fetch(quizForm.action, {
        method: 'POST',
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        }
      })
      .then(response => response.json())
      .then(data => {
        window.location.href = "/view_results";
      });
    }
    
    function startTimer() {
      console.log("Starting timer with remaining time:", timeLeft);
      timerInterval = setInterval(() => {
        timeLeft--;
        // Update the hidden field continuously
        if(remainingTimeInput) {
          remainingTimeInput.value = timeLeft;
        }
        if (timeLeft <= 0) {
          clearInterval(timerInterval);
          timerDisplay.textContent = "0:00";
          submitQuiz();
        } else {
          let minutes = Math.floor(timeLeft / 60);
          let seconds = timeLeft % 60;
          if (seconds < 10) seconds = "0" + seconds;
          timerDisplay.textContent = minutes + ":" + seconds;
        }
      }, 1000);
    }
    
    window.addEventListener("load", startTimer);
    
    // You may keep the beforeunload handler if needed
    window.addEventListener("beforeunload", function(event) {
      const data = new URLSearchParams();
      data.append('remaining_time', timeLeft);
      navigator.sendBeacon('/update_quiz_timer', data);
    });
    
    quizForm.addEventListener("submit", function(event) {
      event.preventDefault();
      submitQuiz();
    });
  }
})();
  
// The code for rendering the combined histogram and normal curve remains unchanged...
if (typeof graphData !== "undefined" && graphData.length > 0) {
    const scores = graphData.map(item => parseInt(item.score)).filter(s => !isNaN(s));
    
    const maxScore = 20;   
    const bins = new Array(maxScore + 1).fill(0);
    scores.forEach(s => {
      if (s >= 0 && s <= maxScore) {
        bins[s]++;
      }
    });
  
    const n = scores.length;
    const mean = scores.reduce((acc, val) => acc + val, 0) / n;
    const variance = scores.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / n;
    const stdDev = Math.sqrt(variance);
  
    function normalDensity(x, mu, sigma) {
      return (1 / (sigma * Math.sqrt(2 * Math.PI))) *
             Math.exp(-0.5 * Math.pow((x - mu) / sigma, 2));
    }
  
    const normalData = [];
    for (let i = 0; i <= maxScore; i++) {
      const freq = normalDensity(i, mean, stdDev) * n;
      normalData.push(freq);
    }
  
    const ctx = document.getElementById('combinedChart').getContext('2d');
    const combinedChart = new Chart(ctx, {
      data: {
        labels: Array.from({ length: maxScore + 1 }, (_, i) => i.toString()),
        datasets: [
          {
            type: 'bar',
            label: 'Frequency',
            data: bins,
            backgroundColor: 'rgba(52, 152, 219, 0.5)',
            borderColor: 'rgba(41, 128, 185, 1)',
            borderWidth: 1,
            yAxisID: 'y'
          },
          {
            type: 'line',
            label: 'Normal Approx.',
            data: normalData,
            borderColor: 'rgba(231, 76, 60, 1)',
            fill: false,
            tension: 0.2,
            yAxisID: 'y'
          }
        ]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Count'
            }
          }
        }
      }
    });
}
