// ── Sidebar Toggle (Mobile) ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const toggle  = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');

  if (toggle && sidebar) {
    toggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      overlay && overlay.classList.toggle('show');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar && sidebar.classList.remove('open');
      overlay.classList.remove('show');
    });
  }

  // ── Active nav link ────────────────────────────────────────────────────────
  const navItems = document.querySelectorAll('.nav-item');
  const path = window.location.pathname;
  navItems.forEach(item => {
    if (item.getAttribute('href') === path) {
      item.classList.add('active');
    }
  });

  // ── Auto-dismiss alerts ────────────────────────────────────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

  // ── Status Update Form: confirm dialog ────────────────────────────────────
  const statusForm = document.getElementById('statusUpdateForm');
  if (statusForm) {
    statusForm.addEventListener('submit', function (e) {
      const status = document.getElementById('statusSelect').value;
      if (!confirm(`Update complaint status to "${status}"?`)) {
        e.preventDefault();
      }
    });
  }

  // ── Complaint form: simple validation ─────────────────────────────────────
  const complaintForm = document.getElementById('complaintForm');
  if (complaintForm) {
    complaintForm.addEventListener('submit', function (e) {
      const addr = document.getElementById('id_address');
      const desc = document.getElementById('id_description');
      if (!addr.value.trim() || !desc.value.trim()) {
        e.preventDefault();
        showToast('Please fill in all required fields.', 'error');
      }
    });
  }

  // ── Image preview ─────────────────────────────────────────────────────────
  const imgInput = document.getElementById('id_image');
  if (imgInput) {
    imgInput.addEventListener('change', function () {
      const file = this.files[0];
      const preview = document.getElementById('imgPreview');
      if (file && preview) {
        const reader = new FileReader();
        reader.onload = e => {
          preview.src = e.target.result;
          preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // ── Animate stat numbers ──────────────────────────────────────────────────
  document.querySelectorAll('.stat-num').forEach(el => {
    const target = parseInt(el.textContent);
    if (isNaN(target)) return;
    let current = 0;
    const step = Math.max(1, Math.floor(target / 30));
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 30);
  });
});

function showToast(msg, type = 'info') {
  const wrap = document.querySelector('.messages-wrap') || document.body;
  const div = document.createElement('div');
  div.className = `alert alert-${type}`;
  div.textContent = msg;
  wrap.prepend(div);
  setTimeout(() => div.remove(), 4000);
}
