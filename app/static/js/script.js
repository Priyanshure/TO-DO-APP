// ===== NAVBAR TOGGLE (Mobile) =====
const navToggle = document.getElementById('navToggle');
const navLinks = document.querySelector('.nav-links');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const icon = navToggle.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    });
}

// Close nav when clicking outside
document.addEventListener('click', (e) => {
    if (navLinks && !e.target.closest('.nav-container')) {
        navLinks.classList.remove('active');
        const icon = navToggle?.querySelector('i');
        if (icon) {
            icon.classList.add('fa-bars');
            icon.classList.remove('fa-times');
        }
    }
});

// ===== TOGGLE PASSWORD VISIBILITY =====
function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// ===== FORM VALIDATION =====
document.querySelectorAll('.auth-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const inputs = this.querySelectorAll('input[required]');
        let valid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                valid = false;
                input.style.borderColor = 'var(--danger)';
                input.addEventListener('input', function handler() {
                    input.style.borderColor = '';
                    input.removeEventListener('input', handler);
                });
            }
        });

        // Check password match on register
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        if (password && confirmPassword) {
            if (password.value !== confirmPassword.value) {
                valid = false;
                confirmPassword.style.borderColor = 'var(--danger)';
                confirmPassword.setCustomValidity('Passwords do not match');
            } else {
                confirmPassword.setCustomValidity('');
            }
        }

        if (!valid) {
            e.preventDefault();
            shakeElement(form);
        }
    });
});

// ===== SHAKE ANIMATION =====
function shakeElement(el) {
    el.style.animation = 'none';
    el.offsetHeight; // Trigger reflow
    el.style.animation = 'shake 0.5s ease';
}

// Add shake keyframes dynamically
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
`;
document.head.appendChild(shakeStyle);

// ===== AUTO-DISMISS ALERTS =====
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
});

// ===== TASK ITEM HOVER EFFECT =====
document.querySelectorAll('.task-item').forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.style.borderLeftWidth = '6px';
    });
    item.addEventListener('mouseleave', function() {
        this.style.borderLeftWidth = '4px';
    });
});

// ===== CONFIRM DELETE =====
document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', function(e) {
        if (!confirm('Are you sure you want to delete this task?')) {
            e.preventDefault();
            e.stopPropagation();
        }
    });
});

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', (e) => {
    // Escape closes modal
    if (e.key === 'Escape') {
        const modal = document.getElementById('editModal');
        if (modal) modal.classList.remove('active');
    }

    // Ctrl+N focuses on new task input
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        const taskTitle = document.getElementById('taskTitle');
        if (taskTitle) taskTitle.focus();
    }
});

// ===== SMOOTH SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ===== INTERSECTION OBSERVER FOR ANIMATIONS =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.task-item, .stat-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.4s ease';
    observer.observe(el);
});

// ===== CONSOLE WELCOME =====
console.log(
    '%c TaskFlow %c To-Do App ',
    'background: #6c5ce7; color: white; padding: 5px 10px; border-radius: 5px 0 0 5px; font-weight: bold;',
    'background: #a29bfe; color: white; padding: 5px 10px; border-radius: 0 5px 5px 0;'
);