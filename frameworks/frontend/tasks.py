"""
Frontend (HTML/CSS/JS) framework tasks with detailed expert-level instructions.
Based on WCAG 2.1, Core Web Vitals, and modern web standards.
"""
from typing import Dict, List
from crewai import Agent, Task
from frameworks.base import BaseTasks


class FrontendTasks(BaseTasks):
    """Factory for Frontend-specific tasks with comprehensive instructions."""
    
    @property
    def framework_name(self) -> str:
        return "Frontend"
    
    def frontend_architecture_task(self, agent: Agent, analysis: Dict) -> Task:
        return self.create_architecture_task(
            agent=agent,
            analysis=analysis,
            description="""\
                Design accessible, performant frontend architecture.
                
                **REQUIREMENTS:**
                {requirements}
                
                **FILES TO MODIFY:** {files_to_modify}
                **FILES TO CREATE:** {files_to_create}
                
                ---
                
                **DELIVERABLES:**
                
                1. **HTML Document Structure**
                   ```
                   Page: [page name]
                   Landmarks:
                     - header (banner)
                     - nav (navigation)
                     - main (main content)
                     - aside (complementary)
                     - footer (contentinfo)
                   
                   Heading Hierarchy:
                     - h1: [main page title]
                     - h2: [section titles]
                     - h3: [subsections]
                   
                   Interactive Elements:
                     - Forms (inputs, labels, error handling)
                     - Buttons (primary, secondary actions)
                     - Links (navigation, external)
                     - Modals/Dialogs (if needed)
                   ```
                
                2. **CSS Architecture**
                   ```
                   Methodology: BEM + Utility classes
                   
                   Custom Properties:
                     --color-primary: #value
                     --color-text: #value
                     --font-family: value
                     --spacing-unit: value
                   
                   Breakpoints:
                     --bp-sm: 576px
                     --bp-md: 768px
                     --bp-lg: 992px
                     --bp-xl: 1200px
                   
                   File Structure:
                     styles/
                     ├── base/          # Reset, typography
                     ├── components/    # BEM components
                     ├── layout/        # Grid, containers
                     ├── utilities/     # Helper classes
                     └── main.css       # Imports all
                   ```
                
                3. **JavaScript Architecture**
                   ```
                   Pattern: Module pattern with ES6+
                   
                   Modules:
                     - ModuleName
                       Purpose: [description]
                       Dependencies: [other modules]
                       Events: [events it handles]
                       Public API: [exposed methods]
                   
                   File Structure:
                     js/
                     ├── main.js        # Entry, initializes modules
                     ├── modules/       # Feature modules
                     └── utils/         # Pure functions
                   ```
                
                4. **Accessibility Plan (WCAG 2.1 AA)**
                   ```
                   Keyboard Navigation:
                     - Tab order: [list interactive elements in order]
                     - Focus management: [modals, dynamic content]
                     - Keyboard shortcuts: [if any]
                   
                   Screen Reader Support:
                     - ARIA landmarks: [roles to use]
                     - Live regions: [for dynamic updates]
                     - Labels: [buttons, form fields]
                   
                   Visual Accessibility:
                     - Color contrast: 4.5:1 minimum
                     - Focus indicators: 2px solid outline
                     - Text sizing: rem units, scalable
                   ```
                
                5. **Performance Plan**
                   ```
                   Loading Strategy:
                     - Critical CSS: inline in <head>
                     - Non-critical CSS: load async
                     - JavaScript: defer or async
                     - Images: lazy loading
                   
                   Target Metrics:
                     - LCP: < 2.5s
                     - FID: < 100ms
                     - CLS: < 0.1
                   ```
                
                {incentive}""",
            expected_output="""\
                Complete frontend architecture document with:
                - HTML structure with landmarks and heading hierarchy
                - CSS architecture with custom properties and BEM
                - JavaScript module design
                - WCAG 2.1 AA accessibility plan
                - Performance optimization strategy
                - File organization""",
        )
    
    def frontend_implementation_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_implementation_task(
            agent=agent,
            context=context,
            description="""\
                Implement accessible, performant frontend code.
                
                **IMPLEMENTATION STANDARDS:**
                
                1. **HTML Structure**
                   ```html
                   <!DOCTYPE html>
                   <html lang="en">
                   <head>
                       <meta charset="UTF-8">
                       <meta name="viewport" content="width=device-width, initial-scale=1.0">
                       <meta name="description" content="[page description]">
                       <title>[Page Title] | [Site Name]</title>
                       
                       <!-- Preconnect to external domains -->
                       <link rel="preconnect" href="https://fonts.googleapis.com">
                       
                       <!-- Critical CSS inline -->
                       <style>
                           /* Critical above-the-fold styles */
                       </style>
                       
                       <!-- Non-critical CSS -->
                       <link rel="stylesheet" href="styles/main.css" media="print" onload="this.media='all'">
                   </head>
                   <body>
                       <!-- Skip link (first element) -->
                       <a href="#main-content" class="skip-link">Skip to main content</a>
                       
                       <header>
                           <nav aria-label="Main navigation">
                               <!-- Navigation -->
                           </nav>
                       </header>
                       
                       <main id="main-content">
                           <!-- Page content -->
                       </main>
                       
                       <footer>
                           <!-- Footer content -->
                       </footer>
                       
                       <!-- JavaScript at end, with defer -->
                       <script src="js/main.js" defer></script>
                   </body>
                   </html>
                   ```
                
                2. **Accessible Forms**
                   ```html
                   <form action="/submit" method="POST" novalidate data-validate>
                       <div class="form-group">
                           <label for="name">
                               Full Name
                               <span class="required" aria-hidden="true">*</span>
                           </label>
                           <input 
                               type="text" 
                               id="name" 
                               name="name"
                               required
                               aria-required="true"
                               aria-describedby="name-error"
                               autocomplete="name"
                           >
                           <p id="name-error" class="error" role="alert" hidden></p>
                       </div>
                       
                       <div class="form-group">
                           <label for="email">
                               Email Address
                               <span class="required" aria-hidden="true">*</span>
                           </label>
                           <input 
                               type="email" 
                               id="email" 
                               name="email"
                               required
                               aria-required="true"
                               aria-describedby="email-hint email-error"
                               autocomplete="email"
                           >
                           <p id="email-hint" class="hint">We'll never share your email.</p>
                           <p id="email-error" class="error" role="alert" hidden></p>
                       </div>
                       
                       <button type="submit" class="btn btn--primary">
                           Submit
                       </button>
                   </form>
                   ```
                
                3. **CSS with Custom Properties**
                   ```css
                   /* Base: Custom Properties */
                   :root {
                       /* Colors */
                       --color-primary: #0066cc;
                       --color-primary-dark: #004999;
                       --color-text: #333333;
                       --color-text-light: #666666;
                       --color-background: #ffffff;
                       --color-error: #cc0000;
                       --color-success: #008000;
                       
                       /* Typography */
                       --font-family: system-ui, -apple-system, sans-serif;
                       --font-size-base: 1rem;
                       --line-height: 1.5;
                       
                       /* Spacing */
                       --spacing-xs: 0.25rem;
                       --spacing-sm: 0.5rem;
                       --spacing-md: 1rem;
                       --spacing-lg: 1.5rem;
                       --spacing-xl: 2rem;
                       
                       /* Focus */
                       --focus-outline: 2px solid var(--color-primary);
                       --focus-offset: 2px;
                   }
                   
                   /* Dark mode */
                   @media (prefers-color-scheme: dark) {
                       :root {
                           --color-text: #f0f0f0;
                           --color-background: #1a1a1a;
                       }
                   }
                   
                   /* Reduced motion */
                   @media (prefers-reduced-motion: reduce) {
                       *, *::before, *::after {
                           animation-duration: 0.01ms !important;
                           transition-duration: 0.01ms !important;
                       }
                   }
                   
                   /* Focus styles */
                   :focus {
                       outline: var(--focus-outline);
                       outline-offset: var(--focus-offset);
                   }
                   
                   :focus:not(:focus-visible) {
                       outline: none;
                   }
                   
                   :focus-visible {
                       outline: var(--focus-outline);
                       outline-offset: var(--focus-offset);
                   }
                   
                   /* Skip link */
                   .skip-link {
                       position: absolute;
                       top: -100%;
                       left: var(--spacing-md);
                       z-index: 9999;
                       padding: var(--spacing-sm) var(--spacing-md);
                       background: var(--color-primary);
                       color: white;
                       text-decoration: none;
                       border-radius: 0 0 4px 4px;
                   }
                   
                   .skip-link:focus {
                       top: 0;
                   }
                   
                   /* Visually hidden */
                   .visually-hidden {
                       position: absolute;
                       width: 1px;
                       height: 1px;
                       padding: 0;
                       margin: -1px;
                       overflow: hidden;
                       clip: rect(0, 0, 0, 0);
                       white-space: nowrap;
                       border: 0;
                   }
                   
                   /* BEM Components */
                   .btn {
                       display: inline-flex;
                       align-items: center;
                       justify-content: center;
                       padding: var(--spacing-sm) var(--spacing-md);
                       font-family: inherit;
                       font-size: var(--font-size-base);
                       line-height: var(--line-height);
                       text-decoration: none;
                       border: 2px solid transparent;
                       border-radius: 4px;
                       cursor: pointer;
                       transition: background-color 0.2s, border-color 0.2s;
                   }
                   
                   .btn--primary {
                       background-color: var(--color-primary);
                       color: white;
                   }
                   
                   .btn--primary:hover,
                   .btn--primary:focus {
                       background-color: var(--color-primary-dark);
                   }
                   ```
                
                4. **JavaScript Modules**
                   ```javascript
                   // main.js - Entry point
                   import { Navigation } from './modules/navigation.js';
                   import { FormValidator } from './modules/form-validator.js';
                   import { Modal } from './modules/modal.js';
                   
                   document.addEventListener('DOMContentLoaded', () => {
                       // Initialize navigation
                       Navigation.init();
                       
                       // Initialize form validation
                       document.querySelectorAll('form[data-validate]').forEach(form => {
                           FormValidator.init(form);
                       });
                       
                       // Initialize modals
                       document.querySelectorAll('[data-modal]').forEach(trigger => {
                           Modal.init(trigger);
                       });
                   });
                   
                   // modules/form-validator.js
                   export const FormValidator = {
                       init(form) {
                           form.setAttribute('novalidate', '');
                           form.addEventListener('submit', this.handleSubmit.bind(this));
                           
                           form.querySelectorAll('input, select, textarea').forEach(input => {
                               input.addEventListener('blur', () => this.validateField(input));
                               input.addEventListener('input', () => this.clearError(input));
                           });
                       },
                       
                       handleSubmit(e) {
                           const form = e.target;
                           let isValid = true;
                           
                           form.querySelectorAll('[required]').forEach(input => {
                               if (!this.validateField(input)) {
                                   isValid = false;
                               }
                           });
                           
                           if (!isValid) {
                               e.preventDefault();
                               const firstError = form.querySelector('[aria-invalid="true"]');
                               firstError?.focus();
                           }
                       },
                       
                       validateField(input) {
                           const errorEl = document.getElementById(`${input.id}-error`);
                           
                           if (!input.validity.valid) {
                               input.setAttribute('aria-invalid', 'true');
                               if (errorEl) {
                                   errorEl.textContent = this.getErrorMessage(input);
                                   errorEl.hidden = false;
                               }
                               return false;
                           }
                           
                           this.clearError(input);
                           return true;
                       },
                       
                       clearError(input) {
                           const errorEl = document.getElementById(`${input.id}-error`);
                           input.setAttribute('aria-invalid', 'false');
                           if (errorEl) {
                               errorEl.hidden = true;
                           }
                       },
                       
                       getErrorMessage(input) {
                           const label = input.labels?.[0]?.textContent?.replace('*', '').trim() || 'This field';
                           
                           if (input.validity.valueMissing) {
                               return `${label} is required`;
                           }
                           if (input.validity.typeMismatch) {
                               return `Please enter a valid ${input.type}`;
                           }
                           if (input.validity.tooShort) {
                               return `${label} must be at least ${input.minLength} characters`;
                           }
                           return input.validationMessage;
                       }
                   };
                   ```""",
            expected_output="""\
                Complete frontend implementation including:
                - Semantic HTML with proper landmarks
                - Accessible forms with validation
                - CSS with custom properties and BEM
                - JavaScript modules with event handling
                - Skip link and focus management
                - Responsive design""",
        )
    
    def frontend_testing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_testing_task(
            agent=agent,
            context=context,
            description="""\
                Create comprehensive frontend tests for accessibility and functionality.
                
                **TESTING REQUIREMENTS:**
                
                1. **Accessibility Audit**
                   ```
                   Automated Testing:
                   □ Run axe DevTools - 0 violations
                   □ Run Lighthouse Accessibility - Score 90+
                   □ Run Pa11y CLI - 0 errors
                   □ HTML validation - No errors
                   
                   Manual Testing:
                   □ Keyboard-only navigation
                   □ Screen reader testing (VoiceOver/NVDA)
                   □ Color contrast verification
                   □ 200% zoom functionality
                   □ Reduced motion preference
                   ```
                
                2. **Keyboard Navigation Test Script**
                   ```
                   1. Load page
                   2. Press Tab - Focus should be on skip link
                   3. Press Enter - Focus should move to main content
                   4. Press Tab - Navigate through all interactive elements
                   5. Verify focus indicator is visible on each element
                   6. Open modal - Focus trapped inside
                   7. Press Escape - Modal closes, focus returns
                   8. Complete form using only keyboard
                   9. Submit form - Error messages announced
                   ```
                
                3. **JavaScript Unit Tests**
                   ```javascript
                   // form-validator.test.js
                   import { FormValidator } from './form-validator.js';
                   
                   describe('FormValidator', () => {
                       let form, input, errorEl;
                       
                       beforeEach(() => {
                           document.body.innerHTML = `
                               <form data-validate>
                                   <label for="email">Email</label>
                                   <input type="email" id="email" required>
                                   <span id="email-error" hidden></span>
                                   <button type="submit">Submit</button>
                               </form>
                           `;
                           form = document.querySelector('form');
                           input = document.querySelector('#email');
                           errorEl = document.querySelector('#email-error');
                           FormValidator.init(form);
                       });
                       
                       test('adds novalidate attribute', () => {
                           expect(form.hasAttribute('novalidate')).toBe(true);
                       });
                       
                       test('validates required field on blur', () => {
                           input.dispatchEvent(new Event('blur'));
                           
                           expect(input.getAttribute('aria-invalid')).toBe('true');
                           expect(errorEl.hidden).toBe(false);
                           expect(errorEl.textContent).toContain('required');
                       });
                       
                       test('validates email format', () => {
                           input.value = 'invalid';
                           input.dispatchEvent(new Event('blur'));
                           
                           expect(input.getAttribute('aria-invalid')).toBe('true');
                           expect(errorEl.textContent).toContain('valid email');
                       });
                       
                       test('clears error on valid input', () => {
                           input.value = 'test@example.com';
                           input.dispatchEvent(new Event('blur'));
                           
                           expect(input.getAttribute('aria-invalid')).toBe('false');
                           expect(errorEl.hidden).toBe(true);
                       });
                       
                       test('prevents submit with invalid form', () => {
                           const submitEvent = new Event('submit', { cancelable: true });
                           form.dispatchEvent(submitEvent);
                           
                           expect(submitEvent.defaultPrevented).toBe(true);
                       });
                       
                       test('allows submit with valid form', () => {
                           input.value = 'test@example.com';
                           const submitEvent = new Event('submit', { cancelable: true });
                           form.dispatchEvent(submitEvent);
                           
                           expect(submitEvent.defaultPrevented).toBe(false);
                       });
                   });
                   ```
                
                4. **Cross-Browser Test Matrix**
                   ```
                   | Browser        | Version | OS      | Status |
                   |----------------|---------|---------|--------|
                   | Chrome         | Latest  | Windows | □      |
                   | Chrome         | Latest  | macOS   | □      |
                   | Firefox        | Latest  | Windows | □      |
                   | Firefox        | Latest  | macOS   | □      |
                   | Safari         | Latest  | macOS   | □      |
                   | Edge           | Latest  | Windows | □      |
                   | Chrome Mobile  | Latest  | Android | □      |
                   | Safari Mobile  | Latest  | iOS     | □      |
                   ```
                
                5. **Performance Test**
                   ```javascript
                   // lighthouse-config.js
                   module.exports = {
                       extends: 'lighthouse:default',
                       settings: {
                           onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
                       },
                       assertions: {
                           'categories:performance': ['error', { minScore: 0.9 }],
                           'categories:accessibility': ['error', { minScore: 0.95 }],
                           'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
                           'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
                       }
                   };
                   ```""",
            expected_output="""\
                Complete frontend test suite including:
                - Accessibility audit results (axe, Lighthouse)
                - Keyboard navigation test script
                - JavaScript unit tests with assertions
                - Cross-browser test matrix
                - Performance test configuration
                - Screen reader test notes""",
        )
    
    def frontend_reviewing_task(self, agent: Agent, context: List[Task]) -> Task:
        return self.create_review_task(
            agent=agent,
            context=context,
            description="""\
                Review frontend implementation for production readiness.
                
                **REVIEW CHECKLIST:**
                
                1. **HTML Quality**
                   □ Valid HTML (W3C passes)
                   □ DOCTYPE declared
                   □ lang attribute on html
                   □ Proper heading hierarchy
                   □ Semantic elements used
                   □ All images have alt
                   □ Forms have labels
                   □ Skip link present
                
                2. **Accessibility (WCAG 2.1 AA)**
                   □ Color contrast 4.5:1+
                   □ Focus indicators visible
                   □ Keyboard navigation works
                   □ ARIA used correctly
                   □ Error messages in role="alert"
                   □ No keyboard traps
                   □ Works at 200% zoom
                   □ Reduced motion respected
                
                3. **Performance**
                   □ LCP < 2.5s
                   □ FID < 100ms
                   □ CLS < 0.1
                   □ Images optimized
                   □ CSS/JS minified
                   □ Critical CSS inlined
                   □ No render-blocking
                
                4. **CSS Quality**
                   □ Custom properties used
                   □ BEM naming convention
                   □ No !important abuse
                   □ Mobile-first responsive
                   □ Dark mode support
                   □ No layout shifts
                
                5. **JavaScript Quality**
                   □ ES6+ syntax
                   □ No global variables
                   □ Event delegation
                   □ Error handling
                   □ Graceful degradation
                   □ No memory leaks
                
                6. **Security**
                   □ No inline handlers
                   □ No eval()
                   □ External scripts trusted
                   □ User input sanitized
                
                7. **SEO**
                   □ Title tag present
                   □ Meta description
                   □ Canonical URL
                   □ Open Graph tags
                   □ Structured data
                
                **PROVIDE:**
                - Accessibility audit results
                - Performance metrics
                - Code quality issues
                - Browser compatibility notes
                - Deployment checklist""",
            expected_output="""\
                Comprehensive review report including:
                - WCAG 2.1 AA compliance status
                - Core Web Vitals scores
                - Code quality assessment
                - Browser compatibility status
                - SEO readiness
                - Instructions to view the page""",
        )
