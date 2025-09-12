// Accessibility checker utility for CustomerMind IQ
class AccessibilityChecker {
  constructor() {
    this.issues = [];
    this.isChecking = false;
  }

  // Main function to check all accessibility issues
  checkAccessibility() {
    this.issues = [];
    this.isChecking = true;

    const checks = [
      this.checkMissingAltText(),
      this.checkMissingLabels(),
      this.checkColorContrast(),
      this.checkKeyboardNavigation(),
      this.checkHeadingStructure(),
      this.checkFocusableElements(),
      this.checkAriaAttributes()
    ];

    Promise.all(checks).then(() => {
      this.isChecking = false;
      this.reportResults();
    });

    return this.issues;
  }

  // Check for images missing alt text
  checkMissingAltText() {
    return new Promise((resolve) => {
      const images = document.querySelectorAll('img');
      const missingAlt = [];

      images.forEach((img, index) => {
        const alt = img.getAttribute('alt');
        const src = img.getAttribute('src') || 'unknown';
        
        // Check for missing, empty, or generic alt text
        if (!alt) {
          missingAlt.push({
            element: img,
            issue: 'Missing alt attribute',
            src: src,
            index: index
          });
        } else if (alt.trim() === '') {
          // Empty alt is OK for decorative images, but flag for review
          missingAlt.push({
            element: img,
            issue: 'Empty alt attribute (decorative image?)',
            src: src,
            index: index,
            severity: 'low'
          });
        } else if (this.isGenericAltText(alt)) {
          missingAlt.push({
            element: img,
            issue: 'Generic alt text detected',
            src: src,
            alt: alt,
            index: index,
            severity: 'medium'
          });
        }
      });

      if (missingAlt.length > 0) {
        this.issues.push({
          type: 'alt-text',
          severity: 'high',
          count: missingAlt.length,
          details: missingAlt,
          message: `Found ${missingAlt.length} images with alt text issues`
        });
      }

      resolve(missingAlt);
    });
  }

  // Check for generic/poor alt text
  isGenericAltText(alt) {
    const genericTerms = [
      'image', 'picture', 'photo', 'img', 'graphic', 'logo',
      'icon', 'button', 'link', 'untitled', 'unnamed'
    ];
    
    const altLower = alt.toLowerCase().trim();
    return genericTerms.some(term => altLower === term || altLower.includes(`${term}.`));
  }

  // Check for form elements missing labels
  checkMissingLabels() {
    return new Promise((resolve) => {
      const formElements = document.querySelectorAll('input, select, textarea');
      const missingLabels = [];

      formElements.forEach((element, index) => {
        const id = element.id;
        const ariaLabel = element.getAttribute('aria-label');
        const ariaLabelledBy = element.getAttribute('aria-labelledby');
        const placeholder = element.getAttribute('placeholder');
        const type = element.type;

        // Skip hidden inputs and buttons (they have different rules)
        if (type === 'hidden' || type === 'button' || type === 'submit' || type === 'reset') {
          return;
        }

        let hasLabel = false;
        
        // Check for associated label
        if (id) {
          const label = document.querySelector(`label[for="${id}"]`);
          if (label) hasLabel = true;
        }

        // Check for aria-label or aria-labelledby
        if (ariaLabel || ariaLabelledBy) hasLabel = true;

        // Check if wrapped in label
        const parentLabel = element.closest('label');
        if (parentLabel) hasLabel = true;

        if (!hasLabel) {
          missingLabels.push({
            element: element,
            issue: 'Missing label',
            type: type,
            placeholder: placeholder,
            index: index
          });
        }
      });

      if (missingLabels.length > 0) {
        this.issues.push({
          type: 'form-labels',
          severity: 'high',
          count: missingLabels.length,
          details: missingLabels,
          message: `Found ${missingLabels.length} form elements without proper labels`
        });
      }

      resolve(missingLabels);
    });
  }

  // Basic color contrast check (simplified)
  checkColorContrast() {
    return new Promise((resolve) => {
      const contrastIssues = [];
      const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, a, button, label');

      textElements.forEach((element, index) => {
        const styles = window.getComputedStyle(element);
        const color = styles.color;
        const backgroundColor = styles.backgroundColor;
        const fontSize = parseFloat(styles.fontSize);

        // Skip if transparent or no background
        if (backgroundColor === 'rgba(0, 0, 0, 0)' || backgroundColor === 'transparent') {
          return;
        }

        // This is a simplified check - in reality, you'd need a more sophisticated contrast calculation
        const hasGoodContrast = this.checkContrastRatio(color, backgroundColor, fontSize);
        
        if (!hasGoodContrast) {
          contrastIssues.push({
            element: element,
            issue: 'Potential contrast issue',
            color: color,
            backgroundColor: backgroundColor,
            fontSize: fontSize,
            index: index
          });
        }
      });

      if (contrastIssues.length > 0) {
        this.issues.push({
          type: 'color-contrast',
          severity: 'medium',
          count: contrastIssues.length,
          details: contrastIssues,
          message: `Found ${contrastIssues.length} elements with potential contrast issues`
        });
      }

      resolve(contrastIssues);
    });
  }

  // Simplified contrast ratio check
  checkContrastRatio(color, backgroundColor, fontSize) {
    // This is a very basic implementation
    // In a real application, you'd use a proper color contrast library
    try {
      const colorLuminance = this.getLuminance(color);
      const bgLuminance = this.getLuminance(backgroundColor);
      
      const contrast = (Math.max(colorLuminance, bgLuminance) + 0.05) / 
                      (Math.min(colorLuminance, bgLuminance) + 0.05);
      
      // WCAG AA standards: 4.5:1 for normal text, 3:1 for large text
      const requiredRatio = fontSize >= 18 || fontSize >= 14 ? 3.0 : 4.5;
      
      return contrast >= requiredRatio;
    } catch (error) {
      return true; // Assume OK if we can't calculate
    }
  }

  // Get relative luminance (simplified)
  getLuminance(color) {
    // Very basic implementation - would need proper RGB parsing
    if (color.includes('rgb')) {
      const matches = color.match(/\d+/g);
      if (matches && matches.length >= 3) {
        const [r, g, b] = matches.map(n => parseInt(n) / 255);
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
      }
    }
    return 0.5; // Default middle value
  }

  // Check keyboard navigation
  checkKeyboardNavigation() {
    return new Promise((resolve) => {
      const focusableElements = document.querySelectorAll(
        'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      
      const keyboardIssues = [];

      focusableElements.forEach((element, index) => {
        const tabIndex = element.getAttribute('tabindex');
        const isVisible = this.isElementVisible(element);

        // Check for positive tabindex (not recommended)
        if (tabIndex && parseInt(tabIndex) > 0) {
          keyboardIssues.push({
            element: element,
            issue: 'Positive tabindex detected (not recommended)',
            tabIndex: tabIndex,
            index: index
          });
        }

        // Check if focusable element is hidden
        if (!isVisible && tabIndex !== '-1') {
          keyboardIssues.push({
            element: element,
            issue: 'Focusable element is hidden',
            index: index
          });
        }
      });

      if (keyboardIssues.length > 0) {
        this.issues.push({
          type: 'keyboard-navigation',
          severity: 'medium',
          count: keyboardIssues.length,
          details: keyboardIssues,
          message: `Found ${keyboardIssues.length} keyboard navigation issues`
        });
      }

      resolve(keyboardIssues);
    });
  }

  // Check heading structure
  checkHeadingStructure() {
    return new Promise((resolve) => {
      const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
      const headingIssues = [];
      let lastLevel = 0;

      headings.forEach((heading, index) => {
        const level = parseInt(heading.tagName.substring(1));
        const text = heading.textContent.trim();

        // Check for empty headings
        if (!text) {
          headingIssues.push({
            element: heading,
            issue: 'Empty heading',
            level: level,
            index: index
          });
        }

        // Check for skipped heading levels
        if (level > lastLevel + 1 && lastLevel > 0) {
          headingIssues.push({
            element: heading,
            issue: `Heading level skipped (jumped from h${lastLevel} to h${level})`,
            level: level,
            index: index
          });
        }

        lastLevel = level;
      });

      // Check for multiple h1s
      const h1Count = document.querySelectorAll('h1').length;
      if (h1Count > 1) {
        headingIssues.push({
          issue: `Multiple h1 elements found (${h1Count})`,
          severity: 'medium'
        });
      }

      if (headingIssues.length > 0) {
        this.issues.push({
          type: 'heading-structure',
          severity: 'medium',
          count: headingIssues.length,
          details: headingIssues,
          message: `Found ${headingIssues.length} heading structure issues`
        });
      }

      resolve(headingIssues);
    });
  }

  // Check focusable elements have visible focus indicators
  checkFocusableElements() {
    return new Promise((resolve) => {
      const focusableElements = document.querySelectorAll(
        'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      
      const focusIssues = [];

      focusableElements.forEach((element, index) => {
        // This is a basic check - in reality, you'd need to simulate focus
        const styles = window.getComputedStyle(element, ':focus');
        const outline = styles.outline;
        const outlineWidth = styles.outlineWidth;

        if (outline === 'none' || outlineWidth === '0px') {
          focusIssues.push({
            element: element,
            issue: 'No visible focus indicator',
            index: index
          });
        }
      });

      if (focusIssues.length > 0) {
        this.issues.push({
          type: 'focus-indicators',
          severity: 'medium',
          count: focusIssues.length,
          details: focusIssues,
          message: `Found ${focusIssues.length} elements without visible focus indicators`
        });
      }

      resolve(focusIssues);
    });
  }

  // Check ARIA attributes
  checkAriaAttributes() {
    return new Promise((resolve) => {
      const elementsWithAria = document.querySelectorAll('[aria-label], [aria-labelledby], [aria-describedby], [role]');
      const ariaIssues = [];

      elementsWithAria.forEach((element, index) => {
        const ariaLabelledby = element.getAttribute('aria-labelledby');
        const ariaDescribedby = element.getAttribute('aria-describedby');
        const role = element.getAttribute('role');

        // Check if aria-labelledby points to existing element
        if (ariaLabelledby) {
          const referencedElement = document.getElementById(ariaLabelledby);
          if (!referencedElement) {
            ariaIssues.push({
              element: element,
              issue: `aria-labelledby points to non-existent element: ${ariaLabelledby}`,
              index: index
            });
          }
        }

        // Check if aria-describedby points to existing element
        if (ariaDescribedby) {
          const referencedElement = document.getElementById(ariaDescribedby);
          if (!referencedElement) {
            ariaIssues.push({
              element: element,
              issue: `aria-describedby points to non-existent element: ${ariaDescribedby}`,
              index: index
            });
          }
        }

        // Check for invalid roles (basic check)
        if (role && !this.isValidAriaRole(role)) {
          ariaIssues.push({
            element: element,
            issue: `Invalid ARIA role: ${role}`,
            index: index
          });
        }
      });

      if (ariaIssues.length > 0) {
        this.issues.push({
          type: 'aria-attributes',
          severity: 'high',
          count: ariaIssues.length,
          details: ariaIssues,
          message: `Found ${ariaIssues.length} ARIA attribute issues`
        });
      }

      resolve(ariaIssues);
    });
  }

  // Check if element is visible
  isElementVisible(element) {
    const rect = element.getBoundingClientRect();
    const styles = window.getComputedStyle(element);
    
    return (
      rect.width > 0 &&
      rect.height > 0 &&
      styles.visibility !== 'hidden' &&
      styles.display !== 'none' &&
      styles.opacity !== '0'
    );
  }

  // Basic ARIA role validation
  isValidAriaRole(role) {
    const validRoles = [
      'alert', 'alertdialog', 'application', 'article', 'banner', 'button',
      'cell', 'checkbox', 'columnheader', 'combobox', 'complementary',
      'contentinfo', 'definition', 'dialog', 'directory', 'document',
      'feed', 'figure', 'form', 'grid', 'gridcell', 'group', 'heading',
      'img', 'link', 'list', 'listbox', 'listitem', 'log', 'main',
      'marquee', 'math', 'menu', 'menubar', 'menuitem', 'menuitemcheckbox',
      'menuitemradio', 'navigation', 'none', 'note', 'option', 'presentation',
      'progressbar', 'radio', 'radiogroup', 'region', 'row', 'rowgroup',
      'rowheader', 'scrollbar', 'search', 'searchbox', 'separator',
      'slider', 'spinbutton', 'status', 'switch', 'tab', 'table',
      'tablist', 'tabpanel', 'term', 'textbox', 'timer', 'toolbar',
      'tooltip', 'tree', 'treegrid', 'treeitem'
    ];
    
    return validRoles.includes(role.toLowerCase());
  }

  // Report results
  reportResults() {
    const totalIssues = this.issues.reduce((sum, issue) => sum + issue.count, 0);
    
    if (process.env.NODE_ENV === 'development') {
      console.group('🔍 Accessibility Check Results');
      console.log(`Found ${totalIssues} total accessibility issues across ${this.issues.length} categories`);
      
      this.issues.forEach(issue => {
        const emoji = issue.severity === 'high' ? '🚨' : issue.severity === 'medium' ? '⚠️' : 'ℹ️';
        console.log(`${emoji} ${issue.message}`);
      });
      
      console.groupEnd();
    }

    // Store results globally for debugging
    window.accessibilityResults = {
      totalIssues,
      issues: this.issues,
      timestamp: new Date().toISOString()
    };

    return {
      totalIssues,
      issues: this.issues
    };
  }

  // Get summary of issues by severity
  getSummary() {
    const summary = {
      high: 0,
      medium: 0,
      low: 0,
      total: 0
    };

    this.issues.forEach(issue => {
      summary[issue.severity]++;
      summary.total += issue.count;
    });

    return summary;
  }

  // Get detailed report
  getDetailedReport() {
    return {
      summary: this.getSummary(),
      issues: this.issues,
      timestamp: new Date().toISOString(),
      url: window.location.href
    };
  }
}

// Create singleton instance
const accessibilityChecker = new AccessibilityChecker();

// Export functions
export const checkAccessibility = () => {
  return accessibilityChecker.checkAccessibility();
};

export const getAccessibilityResults = () => {
  return accessibilityChecker.getDetailedReport();
};

// Auto-run in development
if (process.env.NODE_ENV === 'development') {
  // Run accessibility check after page loads
  window.addEventListener('load', () => {
    setTimeout(() => {
      checkAccessibility();
    }, 2000); // Wait 2 seconds for dynamic content to load
  });
}

export default accessibilityChecker;