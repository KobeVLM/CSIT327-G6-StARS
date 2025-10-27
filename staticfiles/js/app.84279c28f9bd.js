// ========================================
// JAVASCRIPT EXTRACTIONS FOR DJANGO
// ========================================
// Extract these interactive features from React to vanilla JS

// ----------------------------------------
// 1. DARK MODE TOGGLE (Settings page)
// ----------------------------------------
// From: /components/pages/Settings.tsx
// Usage: Add to settings.html

function initDarkMode() {
  const darkModeToggle = document.getElementById('darkModeToggle');
  const htmlElement = document.documentElement;
  
  // Load saved preference
  const savedDarkMode = localStorage.getItem('darkMode') === 'true';
  if (savedDarkMode) {
    htmlElement.classList.add('dark');
    if (darkModeToggle) darkModeToggle.checked = true;
  }
  
  // Toggle dark mode
  if (darkModeToggle) {
    darkModeToggle.addEventListener('change', function() {
      const isDark = this.checked;
      localStorage.setItem('darkMode', isDark);
      
      if (isDark) {
        htmlElement.classList.add('dark');
      } else {
        htmlElement.classList.remove('dark');
      }
    });
  }
}

// ----------------------------------------
// 2. PROFILE DROPDOWN (AppHeader)
// ----------------------------------------
// From: /components/AppHeader.tsx
// Usage: Add to base.html

function initProfileDropdown() {
  const dropdownButton = document.getElementById('profileDropdown');
  const dropdownMenu = document.getElementById('profileDropdownMenu');
  const dropdownOverlay = document.getElementById('dropdownOverlay');
  
  if (dropdownButton && dropdownMenu && dropdownOverlay) {
    // Open dropdown
    dropdownButton.addEventListener('click', function(e) {
      e.stopPropagation();
      dropdownMenu.classList.toggle('hidden');
      dropdownOverlay.classList.toggle('hidden');
    });
    
    // Close dropdown when clicking overlay
    dropdownOverlay.addEventListener('click', function() {
      dropdownMenu.classList.add('hidden');
      dropdownOverlay.classList.add('hidden');
    });
    
    // Close dropdown when clicking menu items
    const menuItems = dropdownMenu.querySelectorAll('a, button');
    menuItems.forEach(item => {
      item.addEventListener('click', function() {
        dropdownMenu.classList.add('hidden');
        dropdownOverlay.classList.add('hidden');
      });
    });
  }
}

// ----------------------------------------
// 3. INLINE PROFILE EDIT (Profile page)
// ----------------------------------------
// From: /components/pages/Profile.tsx
// Usage: Add to profile.html

function initInlineProfileEdit() {
  const editButton = document.getElementById('editProfileBtn');
  const saveButton = document.getElementById('saveProfileBtn');
  const cancelButton = document.getElementById('cancelProfileBtn');
  
  const bioDisplay = document.getElementById('bioDisplay');
  const bioInput = document.getElementById('bioInput');
  const locationDisplay = document.getElementById('locationDisplay');
  const locationInput = document.getElementById('locationInput');
  const websiteDisplay = document.getElementById('websiteDisplay');
  const websiteInput = document.getElementById('websiteInput');
  
  let originalBio, originalLocation, originalWebsite;
  
  // Enter edit mode
  if (editButton) {
    editButton.addEventListener('click', function() {
      // Store original values
      originalBio = bioDisplay.textContent;
      originalLocation = locationDisplay.textContent;
      originalWebsite = websiteDisplay.textContent;
      
      // Hide displays, show inputs
      bioDisplay.classList.add('hidden');
      bioInput.classList.remove('hidden');
      bioInput.value = originalBio;
      
      locationDisplay.classList.add('hidden');
      locationInput.classList.remove('hidden');
      locationInput.value = originalLocation;
      
      websiteDisplay.classList.add('hidden');
      websiteInput.classList.remove('hidden');
      websiteInput.value = originalWebsite;
      
      // Toggle buttons
      editButton.classList.add('hidden');
      saveButton.classList.remove('hidden');
      cancelButton.classList.remove('hidden');
    });
  }
  
  // Save changes
  if (saveButton) {
    saveButton.addEventListener('click', function() {
      // Update displays with new values
      bioDisplay.textContent = bioInput.value;
      locationDisplay.textContent = locationInput.value;
      websiteDisplay.textContent = websiteInput.value;
      
      // Show displays, hide inputs
      bioDisplay.classList.remove('hidden');
      bioInput.classList.add('hidden');
      locationDisplay.classList.remove('hidden');
      locationInput.classList.add('hidden');
      websiteDisplay.classList.remove('hidden');
      websiteInput.classList.add('hidden');
      
      // Toggle buttons
      editButton.classList.remove('hidden');
      saveButton.classList.add('hidden');
      cancelButton.classList.add('hidden');
      
      // TODO: Send AJAX request to Django backend to save
      // fetch('/profile/update/', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     bio: bioInput.value,
      //     location: locationInput.value,
      //     website: websiteInput.value
      //   })
      // });
    });
  }
  
  // Cancel changes
  if (cancelButton) {
    cancelButton.addEventListener('click', function() {
      // Restore original values
      bioInput.value = originalBio;
      locationInput.value = originalLocation;
      websiteInput.value = originalWebsite;
      
      // Show displays, hide inputs
      bioDisplay.classList.remove('hidden');
      bioInput.classList.add('hidden');
      locationDisplay.classList.remove('hidden');
      locationInput.classList.add('hidden');
      websiteDisplay.classList.remove('hidden');
      websiteInput.classList.add('hidden');
      
      // Toggle buttons
      editButton.classList.remove('hidden');
      saveButton.classList.add('hidden');
      cancelButton.classList.add('hidden');
    });
  }
}

// ----------------------------------------
// 4. DASHBOARD SEARCH (Dashboard page)
// ----------------------------------------
// From: /components/pages/Dashboard.tsx
// Usage: Add to dashboard.html

function initDashboardSearch() {
  const searchInput = document.getElementById('dashboardSearch');
  const searchResults = document.getElementById('searchResults');
  const searchOverlay = document.getElementById('searchOverlay');
  const clearSearchBtn = document.getElementById('clearSearch');
  
  if (!searchInput || !searchResults) return;
  
  // Show results on focus
  searchInput.addEventListener('focus', function() {
    if (this.value.trim()) {
      searchResults.classList.remove('hidden');
      searchOverlay.classList.remove('hidden');
    }
  });
  
  // Search on input
  searchInput.addEventListener('input', function() {
    const query = this.value.trim();
    
    // Show/hide clear button
    if (clearSearchBtn) {
      clearSearchBtn.classList.toggle('hidden', !query);
    }
    
    if (!query) {
      searchResults.classList.add('hidden');
      searchOverlay.classList.add('hidden');
      return;
    }
    
    // Show results
    searchResults.classList.remove('hidden');
    searchOverlay.classList.remove('hidden');
    
    // TODO: Perform search via AJAX
    // fetch(`/search/?q=${encodeURIComponent(query)}`)
    //   .then(response => response.json())
    //   .then(data => {
    //     // Update searchResults innerHTML with data
    //   });
  });
  
  // Clear search
  if (clearSearchBtn) {
    clearSearchBtn.addEventListener('click', function() {
      searchInput.value = '';
      searchResults.classList.add('hidden');
      searchOverlay.classList.add('hidden');
      clearSearchBtn.classList.add('hidden');
    });
  }
  
  // Close search results on overlay click
  if (searchOverlay) {
    searchOverlay.addEventListener('click', function() {
      searchResults.classList.add('hidden');
      searchOverlay.classList.add('hidden');
    });
  }
}

// ----------------------------------------
// 5. SETTINGS SAVE NOTIFICATION
// ----------------------------------------
// From: /components/pages/Settings.tsx
// Usage: Add to settings.html

function initSettingsForm() {
  const settingsForm = document.getElementById('settingsForm');
  const successAlert = document.getElementById('settingsSuccess');
  
  if (settingsForm) {
    settingsForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Show success message
      if (successAlert) {
        successAlert.classList.remove('hidden');
        
        // Hide after 3 seconds
        setTimeout(() => {
          successAlert.classList.add('hidden');
        }, 3000);
      }
      
      // TODO: Submit form via AJAX
      // const formData = new FormData(this);
      // fetch('/settings/update/', {
      //   method: 'POST',
      //   body: formData
      // });
    });
  }
}

// ----------------------------------------
// INITIALIZE ALL ON PAGE LOAD
// ----------------------------------------

document.addEventListener('DOMContentLoaded', function() {
  initDarkMode();
  initProfileDropdown();
  initInlineProfileEdit();
  initDashboardSearch();
  initSettingsForm();
  
  // Initialize Lucide icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
});
