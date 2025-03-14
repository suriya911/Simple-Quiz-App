// Set test duration to 5 minutes (300 seconds)
const testDuration = 5 * 60; 

// Get DOM elements
const timerDisplay = document.getElementById("timerDisplay");
const quizForm = document.getElementById("quizForm");

// Function to start/resume the timer
function startTimer() {
    // If no test start time is stored, set it now
    if (!localStorage.getItem("testStartTime")) {
        localStorage.setItem("testStartTime", Date.now());
    }
    const testStartTime = parseInt(localStorage.getItem("testStartTime"), 10);
    const timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - testStartTime) / 1000);
        let timeLeft = testDuration - elapsed;
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            timerDisplay.textContent = "0:00";
            // Auto-submit the form when time runs out
            quizForm.submit();
        } else {
            let minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;
            if (seconds < 10) {
                seconds = "0" + seconds;
            }
            timerDisplay.textContent = minutes + ":" + seconds;
        }
    }, 1000);
}

// On page load, start or resume the timer
window.addEventListener("load", () => {
    // Check if there's a stored start time and that it's within test duration
    const stored = localStorage.getItem("testStartTime");
    if (stored) {
        const elapsed = Math.floor((Date.now() - parseInt(stored, 10)) / 1000);
        if (elapsed < testDuration) {
            startTimer();
        } else {
            // If expired, remove the stored time and start fresh
            localStorage.removeItem("testStartTime");
            startTimer();
        }
    } else {
        startTimer();
    }
});

// Clear stored test start time on form submission
if (quizForm) {
    quizForm.addEventListener("submit", () => {
        localStorage.removeItem("testStartTime");
    });
}


// static/js/script.js

// Check if graphData is defined and not empty
if (typeof graphData !== "undefined" && graphData.length > 0) {
    // 1. Extract numeric scores
    const scores = graphData.map(item => parseInt(item.score)).filter(s => !isNaN(s));
    
    // 2. Build histogram data (0–20)
    const maxScore = 20;   // Adjust if your quiz allows different max
    const bins = new Array(maxScore + 1).fill(0);
    scores.forEach(s => {
      if (s >= 0 && s <= maxScore) {
        bins[s]++;
      }
    });
  
    // 3. Compute mean and standard deviation for normal approximation
    const n = scores.length;
    const mean = scores.reduce((acc, val) => acc + val, 0) / n;
    const variance = scores.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / n;
    const stdDev = Math.sqrt(variance);
  
    // 4. Normal distribution for each bin center (assuming bin width = 1)
    function normalDensity(x, mu, sigma) {
      return (1 / (sigma * Math.sqrt(2 * Math.PI))) *
             Math.exp(-0.5 * Math.pow((x - mu) / sigma, 2));
    }
  
    const normalData = [];
    for (let i = 0; i <= maxScore; i++) {
      // frequency = density * total count * binWidth (binWidth=1)
      const freq = normalDensity(i, mean, stdDev) * n;
      normalData.push(freq);
    }
  
    // 5. Create the combined chart
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
  