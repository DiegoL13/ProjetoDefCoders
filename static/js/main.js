// Form validation functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateCPF(cpf) {
    // Remove non-numeric characters
    cpf = cpf.replace(/[^\d]/g, '');
    
    // Check if CPF has 11 digits
    if (cpf.length !== 11) return false;
    
    // Check for known invalid CPFs
    if (/^(\d)\1{10}$/.test(cpf)) return false;
    
    // Validate CPF digits
    let sum = 0;
    for (let i = 0; i < 9; i++) {
        sum += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let remainder = 11 - (sum % 11);
    let digit1 = remainder >= 10 ? 0 : remainder;
    
    sum = 0;
    for (let i = 0; i < 10; i++) {
        sum += parseInt(cpf.charAt(i)) * (11 - i);
    }
    remainder = 11 - (sum % 11);
    let digit2 = remainder >= 10 ? 0 : remainder;
    
    return parseInt(cpf.charAt(9)) === digit1 && parseInt(cpf.charAt(10)) === digit2;
}

// Login form validation
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form[action*="login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const emailInput = loginForm.querySelector('input[type="email"], input[name*="email"], input[name*="username"]');
            const passwordInput = loginForm.querySelector('input[type="password"]');
            
            // Remove previous error messages
            const existingError = loginForm.querySelector('.validation-error');
            if (existingError) {
                existingError.remove();
            }
            
            let isValid = true;
            
            if (emailInput && emailInput.value.trim() === '') {
                showError(emailInput, 'O campo e-mail é obrigatório');
                isValid = false;
            } else if (emailInput && !validateEmail(emailInput.value)) {
                showError(emailInput, 'Por favor, insira um e-mail válido');
                isValid = false;
            }
            
            if (passwordInput && passwordInput.value.trim() === '') {
                showError(passwordInput, 'O campo senha é obrigatório');
                isValid = false;
            } else if (passwordInput && passwordInput.value.length < 6) {
                showError(passwordInput, 'A senha deve ter pelo menos 6 caracteres');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
});

// Patient/Medico registration form validation
document.addEventListener('DOMContentLoaded', function() {
    const registrationForms = document.querySelectorAll('form[action*="cadastro"]');
    registrationForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Clear previous errors
            const existingErrors = form.querySelectorAll('.validation-error');
            existingErrors.forEach(error => error.remove());
            
            // Validate email
            const emailInput = form.querySelector('input[name*="email"]');
            if (emailInput && emailInput.value.trim() === '') {
                showError(emailInput, 'O campo e-mail é obrigatório');
                isValid = false;
            } else if (emailInput && !validateEmail(emailInput.value)) {
                showError(emailInput, 'Por favor, insira um e-mail válido');
                isValid = false;
            }
            
            // Validate CPF
            const cpfInput = form.querySelector('input[name*="cpf"]');
            if (cpfInput && !validateCPF(cpfInput.value)) {
                showError(cpfInput, 'Por favor, insira um CPF válido');
                isValid = false;
            }
            
            // Validate password
            const passwordInput = form.querySelector('input[name*="password"]');
            const confirmPasswordInput = form.querySelector('input[name*="confirm_password"]');
            
            if (passwordInput && passwordInput.value.length < 6) {
                showError(passwordInput, 'A senha deve ter pelo menos 6 caracteres');
                isValid = false;
            }
            
            if (confirmPasswordInput && passwordInput.value !== confirmPasswordInput.value) {
                showError(confirmPasswordInput, 'As senhas não conferem');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
});

// Helper function to show error messages
function showError(input, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'validation-error';
    errorDiv.style.color = '#e74c3c';
    errorDiv.style.fontSize = '0.9rem';
    errorDiv.style.marginTop = '5px';
    errorDiv.textContent = message;
    
    input.parentNode.appendChild(errorDiv);
    input.style.borderColor = '#e74c3c';
    
    // Remove error styling on input
    input.addEventListener('input', function() {
        input.style.borderColor = '';
        const error = input.parentNode.querySelector('.validation-error');
        if (error) {
            error.remove();
        }
    });
}

// Loading state for forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Processando...';
                
                // Re-enable after 5 seconds as a fallback
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.textContent = submitButton.getAttribute('data-original-text') || 'Enviar';
                }, 5000);
            }
        });
    });
});

// Smooth scroll for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// File upload preview (for exam images)
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const files = e.target.files;
            const previewContainer = document.getElementById('image-preview') || createImagePreviewContainer(input);
            
            // Clear previous previews
            previewContainer.innerHTML = '';
            
            Array.from(files).forEach(file => {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.style.maxWidth = '200px';
                        img.style.maxHeight = '200px';
                        img.style.margin = '10px';
                        img.style.border = '1px solid #ddd';
                        img.style.borderRadius = '5px';
                        previewContainer.appendChild(img);
                    };
                    reader.readAsDataURL(file);
                }
            });
        });
    });
});

function createImagePreviewContainer(input) {
    const container = document.createElement('div');
    container.id = 'image-preview';
    container.style.marginTop = '10px';
    input.parentNode.appendChild(container);
    return container;
}