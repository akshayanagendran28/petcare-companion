/**
 * Real-Time Chart.js Integration for Pet Health Weight Tracker & Analytics
 */

let petWeightChartInstance = null;
let currentSelectedRange = 'all';

/**
 * Renders or updates the interactive Weight Tracking Chart
 * @param {string} canvasId - The canvas element ID
 * @param {number|string} petId - The pet ID
 * @param {string} range - '1m' | '3m' | '6m' | '1y' | 'all'
 */
function renderPetWeightChart(canvasId, petId, range = 'all') {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === 'undefined') return;

  currentSelectedRange = range;

  // Update active state on range selector buttons
  const rangeBtns = document.querySelectorAll('.weight-range-btn');
  rangeBtns.forEach(btn => {
    if (btn.dataset.range === range) {
      btn.classList.add('btn-primary', 'text-white', 'shadow-sm');
      btn.classList.remove('btn-outline-secondary');
    } else {
      btn.classList.remove('btn-primary', 'text-white', 'shadow-sm');
      btn.classList.add('btn-outline-secondary');
    }
  });

  const loadingIndicator = document.getElementById('chart-loading-spinner');
  if (loadingIndicator) loadingIndicator.style.display = 'block';

  fetch(`/health/${petId}/weight-data/?range=${encodeURIComponent(range)}`)
    .then(res => res.json())
    .then(payload => {
      if (loadingIndicator) loadingIndicator.style.display = 'none';
      if (!payload.success || !payload.labels || payload.labels.length === 0) {
        if (!petWeightChartInstance) {
          canvas.parentElement.innerHTML = '<div class="alert alert-info text-center py-4 my-2"><i class="fa-solid fa-weight-scale fs-3 d-block mb-2 text-primary"></i>No weight logs found for this timeframe. Click <strong>+ Log Weight</strong> to add a new check-in.</div>';
        }
        return;
      }

      updateWeightDashboardStats(payload);
      drawPetWeightChart(canvas, payload);
    })
    .catch(err => {
      if (loadingIndicator) loadingIndicator.style.display = 'none';
      console.error('Error loading pet weight data:', err);
    });
}

/**
 * Updates the live summary KPI statistic cards
 */
function updateWeightDashboardStats(payload) {
  const stats = payload.stats || {};
  
  // Current weight badge
  const curEl = document.getElementById('stat-current-weight');
  if (curEl) curEl.textContent = `${stats.current_weight} kg`;

  // Header banner weight
  const headerWeightEl = document.getElementById('pet-header-weight');
  if (headerWeightEl) headerWeightEl.textContent = `${stats.current_weight} kg`;

  // Delta change
  const changeEl = document.getElementById('stat-weight-change');
  if (changeEl) {
    const diff = stats.change_kg || 0;
    const arrow = diff > 0 ? '▲' : (diff < 0 ? '▼' : '—');
    const colorClass = diff > 0 ? 'text-primary' : (diff < 0 ? 'text-info' : 'text-muted');
    changeEl.className = `fw-bold ${colorClass}`;
    changeEl.innerHTML = `${arrow} ${stats.change_kg_display} <span class="small text-muted font-monospace">(${stats.change_pct_display})</span>`;
  }

  // Breed ideal target range
  const targetEl = document.getElementById('stat-target-range');
  if (targetEl) {
    targetEl.textContent = payload.ideal_short_label || `${payload.ideal_min} – ${payload.ideal_max} kg`;
  }

  // Status badge
  const statusEl = document.getElementById('stat-weight-status');
  if (statusEl && stats.status) {
    statusEl.className = `badge ${stats.badge_class || 'bg-success'} px-2 py-1`;
    statusEl.innerHTML = `<i class="fa-solid ${stats.icon || 'fa-circle-check'} me-1"></i> ${stats.status}`;
  }

  // Range Min / Max / Avg stats
  const minMaxAvgEl = document.getElementById('stat-min-max-avg');
  if (minMaxAvgEl) {
    minMaxAvgEl.innerHTML = `<span class="text-muted">Min:</span> <strong>${stats.min_weight}kg</strong> &nbsp;|&nbsp; <span class="text-muted">Max:</span> <strong>${stats.max_weight}kg</strong> &nbsp;|&nbsp; <span class="text-muted">Avg:</span> <strong>${stats.avg_weight}kg</strong>`;
  }
}

/**
 * Internal helper to instantiate or update the Chart.js canvas
 */
function drawPetWeightChart(canvas, payload) {
  const ctx = canvas.getContext('2d');

  // Vibrant gradient background fill
  const gradientFill = ctx.createLinearGradient(0, 0, 0, 240);
  gradientFill.addColorStop(0, 'rgba(99, 102, 241, 0.30)');
  gradientFill.addColorStop(0.8, 'rgba(99, 102, 241, 0.04)');
  gradientFill.addColorStop(1, 'rgba(99, 102, 241, 0.0)');

  // Ideal target band fill between min and max
  const targetFill = 'rgba(16, 185, 129, 0.06)';

  const datasets = [
    {
      label: `${payload.pet_name}'s Weight (kg)`,
      data: payload.data,
      borderColor: '#6366f1',
      borderWidth: 3,
      backgroundColor: gradientFill,
      fill: true,
      tension: 0.38,
      pointBackgroundColor: '#ffffff',
      pointBorderColor: '#6366f1',
      pointBorderWidth: 2.5,
      pointRadius: 5,
      pointHoverRadius: 8,
      pointHoverBackgroundColor: '#6366f1',
      pointHoverBorderColor: '#ffffff',
      pointHoverBorderWidth: 2,
      order: 1,
    }
  ];

  // If breed target bounds are valid, render the reference lines
  if (payload.ideal_min && payload.ideal_max) {
    datasets.push({
      label: `Ideal Target Min (${payload.ideal_min} kg)`,
      data: Array(payload.labels.length).fill(payload.ideal_min),
      borderColor: 'rgba(16, 185, 129, 0.75)',
      borderWidth: 1.5,
      borderDash: [6, 4],
      pointRadius: 0,
      fill: false,
      order: 2,
    });

    datasets.push({
      label: `Ideal Target Max (${payload.ideal_max} kg)`,
      data: Array(payload.labels.length).fill(payload.ideal_max),
      borderColor: 'rgba(16, 185, 129, 0.75)',
      borderWidth: 1.5,
      borderDash: [6, 4],
      pointRadius: 0,
      backgroundColor: targetFill,
      fill: '-1', // fills zone between min and max
      order: 3,
    });
  }

  // Calculate Y-axis bounds with smart padding
  const allValues = [...payload.data];
  if (payload.ideal_min) allValues.push(payload.ideal_min);
  if (payload.ideal_max) allValues.push(payload.ideal_max);
  const minVal = Math.min(...allValues);
  const maxVal = Math.max(...allValues);
  const padding = Math.max(0.2, (maxVal - minVal) * 0.2);

  const yMin = Math.max(0, Math.floor((minVal - padding) * 10) / 10);
  const yMax = Math.ceil((maxVal + padding) * 10) / 10;

  if (petWeightChartInstance) {
    petWeightChartInstance.data.labels = payload.labels;
    petWeightChartInstance.data.datasets = datasets;
    petWeightChartInstance.options.scales.y.min = yMin;
    petWeightChartInstance.options.scales.y.max = yMax;
    petWeightChartInstance.update();
    return;
  }

  petWeightChartInstance = new Chart(canvas, {
    type: 'line',
    data: {
      labels: payload.labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      animation: {
        duration: 750,
        easing: 'easeOutQuart'
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'end',
          labels: {
            boxWidth: 14,
            boxHeight: 14,
            usePointStyle: true,
            pointStyle: 'circle',
            font: { size: 11, family: 'Inter, system-ui, sans-serif', weight: '500' },
            filter: function(item) {
              // Hide redundant target max label if min already represents the band
              return item.datasetIndex < 2;
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.92)',
          titleFont: { size: 12, weight: 'bold' },
          bodyFont: { size: 12 },
          padding: 12,
          cornerRadius: 8,
          boxPadding: 4,
          callbacks: {
            label: function(ctx) {
              if (ctx.datasetIndex === 0) {
                return `  Weight: ${ctx.raw} kg`;
              } else if (ctx.datasetIndex === 1) {
                return `  Breed Target: ${payload.ideal_min} – ${payload.ideal_max} kg`;
              }
              return null;
            },
            afterLabel: function(ctx) {
              if (ctx.datasetIndex === 0 && payload.notes && payload.notes[ctx.dataIndex]) {
                return `  Notes: ${payload.notes[ctx.dataIndex]}`;
              }
              return null;
            }
          }
        }
      },
      scales: {
        y: {
          min: yMin,
          max: yMax,
          title: {
            display: true,
            text: 'Weight (kg)',
            font: { size: 11, weight: 'bold' },
            color: '#64748b'
          },
          grid: {
            color: 'rgba(226, 232, 240, 0.7)',
            drawBorder: false,
          },
          ticks: {
            font: { size: 11 },
            color: '#64748b',
            callback: (v) => `${v} kg`
          }
        },
        x: {
          grid: {
            display: false,
          },
          ticks: {
            font: { size: 11 },
            color: '#64748b',
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: 7
          }
        }
      }
    }
  });
}

/**
 * Real-time AJAX submission for Quick Weight Logger Modal/Form
 */
function submitRealtimeWeightLog(event, formEl, petId, canvasId = 'petWeightChart') {
  event.preventDefault();
  const formData = new FormData(formEl);
  formData.append('range', currentSelectedRange);

  const submitBtn = formEl.querySelector('button[type="submit"]');
  const originalBtnText = submitBtn ? submitBtn.innerHTML : '';
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Saving...';
  }

  fetch(`/health/${petId}/add-weight-ajax/`, {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
    .then(res => res.json())
    .then(payload => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }

      if (payload.success) {
        // Redraw chart with new data immediately
        updateWeightDashboardStats(payload);
        const canvas = document.getElementById(canvasId);
        if (canvas) {
          drawPetWeightChart(canvas, payload);
        }

        // Close modal if open
        const modalEl = document.getElementById('quickLogWeightModal');
        if (modalEl && typeof bootstrap !== 'undefined') {
          const modalInstance = bootstrap.Modal.getInstance(modalEl);
          if (modalInstance) modalInstance.hide();
        }

        // Reset form
        formEl.reset();
        const dateInput = formEl.querySelector('input[type="date"]');
        if (dateInput) {
          dateInput.valueAsDate = new Date();
        }

        // Show toast notification
        showWeightSuccessToast(payload.message || 'Weight logged successfully!');
      } else {
        alert(payload.error || 'Failed to log weight. Please verify the value.');
      }
    })
    .catch(err => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
      console.error('AJAX weight submit error:', err);
      alert('An error occurred while saving the weight record.');
    });
}

/**
 * Toast / Alert feedback notification
 */
function showWeightSuccessToast(message) {
  const container = document.getElementById('weight-toast-container');
  if (!container) {
    const toastDiv = document.createElement('div');
    toastDiv.id = 'weight-toast-container';
    toastDiv.className = 'position-fixed bottom-0 end-0 p-3';
    toastDiv.style.zIndex = '9999';
    toastDiv.innerHTML = `
      <div id="liveWeightToast" class="toast align-items-center text-white bg-success border-0 shadow-lg" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body d-flex align-items-center gap-2">
            <i class="fa-solid fa-circle-check fs-5"></i>
            <span id="weightToastMsg">${message}</span>
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>
    `;
    document.body.appendChild(toastDiv);
  } else {
    document.getElementById('weightToastMsg').textContent = message;
  }

  const toastEl = document.getElementById('liveWeightToast');
  if (toastEl && typeof bootstrap !== 'undefined') {
    const toast = new bootstrap.Toast(toastEl, { delay: 3500 });
    toast.show();
  }
}
