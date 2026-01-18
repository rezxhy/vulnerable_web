document.getElementById('loginForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const messageEl = document.getElementById('message');

  messageEl.textContent = 'Connexion en cours...';
  messageEl.style.color = '#666';

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok && data.success) {
      messageEl.style.color = 'green';
      messageEl.textContent = '✅ ' + data.message + ' Redirection...';
      
      // Sauvegarder le nom d'utilisateur
      localStorage.setItem('username', username);
      
      // Rediriger vers le dashboard après 1 seconde
      setTimeout(() => {
        window.location.href = '/dashboard.html';
      }, 1000);
      
    } else {
      messageEl.style.color = 'red';
      messageEl.textContent = '❌ ' + data.message;
    }
  } catch (err) {
    messageEl.style.color = 'red';
    messageEl.textContent = '❌ Erreur réseau : ' + err.message;
  }
});