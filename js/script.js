"use strict";

/* ==========================================================================
   SAAD ALI KHAN - PERSONAL PORTFOLIO SCRIPT
   Full Stack Developer | Laravel & PHP Specialist
   Vanilla JavaScript (ES6+) with zero external framework dependencies.
   ========================================================================== */

// --- 1. PROJECT DATASTORE FOR MODAL DETAILS ---
const PROJECTS_DATA = {
  practical: {
    title: "PractiCal Backend Platform",
    category: "Laravel / PHP / MySQL / REST API",
    badge: "Private / Production Project",
    overview: "A comprehensive production backend platform serving meal subscription operations. Manages complex user profiles, multi-tier subscription plans, custom meal schedules, digital wallets, order histories, and automated kitchen/delivery dispatch lists.",
    problem: "Handling high-concurrency order calculations, recurring subscriber wallet transactions, meal replacement rules, and custom dietary schedule updates while avoiding race conditions and ensuring 100% financial and delivery data consistency.",
    solution: "Architected a modular Laravel service layer with strict database transactions, custom Repository patterns for user state, idempotent wallet ledgers, and optimized MySQL queries for batch generation of subscriber meal lists.",
    techStack: ["PHP 8.x", "Laravel", "MySQL", "REST APIs", "Transaction Ledgers", "Cron / Queues", "cPanel / Apache"],
    responsibilities: [
      "Designed relational database schemas for users, plans, orders, wallet transactions, and delivery time slots.",
      "Implemented RESTful API endpoints consumed by mobile apps and frontend web interfaces.",
      "Built idempotent wallet transaction logic to handle recurring subscription billing & refund adjustments.",
      "Optimized query performance and daily cron processing for subscriber meal allocation logic.",
      "Fixed production concurrency bugs related to dietary preference updates and time-slot assignments."
    ]
  },
  wordpress: {
    title: "Enterprise WordPress Website Revamp",
    category: "WordPress / PHP / ACF / Elementor",
    badge: "Production Project (800+ Pages)",
    overview: "Large-scale modernization and restructuring of an enterprise WordPress website comprising over 800-900+ pages of dynamic content, multi-language pages, custom post types, and custom taxonomy structures.",
    problem: "The existing legacy legacy installation suffered from slow database queries, fragmented plugin bloat, broken page hierarchies, and unmaintainable hardcoded content blocks across hundreds of pages.",
    solution: "Executed a comprehensive architectural overhaul using Advanced Custom Fields (ACF Pro), custom PHP post types, streamlined Elementor templates, custom REST API integration, and clean MySQL database migration scripts.",
    techStack: ["WordPress", "PHP", "ACF Pro", "Elementor", "Custom Post Types", "MySQL", "PHP-FPM", "Nginx"],
    responsibilities: [
      "Restructured 800+ legacy pages into maintainable custom post types and ACF field groups.",
      "Developed custom PHP code snippets to bypass heavy plugin dependencies and improve server response times.",
      "Migrated massive database content cleanly while preserving SEO permalink structures.",
      "Optimized database autoload options and transient caches, drastically reducing TTFB (Time to First Byte)."
    ]
  },
  shopify: {
    title: "Shopify E-commerce Customization",
    category: "Shopify / Liquid / JavaScript",
    badge: "Production E-commerce Store",
    overview: "Frontend enhancement, liquid theme customization, and feature integration for a high-traffic production Shopify e-commerce store.",
    problem: "The store required custom product bundle selectors, custom checkout cart drawer mechanics, and responsive performance optimizations without slowing down Liquid template render speed.",
    solution: "Built vanilla JavaScript components interacting directly with Shopify AJAX Cart APIs, customized Liquid section schemas, and refactored responsive stylesheets for fast mobile page load.",
    techStack: ["Shopify Liquid", "JavaScript (ES6)", "AJAX Cart API", "CSS Grid/Flexbox", "Responsive UI"],
    responsibilities: [
      "Customized liquid templates, section files, and snippet components.",
      "Implemented a lightweight dynamic cart drawer using vanilla JS and Shopify REST APIs.",
      "Optimized mobile layout responsiveness and resolved cross-browser CSS rendering issues.",
      "Integrated third-party analytics and review widgets without compromising page performance."
    ]
  },
  payments: {
    title: "Payment Gateway Integrations",
    category: "API Integration / Payments / Security",
    badge: "Production Payment Integration",
    overview: "Secure integration of third-party payment gateways and payment verification service modules into custom PHP/Laravel and e-commerce platforms.",
    problem: "Ensuring zero-drop payment verification, preventing double-charge issues, validating SHA256 checksum signatures, and gracefully handling asynchronous webhook notifications from payment processors.",
    solution: "Developed robust API request wrappers, signature checksum verification handlers, fallback verification polling timers, and database audit logs to track every transaction lifecycle.",
    techStack: ["PHP / Laravel", "REST APIs", "Webhooks", "HMAC / SHA256", "Payment Logs", "cURL"],
    responsibilities: [
      "Implemented API authentication, request signing, and response checksum validations.",
      "Constructed secure webhook endpoint handlers with duplicate request idempotency checks.",
      "Built fallback verification routines to catch edge-case drop-offs during payment gateway redirects.",
      "Ensured strict security compliance by storing no raw card credentials and maintaining full transaction logs."
    ]
  }
};

// --- 2. DOM CONTENT LOADED EVENT HANDLER ---
document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initNavigation();
  initScrollReveal();
  initProjectModal();
  initCopyButtons();
  initContactForm();
  initCurrentYear();
});

/* --------------------------------------------------------------------------
   3. THEME TOGGLE (DARK/LIGHT MODE)
   -------------------------------------------------------------------------- */
function initThemeToggle() {
  const toggleBtn = document.getElementById("theme-toggle");
  if (!toggleBtn) return;

  // Saved theme or preference detection
  const savedTheme = localStorage.getItem("theme");
  const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  
  if (savedTheme === "light" || (!savedTheme && !systemPrefersDark)) {
    document.documentElement.setAttribute("data-theme", "light");
  } else {
    document.documentElement.removeAttribute("data-theme");
  }

  toggleBtn.addEventListener("click", () => {
    const isLight = document.documentElement.getAttribute("data-theme") === "light";
    if (isLight) {
      document.documentElement.removeAttribute("data-theme");
      localStorage.setItem("theme", "dark");
      showToast("Switched to Dark Mode");
    } else {
      document.documentElement.setAttribute("data-theme", "light");
      localStorage.setItem("theme", "light");
      showToast("Switched to Light Mode");
    }
  });
}

/* --------------------------------------------------------------------------
   4. NAVIGATION & MOBILE MENU & ACTIVE LINK
   -------------------------------------------------------------------------- */
function initNavigation() {
  const navbar = document.querySelector(".navbar");
  const mobileToggle = document.querySelector(".mobile-toggle");
  const navMenu = document.querySelector(".nav-menu");
  const navLinks = document.querySelectorAll(".nav-link");
  const sections = document.querySelectorAll("section[id]");

  // Scroll navbar styling
  window.addEventListener("scroll", () => {
    if (window.scrollY > 30) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });

  // Mobile menu toggle
  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener("click", () => {
      const isOpen = navMenu.classList.contains("active");
      if (isOpen) {
        navMenu.classList.remove("active");
        mobileToggle.classList.remove("active");
        mobileToggle.setAttribute("aria-expanded", "false");
      } else {
        navMenu.classList.add("active");
        mobileToggle.classList.add("active");
        mobileToggle.setAttribute("aria-expanded", "true");
      }
    });

    // Close menu when clicking link
    navLinks.forEach(link => {
      link.addEventListener("click", () => {
        navMenu.classList.remove("active");
        mobileToggle.classList.remove("active");
        mobileToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Active navigation highlight via IntersectionObserver
  if ("IntersectionObserver" in window && sections.length > 0) {
    const observerOptions = {
      root: null,
      rootMargin: "-20% 0px -60% 0px",
      threshold: 0
    };

    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const currentId = entry.target.getAttribute("id");
          navLinks.forEach(link => {
            if (link.getAttribute("href") === `#${currentId}`) {
              link.classList.add("active");
            } else {
              link.classList.remove("active");
            }
          });
        }
      });
    }, observerOptions);

    sections.forEach(section => sectionObserver.observe(section));
  }
}

/* --------------------------------------------------------------------------
   5. SCROLL REVEAL ANIMATIONS (WITH REDUCED MOTION RESPECT)
   -------------------------------------------------------------------------- */
function initScrollReveal() {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const reveals = document.querySelectorAll(".reveal");

  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    reveals.forEach(el => el.classList.add("revealed"));
    return;
  }

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("revealed");
        observer.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    threshold: 0.1,
    rootMargin: "0px 0px -40px 0px"
  });

  reveals.forEach(el => revealObserver.observe(el));
}

/* --------------------------------------------------------------------------
   6. PROJECT DETAILS MODAL HANDLER
   -------------------------------------------------------------------------- */
function initProjectModal() {
  const modalOverlay = document.getElementById("project-modal");
  const modalCloseBtn = document.getElementById("modal-close");
  const modalButtons = document.querySelectorAll("[data-project]");

  if (!modalOverlay) return;

  // Open modal
  modalButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const projectId = btn.getAttribute("data-project");
      const data = PROJECTS_DATA[projectId];

      if (!data) return;

      populateModal(data);
      modalOverlay.classList.add("active");
      modalOverlay.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      if (modalCloseBtn) modalCloseBtn.focus();
    });
  });

  // Close modal function
  const closeModal = () => {
    modalOverlay.classList.remove("active");
    modalOverlay.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  };

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener("click", closeModal);
  }

  // Backdrop click close
  modalOverlay.addEventListener("click", (e) => {
    if (e.target === modalOverlay) {
      closeModal();
    }
  });

  // Escape key close
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modalOverlay.classList.contains("active")) {
      closeModal();
    }
  });
}

function populateModal(data) {
  const titleEl = document.getElementById("modal-title");
  const categoryEl = document.getElementById("modal-category");
  const badgeEl = document.getElementById("modal-badge");
  const overviewEl = document.getElementById("modal-overview");
  const problemEl = document.getElementById("modal-problem");
  const solutionEl = document.getElementById("modal-solution");
  const techEl = document.getElementById("modal-tech");
  const respEl = document.getElementById("modal-resp");

  if (titleEl) titleEl.textContent = data.title;
  if (categoryEl) categoryEl.textContent = data.category;
  if (badgeEl) badgeEl.textContent = data.badge;
  if (overviewEl) overviewEl.textContent = data.overview;
  if (problemEl) problemEl.textContent = data.problem;
  if (solutionEl) solutionEl.textContent = data.solution;

  if (techEl) {
    techEl.innerHTML = data.techStack.map(t => `<span class="project-tag">${t}</span>`).join("");
  }

  if (respEl) {
    respEl.innerHTML = data.responsibilities.map(r => `<li>${r}</li>`).join("");
  }
}

/* --------------------------------------------------------------------------
   7. COPY TO CLIPBOARD & TOAST NOTIFICATIONS
   -------------------------------------------------------------------------- */
function initCopyButtons() {
  const copyCmdBtn = document.getElementById("copy-cmd-btn");
  const cmdText = document.getElementById("cmd-text");

  if (copyCmdBtn && cmdText) {
    copyCmdBtn.addEventListener("click", () => {
      copyToClipboard(cmdText.textContent.trim(), "Git clone command copied to clipboard!");
    });
  }
}

function copyToClipboard(text, message) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => {
      showToast(message);
    }).catch(() => {
      fallbackCopy(text, message);
    });
  } else {
    fallbackCopy(text, message);
  }
}

function fallbackCopy(text, message) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.left = "-9999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    document.execCommand('copy');
    showToast(message);
  } catch (err) {
    showToast("Copy failed, please copy manually.");
  }
  document.body.removeChild(textArea);
}

function showToast(message) {
  let toast = document.getElementById("toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "toast";
    toast.className = "toast";
    document.body.appendChild(toast);
  }

  toast.innerHTML = `
    <svg class="icon-svg" style="color: var(--accent-green);" viewBox="0 0 24 24">
      <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
    </svg>
    <span>${message}</span>
  `;

  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

/* --------------------------------------------------------------------------
   8. CONTACT FORM HANDLER
   -------------------------------------------------------------------------- */
function initContactForm() {
  const form = document.getElementById("contact-form");
  const statusEl = document.getElementById("form-status");

  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const nameInput = document.getElementById("name");
    const emailInput = document.getElementById("email");
    const messageInput = document.getElementById("message");

    const name = nameInput ? nameInput.value.trim() : "";
    const email = emailInput ? emailInput.value.trim() : "";
    const message = messageInput ? messageInput.value.trim() : "";

    if (!name || !email || !message) {
      showFormStatus("Please fill in all required fields.", "error");
      return;
    }

    if (!validateEmail(email)) {
      showFormStatus("Please enter a valid email address.", "error");
      return;
    }

    // Feedback for user (mailto fallback ready)
    showFormStatus("Thank you for reaching out! Opening mail client...", "success");

    // Optional mailto fallback URL trigger
    const mailtoUrl = `mailto:saadalikhan.dev@gmail.com?subject=${encodeURIComponent('Inquiry from Portfolio: ' + name)}&body=${encodeURIComponent(message + '\n\nSender Email: ' + email)}`;

    setTimeout(() => {
      window.location.href = mailtoUrl;
      form.reset();
    }, 1000);
  });

  function showFormStatus(msg, type) {
    if (!statusEl) return;
    statusEl.textContent = msg;
    statusEl.className = `form-status ${type}`;
  }

  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}

/* --------------------------------------------------------------------------
   9. DYNAMIC FOOTER YEAR
   -------------------------------------------------------------------------- */
function initCurrentYear() {
  const yearSpan = document.getElementById("current-year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }
}
