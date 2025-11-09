/**
 * HTMX Configuration & Enhancements
 * Custom behaviors for a smooth user experience
 */

document.addEventListener('DOMContentLoaded', function() {
  
  // Configure HTMX globally
  if (typeof htmx !== 'undefined') {
    
    // Show progress bar for slow requests
    htmx.on('htmx:beforeRequest', function(evt) {
      const progressBar = document.createElement('div');
      progressBar.className = 'htmx-request-progress';
      progressBar.id = 'htmx-progress';
      document.body.appendChild(progressBar);
      
      // Remove after a short delay if request completes quickly
      setTimeout(() => {
        const bar = document.getElementById('htmx-progress');
        if (bar) bar.remove();
      }, 1000);
    });
    
    // Remove progress bar when complete
    htmx.on('htmx:afterRequest', function(evt) {
      const progressBar = document.getElementById('htmx-progress');
      if (progressBar) {
        setTimeout(() => progressBar.remove(), 200);
      }
    });
    
    // Log errors for debugging (remove in production)
    htmx.on('htmx:responseError', function(evt) {
      console.error('HTMX Error:', evt.detail);
    });
    
    // Add fade-in animation to swapped content
    htmx.on('htmx:afterSwap', function(evt) {
      evt.detail.target.classList.add('fade-in');
    });
  }
  
});

/**
 * Alpine.js Components
 * Lightweight interactivity
 */

// Favorite toggle component
function favoriteToggle() {
  return {
    isFavorite: false,
    loading: false,
    
    toggle() {
      this.loading = true;
      this.isFavorite = !this.isFavorite;
      
      // Simulate API call
      setTimeout(() => {
        this.loading = false;
      }, 500);
    }
  }
}

// Search filter state
function searchFilter() {
  return {
    query: '',
    filters: {
      city: '',
      minAge: '',
      maxAge: '',
      gender: ''
    },
    resultsCount: 0,
    
    updateResults() {
      // This will be triggered by HTMX
      console.log('Filters updated:', this.filters);
    },
    
    clearFilters() {
      this.query = '';
      this.filters = {
        city: '',
        minAge: '',
        maxAge: '',
        gender: ''
      };
    }
  }
}

// Message notification counter
function notificationCounter() {
  return {
    count: 0,
    
    init() {
      this.fetchCount();
      // Poll every 30 seconds for new messages
      setInterval(() => this.fetchCount(), 30000);
    },
    
    fetchCount() {
      // This would call your Django endpoint
      // For now, just a placeholder
      fetch('/api/unread-count/')
        .then(r => r.json())
        .then(data => {
          this.count = data.count || 0;
        })
        .catch(() => {
          // Silently fail
        });
    }
  }
}

// Expose to global scope for Alpine
window.favoriteToggle = favoriteToggle;
window.searchFilter = searchFilter;
window.notificationCounter = notificationCounter;

