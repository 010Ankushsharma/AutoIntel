/**
 * Car Price Prediction - Frontend JavaScript
 * Handles form validation, AJAX calls, and UI interactions
 */

// DOM Elements
const predictionForm = document.getElementById('predictionForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');
const spinner = document.querySelector('.spinner');

// Form Validation
function validateForm(formData) {
    const errors = [];
    
    // Validate Year
    const year = parseInt(formData.get('year'));
    if (isNaN(year) || year < 2000 || year > 2026) {
        errors.push('Please enter a valid manufacturing year (2000-2026)');
    }
    
    // Validate Kilometers Driven
    const kmDriven = parseFloat(formData.get('km_driven'));
    if (isNaN(kmDriven) || kmDriven < 0) {
        errors.push('Please enter valid kilometers driven');
    }
    
    // Validate Engine Capacity
    const engine = parseFloat(formData.get('engine'));
    if (isNaN(engine) || engine <= 0) {
        errors.push('Please enter valid engine capacity');
    }
    
    // Validate Mileage
    const mileage = parseFloat(formData.get('mileage'));
    if (isNaN(mileage) || mileage < 0) {
        errors.push('Please enter valid mileage');
    }
    
    // Validate Max Power
    const maxPower = parseFloat(formData.get('max_power'));
    if (isNaN(maxPower) || maxPower < 0) {
        errors.push('Please enter valid max power');
    }
    
    // Validate Seats
    const seats = parseInt(formData.get('seats'));
    if (isNaN(seats) || seats < 2 || seats > 10) {
        errors.push('Please enter valid number of seats (2-10)');
    }
    
    return errors;
}

// Show Loading State
function showLoading() {
    if (btnText && btnLoader) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'flex';
    }
    if (submitBtn) {
        submitBtn.disabled = true;
    }
}

// Hide Loading State
function hideLoading() {
    if (btnText && btnLoader) {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
    if (submitBtn) {
        submitBtn.disabled = false;
    }
}

// Show Error Message
function showError(message) {
    // Remove existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <span class="error-icon">⚠️</span>
        ${message}
    `;
    
    // Insert after section header
    const sectionHeader = document.querySelector('.section-header');
    if (sectionHeader) {
        sectionHeader.insertAdjacentElement('afterend', errorDiv);
        
        // Scroll to error
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            errorDiv.style.opacity = '0';
            errorDiv.style.transition = 'opacity 0.5s ease';
            setTimeout(() => errorDiv.remove(), 500);
        }, 10000);
    }
}

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Add Animation on Scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.feature-card, .stat-card, .step-card, .tech-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
}

// Initialize animations when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

function init() {
    animateOnScroll();
    
    // Add hover effects to cards
    addCardHoverEffects();
    
    // Initialize tooltips if any
    initializeTooltips();
}

// Add Enhanced Hover Effects
function addCardHoverEffects() {
    const cards = document.querySelectorAll('.feature-card, .stat-card, .step-card, .tech-card, .range-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            setTimeout(() => {
                this.style.transform = 'translateY(0)';
            }, 100);
        });
    });
}

// Initialize Tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.position = 'absolute';
            tooltip.style.background = 'rgba(0, 0, 0, 0.9)';
            tooltip.style.color = '#fff';
            tooltip.style.padding = '0.5rem 1rem';
            tooltip.style.borderRadius = '5px';
            tooltip.style.fontSize = '0.85rem';
            tooltip.style.zIndex = '1000';
            tooltip.style.pointerEvents = 'none';
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
            
            this._tooltip = tooltip;
        });
        
        el.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Number Formatting Helper
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Currency Formatter
function formatCurrency(amount) {
    return `₹${formatNumber(Math.round(amount))}`;
}

// Input Field Enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add focus effects to input fields
    const inputs = document.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.2s ease';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
    
    // Auto-format large numbers in km_driven field
    const kmInput = document.getElementById('km_driven');
    if (kmInput) {
        kmInput.addEventListener('blur', function() {
            const value = parseInt(this.value);
            if (value > 10000) {
                // Optional: Add visual formatting hint
                console.log(`Kilometers entered: ${formatNumber(value)}`);
            }
        });
    }
});

// Performance monitoring - Log page load time
window.addEventListener('load', function() {
    if (window.performance) {
        const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
    }
});

// Service Worker Registration (Optional - for PWA support)
if ('serviceWorker' in navigator) {
    // Uncomment below to enable PWA features
    // navigator.serviceWorker.register('/sw.js')
    //     .then(registration => console.log('SW registered:', registration))
    //     .catch(error => console.log('SW registration failed:', error));
}

console.log('AutoIntel Application Initialized Successfully! 🚗');
