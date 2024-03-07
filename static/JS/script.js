
document.getElementById('username').addEventListener('click', function() {
   const logoutDropdown = document.getElementById('logoutDropdown');
     if (logoutDropdown.style.display === 'block') {
          logoutDropdown.style.display = 'none';
     } else {
          logoutDropdown.style.display = 'block';
     }
});

window.addEventListener('click', function(event) {
    const logoutDropdown = document.getElementById('logoutDropdown');
      const usernameItem = document.getElementById('usernameItem');
      if (event.target !== logoutDropdown && event.target !== usernameItem && !usernameItem.contains(event.target)) {
        logoutDropdown.style.display = 'none';
      }
});

setTimeout(function() {
    var flashMessage = document.querySelector('.flash-message');
    flashMessage.remove();
}, 3000);



// Function to update the progress bar
function updateProgressBar(progress) {
  const progressBar = document.getElementById('progressBar');
  progressBar.style.width = progress + '%';
  progressBar.setAttribute('aria-valuenow', progress);
}

// Function to check progress via AJAX
function checkProgress() {
  fetch('/progress')
    .then(response => response.json())
    .then(data => {
      updateProgressBar(data.progress);
      // Update status message
      document.getElementById('statusMessage').innerText = data.message;
      // Check progress again after 1 second
      if (data.progress < 100) {
        setTimeout(checkProgress, 1000);
      }
    })
    .catch(error => console.error('Error:', error));
}

// Call checkProgress function when the page loads
window.onload = function() {
  checkProgress();
};

