/*
 * automation-center-f78c-24TaylorSmith575
 * Frontend interaction script — PROMPT-F78CD1-000076
 * Features: pagination navigation, batch operation confirmation,
 *           theme toggle trigger, notification toast simulation.
 * All API calls use mock-friendly JSON endpoints; no external deps required.
 */

// --- Utility Helpers --- //
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

const notify = (message, type = 'info') => {
  const toast = document.createElement('div');
  toast.className = `notification-toast toast-${type}`;
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 6px;
    color: white;
    font-size: 14px;
    z-index: 10000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transform: translateX(120%);
    transition: transform 0.3s ease-out;
  `;
  if (type === 'success') toast.style.background = '#4CAF50';
  if (type === 'warn') toast.style.background = '#FF9800';
  if (type === 'error') toast.style.background = '#f44336';
  if (type === 'info') toast.style.background = '#2196F3';

  document.body.appendChild(toast);
  
  // Animate in
  setTimeout(() => {
    toast.style.transform = 'translateX(0)';
  }, 10);

  // Auto-dismiss after 3s
  setTimeout(() => {
    toast.style.transform = 'translateX(120%)';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
};

// --- Pagination Navigation --- //
const initPagination = () => {
  const prevBtn = $('#pagination-prev');
  const nextBtn = $('#pagination-next');
  const pageInput = $('#page-input');
  const totalPagesSpan = $('#total-pages');

  if (!prevBtn || !nextBtn || !pageInput || !totalPagesSpan) return;

  let currentPage = parseInt(pageInput.value) || 1;
  let totalPages = parseInt(totalPagesSpan.textContent) || 1;

  const updatePageInput = () => {
    pageInput.value = Math.max(1, Math.min(currentPage, totalPages));
  };

  const loadPage = (page) => {
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    updatePageInput();

    // Simulate API fetch
    notify(`Loading tasks page ${currentPage}...`, 'info');
    
    // In real app: fetch(`/api/v1/tasks?page=${currentPage}&size=10`)
    // For demo: just simulate success
    setTimeout(() => {
      notify(`Loaded page ${currentPage} of ${totalPages}`, 'success');
    }, 400);
  };

  prevBtn.addEventListener('click', () => loadPage(currentPage - 1));
  nextBtn.addEventListener('click', () => loadPage(currentPage + 1));

  pageInput.addEventListener('change', () => {
    const target = parseInt(pageInput.value);
    if (!isNaN(target)) loadPage(target);
  });

  // Keyboard support for page input
  pageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const target = parseInt(pageInput.value);
      if (!isNaN(target)) loadPage(target);
    }
  });
};

// --- Batch Operation Confirmation --- //
const initBatchActions = () => {
  const batchUpdateBtn = $('#batch-update-btn');
  const batchDeleteBtn = $('#batch-delete-btn');

  if (batchUpdateBtn) {
    batchUpdateBtn.addEventListener('click', () => {
      const selected = Array.from($$('.task-checkbox:checked')).map(cb => cb.value);
      if (selected.length === 0) {
        notify('Please select at least one task to update.', 'warn');
        return;
      }
      if (confirm(`Are you sure you want to update ${selected.length} task(s)?`)) {
        notify(`Updating ${selected.length} task(s)...`, 'info');
        setTimeout(() => {
          notify(`${selected.length} task(s) updated successfully.`, 'success');
        }, 600);
      }
    });
  }

  if (batchDeleteBtn) {
    batchDeleteBtn.addEventListener('click', () => {
      const selected = Array.from($$('.task-checkbox:checked')).map(cb => cb.value);
      if (selected.length === 0) {
        notify('Please select at least one task to delete.', 'warn');
        return;
      }
      if (confirm(`⚠️  Warning: This will permanently delete ${selected.length} task(s).\nAre you sure?`)) {
        notify(`Deleting ${selected.length} task(s)...`, 'info');
        setTimeout(() => {
          notify(`${selected.length} task(s) deleted.`, 'success');
          // In real app: remove rows or reload
          selected.forEach(id => {
            const row = document.querySelector(`[data-task-id="${id}"]`);
            if (row) row.remove();
          });
        }, 800);
      }
    });
  }
};

// --- Theme Toggle --- //
const initThemeToggle = () => {
  const themeToggleBtn = $('#theme-toggle');
  if (!themeToggleBtn) return;

  const savedTheme = localStorage.getItem('ui-theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);

  const setTheme = (mode) => {
    document.documentElement.setAttribute('data-theme', mode);
    localStorage.setItem('ui-theme', mode);
    themeToggleBtn.textContent = mode === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
    notify(`Theme switched to ${mode}.`, 'info');
  };

  themeToggleBtn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    setTheme(current === 'light' ? 'dark' : 'light');
  });
};

// --- Notification Badge Simulation --- //
const initNotifications = () => {
  const notifBadge = $('#notification-badge');
  const notifBell = $('#notification-bell');

  if (!notifBadge || !notifBell) return;

  // Simulate unread count (mock: always 3 on load)
  let unreadCount = 3;
  notifBadge.textContent = unreadCount;
  notifBadge.style.display = unreadCount > 0 ? 'inline-flex' : 'none';

  notifBell.addEventListener('click', () => {
    if (unreadCount > 0) {
      notify(`Marking ${unreadCount} notifications as read...`, 'info');
      setTimeout(() => {
        unreadCount = 0;
        notifBadge.textContent = '';
        notifBadge.style.display = 'none';
        notify('All notifications marked as read.', 'success');
      }, 500);
    }
  });
};

// --- File Upload Simulation --- //
const initFileUpload = () => {
  const uploadInput = $('#file-upload-input');
  const uploadBtn = $('#file-upload-btn');

  if (uploadInput && uploadBtn) {
    const handleUpload = () => {
      const file = uploadInput.files[0];
      if (!file) {
        notify('Please select a file first.', 'warn');
        return;
      }

      // Basic validation
      const maxSize = 5 * 1024 * 1024; // 5MB
      const allowedTypes = ['image/jpeg', 'image/png', 'text/plain', 'application/pdf'];
      if (file.size > maxSize) {
        notify('File too large. Max size is 5MB.', 'error');
        return;
      }
      if (!allowedTypes.includes(file.type)) {
        notify('Unsupported file type. Allowed: JPG, PNG, TXT, PDF.', 'error');
        return;
      }

      notify(`Uploading \"${file.name}\"...`, 'info');
      
      // Simulate network delay
      setTimeout(() => {
        const mockId = `mock_${Date.now()}_${Math.floor(Math.random() * 1000)}`;
        notify(`✅ Uploaded! ID: ${mockId}`, 'success');
        // In real app: display preview or store ID for later use
      }, 900);
    };

    uploadBtn.addEventListener('click', handleUpload);
    uploadInput.addEventListener('change', handleUpload);
  }
};

// --- Initialize on DOM load --- //
document.addEventListener('DOMContentLoaded', () => {
  initPagination();
  initBatchActions();
  initThemeToggle();
  initNotifications();
  initFileUpload();

  // Optional: auto-focus search on load
  const searchInput = $('#search-input');
  if (searchInput) searchInput.focus();
});