document.getElementById('loginForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  const messageEl = document.getElementById('message');
  const submitBtn = document.querySelector('button[type="submit"]');
  const originalBtnText = submitBtn.innerHTML;

  // Validation basique côté client
  if (!username || !password) {
    showMessage('error', 'Veuillez remplir tous les champs');
    return;
  }

  // Réinitialiser le message
  messageEl.classList.add('hidden');
  
  // État de chargement
  submitBtn.disabled = true;
  submitBtn.innerHTML = `
    <span class="flex items-center justify-center gap-2">
      <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span>Connexion en cours...</span>
    </span>
  `;
  submitBtn.style.opacity = '0.7';
  submitBtn.style.cursor = 'not-allowed';

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    // Gérer les réponses non-JSON
    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error('Réponse invalide du serveur');
    }

    if (response.ok && data.success) {
      // ✅ SUCCÈS
      showMessage('success', 'Connexion réussie ! Redirection...');
      
      // Animation de succès sur le bouton
      submitBtn.style.background = '#10B981';
      submitBtn.innerHTML = `
        <span class="flex items-center justify-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <span>Connexion réussie !</span>
        </span>
      `;
      
      // Sauvegarder le nom d'utilisateur ET le rôle
      localStorage.setItem('username', username);
      localStorage.setItem('userRole', data.role || 'user');
      
      // Rediriger vers le dashboard après 1.5 secondes
      setTimeout(() => {
        window.location.href = '/dashboard.html';
      }, 1500);
      
    } else {
      // ❌ ERREUR
      let errorMessage = 'Erreur de connexion';
      
      // Personnaliser le message selon le code d'erreur
      if (response.status === 401) {
        errorMessage = 'Identifiants incorrects. Vérifiez votre nom d\'utilisateur et mot de passe.';
      } else if (response.status === 400) {
        errorMessage = 'Données invalides. Veuillez réessayer.';
      } else if (response.status === 503) {
        errorMessage = 'Service temporairement indisponible. Réessayez dans quelques instants.';
      } else if (data.message) {
        errorMessage = data.message;
      }
      
      showMessage('error', errorMessage);
      
      // Réinitialiser le bouton
      resetButton(submitBtn, originalBtnText);
    }
  } catch (err) {
    // ⚠️ ERREUR RÉSEAU
    let errorMsg = 'Impossible de contacter le serveur. Vérifiez votre connexion.';
    
    if (err.message.includes('JSON')) {
      errorMsg = 'Erreur de communication avec le serveur.';
    } else if (err.message) {
      errorMsg = err.message;
    }
    
    showMessage('error', errorMsg);
    
    // Réinitialiser le bouton
    resetButton(submitBtn, originalBtnText);
  }
});

// Fonction pour afficher les messages
function showMessage(type, text) {
  const messageEl = document.getElementById('message');
  messageEl.classList.remove('hidden');
  
  // Retirer toutes les classes de couleur
  messageEl.classList.remove('text-green-600', 'text-red-600', 'text-yellow-600');
  
  let icon = '';
  let colorClass = '';
  
  if (type === 'success') {
    icon = `
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
    `;
    colorClass = 'text-green-600';
  } else if (type === 'error') {
    icon = `
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
    `;
    colorClass = 'text-red-600';
  } else if (type === 'warning') {
    icon = `
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
      </svg>
    `;
    colorClass = 'text-yellow-600';
  }
  
  messageEl.classList.add(colorClass);
  messageEl.innerHTML = `
    <div class="flex items-center justify-center gap-2">
      ${icon}
      <span>${text}</span>
    </div>
  `;
  
  // Animation shake pour les erreurs
  if (type === 'error') {
    messageEl.style.animation = 'shake 0.5s ease-in-out';
    setTimeout(() => {
      messageEl.style.animation = '';
    }, 500);
  }
}

// Fonction pour réinitialiser le bouton
function resetButton(submitBtn, originalText) {
  submitBtn.disabled = false;
  submitBtn.innerHTML = originalText;
  submitBtn.style.background = '#0066CC';
  submitBtn.style.opacity = '1';
  submitBtn.style.cursor = 'pointer';
}

// Ajouter l'animation shake au CSS
if (!document.getElementById('shake-animation')) {
  const style = document.createElement('style');
  style.id = 'shake-animation';
  style.textContent = `
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
      20%, 40%, 60%, 80% { transform: translateX(8px); }
    }
  `;
  document.head.appendChild(style);
}