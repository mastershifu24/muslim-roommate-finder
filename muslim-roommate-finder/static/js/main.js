document.addEventListener("DOMContentLoaded", () => {
    // Debug: Check if Bootstrap is loaded
    console.log('Bootstrap loaded:', typeof bootstrap !== 'undefined');
    console.log('Bootstrap Collapse:', typeof bootstrap !== 'undefined' && typeof bootstrap.Collapse !== 'undefined');
    
    // Delete button confirmation
    const deleteButtons = document.querySelectorAll(".delete-btn");
    
    deleteButtons.forEach(btn => {
      btn.addEventListener("click", (e) => {
        if (!confirm("Are you sure you want to delete this item?")) {
          e.preventDefault();
        }
      });
    });

    // Ensure Bootstrap collapse functionality works
    const collapseTriggers = document.querySelectorAll('[data-bs-toggle="collapse"]');
    
    collapseTriggers.forEach(trigger => {
      trigger.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('data-bs-target');
        const target = document.querySelector(targetId);
        
        if (target) {
          const bsCollapse = new bootstrap.Collapse(target, {
            toggle: true
          });
        }
      });
    });

    // Fix advanced filters dropdown with fallback
    const advancedFilterBtn = document.querySelector('[data-bs-target="#advancedFilters"]');
    if (advancedFilterBtn) {
      advancedFilterBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.getElementById('advancedFilters');
        
        if (target) {
          // Try Bootstrap collapse first
          if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
            const bsCollapse = new bootstrap.Collapse(target, {
              toggle: true
            });
          } else {
            // Fallback: manual toggle
            if (target.classList.contains('show')) {
              target.classList.remove('show');
              target.style.display = 'none';
            } else {
              target.classList.add('show');
              target.style.display = 'block';
            }
          }
          
          // Rotate the chevron icon
          const chevron = this.querySelector('.fa-chevron-down');
          if (chevron) {
            const isOpen = target.classList.contains('show');
            chevron.style.transform = isOpen ? 'rotate(180deg)' : 'rotate(0deg)';
          }
        }
      });
    }

    // Handle chevron rotation for all collapse triggers
    document.querySelectorAll('.collapse').forEach(collapse => {
      collapse.addEventListener('show.bs.collapse', function() {
        const trigger = document.querySelector(`[data-bs-target="#${this.id}"]`);
        if (trigger) {
          const chevron = trigger.querySelector('.fa-chevron-down');
          if (chevron) {
            chevron.style.transform = 'rotate(180deg)';
          }
        }
      });
      
      collapse.addEventListener('hide.bs.collapse', function() {
        const trigger = document.querySelector(`[data-bs-target="#${this.id}"]`);
        if (trigger) {
          const chevron = trigger.querySelector('.fa-chevron-down');
          if (chevron) {
            chevron.style.transform = 'rotate(0deg)';
          }
        }
      });
    });
  });
  