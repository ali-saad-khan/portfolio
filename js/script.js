"use strict";

/* ==========================================================================
   SAAD ALI KHAN - PERSONAL PORTFOLIO SCRIPT
   Full Stack Developer | Laravel & PHP Specialist
   Vanilla JavaScript (ES6+) with zero external framework dependencies.
   ========================================================================== */

// --- DOM CONTENT LOADED EVENT HANDLER ---
document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initNavigation();
  initScrollReveal();
  initCopyButtons();
  initContactForm();
  initCurrentYear();
  initScrollProgress();
  initTyped();
  initCounters();
  initMarquee();
  initSpotlight();
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
        // Drop the stagger delay once shown so hover effects stay snappy
        setTimeout(() => { entry.target.style.transitionDelay = "0s"; }, 1000);
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
// Paste a Formspree / Web3Forms endpoint here to receive messages directly.
// While empty, the form falls back to opening the visitor's mail client.
const CONTACT_ENDPOINT = "https://formspree.io/f/xvkzrrev";
const CONTACT_EMAIL = "saadalikhan0210@gmail.com";

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

    // Honeypot: real visitors never fill this hidden field
    const trap = form.querySelector('input[name="website"]');
    if (trap && trap.value) return;

    const mailto = () => {
      const subject = encodeURIComponent("Project inquiry from " + name);
      const body = encodeURIComponent(message + "\n\nReply to: " + email);
      window.location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;
    };

    if (!CONTACT_ENDPOINT) {
      showFormStatus("Opening your email app to send this message...", "success");
      setTimeout(() => { mailto(); form.reset(); }, 600);
      return;
    }

    const btn = form.querySelector('button[type="submit"]');
    if (btn) btn.disabled = true;
    showFormStatus("Sending...", "success");

    fetch(CONTACT_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({ name, email, message })
    })
      .then((res) => {
        if (!res.ok) throw new Error("Request failed");
        showFormStatus("Thanks! Your message is in. I'll reply by email.", "success");
        form.reset();
      })
      .catch(() => {
        showFormStatus(`Couldn't send. Please email ${CONTACT_EMAIL} directly.`, "error");
      })
      .finally(() => { if (btn) btn.disabled = false; });
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

/* --------------------------------------------------------------------------
   10. MODERN VISUAL EFFECTS
   -------------------------------------------------------------------------- */
const REDUCED_MOTION = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function initScrollProgress() {
  const bar = document.getElementById("scroll-progress");
  if (!bar) return;
  const update = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = `scaleX(${max > 0 ? Math.min(window.scrollY / max, 1) : 0})`;
  };
  window.addEventListener("scroll", update, { passive: true });
  update();
}

function initTyped() {
  const el = document.getElementById("typed-text");
  if (!el || REDUCED_MOTION) return;
  const phrases = ["full stack web apps", "React & TypeScript interfaces", "secure Laravel backends", "payment & wallet systems", "e-commerce platforms"];
  let phrase = 0, char = 0, deleting = false;

  const tick = () => {
    const text = phrases[phrase];
    char += deleting ? -1 : 1;
    el.textContent = text.slice(0, char);

    let delay = deleting ? 35 : 70;
    if (!deleting && char === text.length) { deleting = true; delay = 1800; }
    else if (deleting && char === 0) { deleting = false; phrase = (phrase + 1) % phrases.length; delay = 350; }
    setTimeout(tick, delay);
  };
  el.textContent = "";
  setTimeout(tick, 400);
}

function initCounters() {
  const counters = document.querySelectorAll("[data-count]");
  if (!counters.length || REDUCED_MOTION || !("IntersectionObserver" in window)) return;

  const run = (el) => {
    const target = parseInt(el.dataset.count, 10);
    const suffix = el.dataset.suffix || "";
    const duration = 1400;
    const start = performance.now();
    const step = (now) => {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) { run(entry.target); observer.unobserve(entry.target); }
    });
  }, { threshold: 0.6 });
  counters.forEach((el) => observer.observe(el));
}

function initMarquee() {
  const track = document.getElementById("marquee-track");
  if (!track) return;
  // Duplicate the items so translating by -50% loops seamlessly
  track.innerHTML += track.innerHTML;
}

function initSpotlight() {
  const cards = document.querySelectorAll(
    ".stat-card, .skill-category, .project-card, .service-card, .step-card, .contact-card, .timeline-card, .highlights-box"
  );
  cards.forEach((card) => {
    card.addEventListener("pointermove", (e) => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty("--mx", `${e.clientX - rect.left}px`);
      card.style.setProperty("--my", `${e.clientY - rect.top}px`);
    });
  });
}
