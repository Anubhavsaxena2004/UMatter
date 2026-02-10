/**
 * ANTI-GRAVITY ANIMATION SYSTEM - JavaScript
 * Smooth, Calm, Healing Motion for Mental Wellness
 * Handles: Scroll Triggers, Custom Cursor, Parallax, Smooth Interactions
 */

(function () {
    'use strict';

    // ========================================================================
    // 1. CUSTOM CURSOR SYSTEM
    // ========================================================================

    const initCustomCursor = () => {
        // Custom cursor disabled by user request
        return;
    };

    // ========================================================================
    // 2. SCROLL-TRIGGERED REVEAL ANIMATIONS
    // ========================================================================

    const initScrollReveal = () => {
        const revealElements = document.querySelectorAll(
            '.scroll-reveal, .scroll-reveal-left, .scroll-reveal-right, ' +
            '.scroll-fade, .scroll-scale, .scroll-stagger, .section-unfold'
        );

        const revealOnScroll = () => {
            const windowHeight = window.innerHeight;
            const revealPoint = 100; // pixels from bottom before reveal

            revealElements.forEach(element => {
                const elementTop = element.getBoundingClientRect().top;
                const elementVisible = revealPoint;

                if (elementTop < windowHeight - elementVisible) {
                    element.classList.add('revealed');
                }
            });
        };

        // Initial check
        revealOnScroll();

        // Throttled scroll listener for performance
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            if (scrollTimeout) {
                window.cancelAnimationFrame(scrollTimeout);
            }
            scrollTimeout = window.requestAnimationFrame(revealOnScroll);
        }, { passive: true });
    };

    // ========================================================================
    // 3. PARALLAX BACKGROUND EFFECT
    // ========================================================================

    const initParallax = () => {
        const parallaxLayers = document.querySelectorAll('.parallax-layer');

        if (parallaxLayers.length === 0) return;

        const handleParallax = () => {
            const scrolled = window.pageYOffset;

            parallaxLayers.forEach((layer, index) => {
                const speed = (index + 1) * 0.1; // Different speeds for each layer
                const yPos = -(scrolled * speed);
                layer.style.transform = `translateY(${yPos}px)`;
            });
        };

        // Throttled scroll listener
        let parallaxTimeout;
        window.addEventListener('scroll', () => {
            if (parallaxTimeout) {
                window.cancelAnimationFrame(parallaxTimeout);
            }
            parallaxTimeout = window.requestAnimationFrame(handleParallax);
        }, { passive: true });
    };

    // ========================================================================
    // 4. NAVBAR SCROLL BEHAVIOR
    // ========================================================================

    const initNavbarScroll = () => {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        let lastScrollTop = 0;
        const scrollThreshold = 100;

        const handleNavbarScroll = () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            // Add scrolled class for background
            if (scrollTop > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            // Hide navbar on scroll down, show on scroll up
            if (scrollTop > lastScrollTop && scrollTop > scrollThreshold) {
                navbar.classList.add('hidden');
            } else {
                navbar.classList.remove('hidden');
            }

            lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
        };

        let navbarTimeout;
        window.addEventListener('scroll', () => {
            if (navbarTimeout) {
                window.cancelAnimationFrame(navbarTimeout);
            }
            navbarTimeout = window.requestAnimationFrame(handleNavbarScroll);
        }, { passive: true });
    };

    // ========================================================================
    // 5. SMOOTH SCROLL FOR ANCHOR LINKS
    // ========================================================================

    const initSmoothScroll = () => {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');

                // Ignore empty anchors
                if (href === '#' || href === '#!') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();

                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    };

    // ========================================================================
    // 6. PROGRESSIVE TEXT REVEAL
    // ========================================================================

    const initTextReveal = () => {
        const revealTexts = document.querySelectorAll('.reveal-text');

        revealTexts.forEach(element => {
            const text = element.textContent;
            element.innerHTML = '';

            text.split('').forEach((char, index) => {
                const span = document.createElement('span');
                span.textContent = char === ' ' ? '\u00A0' : char;
                span.style.animationDelay = `${index * 0.03}s`;
                element.appendChild(span);
            });
        });
    };

    // ========================================================================
    // 7. FLOATING SHAPES BACKGROUND
    // ========================================================================

    const initFloatingShapes = () => {
        // Check if parallax background exists
        let parallaxBg = document.querySelector('.parallax-bg');

        if (!parallaxBg) {
            parallaxBg = document.createElement('div');
            parallaxBg.className = 'parallax-bg';
            document.body.insertBefore(parallaxBg, document.body.firstChild);
        }

        // Create floating shapes
        const shapes = [
            { class: 'floating-shape floating-shape-1' },
            { class: 'floating-shape floating-shape-2' },
            { class: 'floating-shape floating-shape-3' }
        ];

        shapes.forEach(shape => {
            const div = document.createElement('div');
            div.className = shape.class;
            parallaxBg.appendChild(div);
        });
    };

    // ========================================================================
    // 8. PAGE LOAD ANIMATION
    // ========================================================================

    const initPageTransition = () => {
        document.body.classList.add('page-transition');
    };

    // ========================================================================
    // 9. CARD INTERACTION ENHANCEMENTS
    // ========================================================================

    const initCardInteractions = () => {
        const cards = document.querySelectorAll('.card');

        cards.forEach(card => {
            // Add magnetic effect on mouse move
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const deltaX = (x - centerX) / centerX;
                const deltaY = (y - centerY) / centerY;

                const tiltX = deltaY * 5; // Max 5 degrees
                const tiltY = -deltaX * 5;

                card.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-12px) scale(1.02)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    };

    // ========================================================================
    // 10. INITIALIZE ALL ANIMATIONS
    // ========================================================================

    const init = () => {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Initialize all animation systems
        // initCustomCursor(); // Disabled by user request
        initScrollReveal();
        initParallax();
        initNavbarScroll();
        initSmoothScroll();
        initTextReveal();
        initFloatingShapes();
        initPageTransition();
        initCardInteractions();

        console.log('🌊 Anti-Gravity Animation System Initialized');
    };

    // Start initialization
    init();

})();
