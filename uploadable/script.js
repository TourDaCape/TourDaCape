// Tour Da Cape JavaScript Functionality
// Version: 1.0

// Document Ready Function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initMobileMenu();
    initContactForm();
    initPopupHandlers();
    initSmoothScrolling();
    initFormValidation();
    initHeroCarousel();
    initRevealOnScroll();
    initWhatsAppChatWidget();
    initCategoryFilter();
    injectWhatsAppFloat();
});

// Mobile Menu Toggle
function initMobileMenu() {
    const mobileMenuButtons = document.querySelectorAll('.mobile_menu_bar');
    const mobileNavs = document.querySelectorAll('.mobile_nav');
    
    mobileMenuButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            const mobileNav = mobileNavs[index];
            mobileNav.classList.toggle('closed');
            mobileNav.classList.toggle('opened');
            
            // Toggle aria-expanded attribute
            const isExpanded = mobileNav.classList.contains('opened');
            this.setAttribute('aria-expanded', isExpanded);
        });
    });
}

// Contact Form Handling
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            // Validate; if invalid, block submission
            if (!validateContactForm()) {
                return;
            }
            // Gather data
            const payload = {
                name: document.querySelector('input[name="name"]').value.trim(),
                email: document.querySelector('input[name="email"]').value.trim(),
                phone: document.querySelector('input[name="phone"]').value.trim(),
                interest: document.querySelector('select[name="interest"]').value,
                message: document.querySelector('textarea[name="message"]').value.trim()
            };
            const statusEl = document.getElementById('formStatus');
            statusEl.textContent = 'Sending your enquiry...';
            try {
                const res = await fetch('/submit-enquiry', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (res.ok) {
                    statusEl.textContent = 'Enquiry sent successfully. We will contact you soon.';
                    contactForm.reset();
                    showFormSuccess();
                } else {
                    const text = await res.text();
                    statusEl.textContent = `Unable to send at the moment: ${text || 'Please try WhatsApp or email us.'}`;
                }
            } catch (err) {
                statusEl.textContent = 'Network error. Please try WhatsApp or email us.';
                console.error('Form submit error', err);
            }
        });
    }
}

// Form Validation
function validateContactForm() {
    const name = document.querySelector('input[name="name"]');
    const email = document.querySelector('input[name="email"]');
    const message = document.querySelector('textarea[name="message"]');
    
    let isValid = true;
    
    // Clear previous errors
    clearFormErrors();
    
    // Validate name
    if (!name.value.trim()) {
        showFieldError(name, 'Please enter your name');
        isValid = false;
    }
    
    // Validate email
    if (!email.value.trim()) {
        showFieldError(email, 'Please enter your email address');
        isValid = false;
    } else if (!isValidEmail(email.value.trim())) {
        showFieldError(email, 'Please enter a valid email address');
        isValid = false;
    }
    
    // Validate message
    if (!message.value.trim()) {
        showFieldError(message, 'Please enter your message');
        isValid = false;
    }
    
    return isValid;
}

// Email Validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Show Field Error
function showFieldError(field, message) {
    field.classList.add('error');
    
    // Create error message element
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.color = '#d32f2f';
    errorElement.style.fontSize = '14px';
    errorElement.style.marginTop = '5px';
    
    // Insert error message after field
    field.parentNode.insertBefore(errorElement, field.nextSibling);
}

// Clear Form Errors
function clearFormErrors() {
    // Remove error classes
    const errorFields = document.querySelectorAll('.error');
    errorFields.forEach(field => field.classList.remove('error'));
    
    // Remove error messages
    const errorMessages = document.querySelectorAll('.field-error');
    errorMessages.forEach(error => error.remove());
}

// Show Form Success
function showFormSuccess() {
    // Create success message
    const successMessage = document.createElement('div');
    successMessage.className = 'form-success';
    successMessage.textContent = 'Thank you for your message! We will get back to you soon.';
    successMessage.style.backgroundColor = '#4caf50';
    successMessage.style.color = 'white';
    successMessage.style.padding = '15px';
    successMessage.style.borderRadius = '4px';
    successMessage.style.marginBottom = '20px';
    successMessage.style.textAlign = 'center';
    
    // Insert success message before form
    const contactForm = document.getElementById('contactForm');
    contactForm.parentNode.insertBefore(successMessage, contactForm);
    
    // Remove success message after 5 seconds
    setTimeout(() => {
        if (successMessage.parentNode) {
            successMessage.parentNode.removeChild(successMessage);
        }
    }, 5000);
}

// Popup Handlers
function initPopupHandlers() {
    // Enquire Now button
    const enquireButtons = document.querySelectorAll('.popmake-6259');
    enquireButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // In a real implementation, this would open a modal
            alert('Enquire Now popup would open here');
        });
    });
    
    // Newsletter signup
    const newsletterButton = document.querySelector('#newsletter');
    if (newsletterButton) {
        newsletterButton.addEventListener('click', function(e) {
            e.preventDefault();
            // In a real implementation, this would open a newsletter signup modal
            alert('Newsletter signup popup would open here');
        });
    }
}

// Smooth Scrolling
function initSmoothScrolling() {
    // Add smooth scrolling to all links with hashes
    const links = document.querySelectorAll('a[href*="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Check if link is to an anchor on the same page
            if (this.hash !== "" && this.pathname === window.location.pathname) {
                e.preventDefault();
                
                const hash = this.hash;
                const target = document.querySelector(hash);
                
                if (target) {
                    // Scroll to target
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Update URL without page jump
                    history.pushState(null, null, hash);
                }
            }
        });
    });
}

// Form Validation for Newsletter Signup
function initFormValidation() {
    // Newsletter signup form validation would go here
    // This is a placeholder for future implementation
    console.log('Form validation initialized');
}

// Hero Carousel Functionality
function initHeroCarousel() {
    const carouselSections = document.querySelectorAll('.hero-carousel');
    if (!carouselSections.length) return;

    carouselSections.forEach((section) => {
        const container = section.querySelector('.carousel') || section;
        const slides = container.querySelectorAll('.carousel-slide');
        const indicators = container.querySelectorAll('.carousel-indicators .dot');

        if (!slides.length) return;

        let currentSlide = 0;
        const slideCount = slides.length;
        const intervalAttr = container.getAttribute('data-interval') || section.getAttribute('data-interval');
        const intervalMs = intervalAttr && !isNaN(parseInt(intervalAttr, 10)) ? parseInt(intervalAttr, 10) : 5000;

        function showSlide(index) {
            slides.forEach((slide) => slide.classList.remove('active'));
            indicators.forEach((dot) => dot.classList.remove('active'));

            const slideEl = slides[index];
            if (slideEl) slideEl.classList.add('active');
            if (indicators.length && indicators[index]) indicators[index].classList.add('active');

            currentSlide = index;
        }

        function nextSlide() {
            const nextIndex = (currentSlide + 1) % slideCount;
            showSlide(nextIndex);
        }

        indicators.forEach((dot, index) => {
            dot.addEventListener('click', () => showSlide(index));
        });

        // Initialize first slide
        showSlide(0);

        // Start automatic rotation
        setInterval(nextSlide, intervalMs);
    });
}

// Category Filter for Tours Page
function initCategoryFilter() {
    const filterBar = document.querySelector('.category-filter');
    if (!filterBar) return;

    const buttons = filterBar.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.tours-content .tour-card');
    const sections = document.querySelectorAll('.tours-content .tour-category');

    function applyFilter(filter) {
        cards.forEach(card => {
            const category = card.getAttribute('data-category');
            const show = filter === 'all' || category === filter;
            card.style.display = show ? '' : 'none';
        });

        // Hide sections that have no visible cards
        sections.forEach(section => {
            const visible = Array.from(section.querySelectorAll('.tour-card')).some(card => card.style.display !== 'none');
            if (visible) {
                section.classList.remove('category-hidden');
            } else {
                section.classList.add('category-hidden');
            }
        });
    }

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active states
            buttons.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-pressed', 'false');
            });
            btn.classList.add('active');
            btn.setAttribute('aria-pressed', 'true');

            const filter = btn.getAttribute('data-filter');
            applyFilter(filter);
        });
    });

    // Initial state: show all
    applyFilter('all');
}

// Reveal on Scroll using IntersectionObserver
function initRevealOnScroll() {
    const revealSelector = '.hero-image, .feature-img, .tour-img, .about-img, .team-img, .value-img, .et_pb_image_wrap img';
    const elements = document.querySelectorAll(revealSelector);
    if (!elements.length) return;

    elements.forEach(el => el.classList.add('reveal'));

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-in', 'fade-up');
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

    elements.forEach(el => observer.observe(el));
}

// WhatsApp Chat Bot (Neville)
function initWhatsAppChatWidget() {
    const button = document.getElementById('whatsapp-chat-button');
    if (!button) return; // Only on pages where the widget exists (home page)
    button.addEventListener('click', function(e) {
        e.preventDefault();
        openWhatsAppChat();
    });
}

const whatsappBot = { name: 'Neville', number: '27616219784' };

function openWhatsAppChat() {
    const prefill = encodeURIComponent(`Hi ${whatsappBot.name}, I would like to enquire.`);
    const url = `https://wa.me/${whatsappBot.number}?text=${prefill}`;
    window.open(url, '_blank');
}
// Ensure global access for inline onclick attributes
window.openWhatsAppChat = openWhatsAppChat;

// Floating WhatsApp button (clean, no avatar)
function injectWhatsAppFloat() {
    // Only show on Home page
    const path = (window.location.pathname || '').toLowerCase();
    const isHome = path.endsWith('/index.html') || path === '/' || path === '';
    if (!isHome) return;
    if (document.querySelector('.whatsapp-float')) return; // avoid duplicates
    const container = document.createElement('div');
    container.className = 'whatsapp-float';
    container.setAttribute('aria-label', 'Chat on WhatsApp');

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'whatsapp-button';
    button.innerHTML = '<i class="fab fa-whatsapp"></i> Chat with Neville';
    button.addEventListener('click', function(e) {
        e.preventDefault();
        openWhatsAppChat();
    });

    container.appendChild(button);
    document.body.appendChild(container);
}

// Utility Functions
function debounce(func, wait, immediate) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Window Resize Handler
window.addEventListener('resize', debounce(function() {
    // Handle window resize events
    console.log('Window resized');
}, 250));

// Scroll Handler
window.addEventListener('scroll', debounce(function() {
    // Handle scroll events
    const scrollPosition = window.scrollY;
    
    // Example: Add class to header when scrolled
    const header = document.querySelector('.et-l--header');
    if (header) {
        if (scrollPosition > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
}, 10));

// Animation on Scroll
function initAnimationOnScroll() {
    const waypoints = document.querySelectorAll('.et-waypoint');
    
    waypoints.forEach(waypoint => {
        // Check if element is in viewport
        const rect = waypoint.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        
        if (rect.top <= windowHeight * 0.75) {
            waypoint.classList.add('et-animated');
        }
    });
}

// Initialize animation on scroll
window.addEventListener('scroll', debounce(initAnimationOnScroll, 100));
window.addEventListener('load', initAnimationOnScroll);

// Export functions for potential use in other scripts
window.TourDaCape = {
    initMobileMenu,
    initContactForm,
    initPopupHandlers,
    initSmoothScrolling,
    initFormValidation,
    validateContactForm,
    showFormSuccess,
    initHeroCarousel,
    openWhatsAppChat
};

// Console message for debugging
console.log('Tour Da Cape JavaScript loaded successfully');