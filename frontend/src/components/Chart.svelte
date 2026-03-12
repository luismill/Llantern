<script>
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';

  export let data = {
    labels: ['Income', 'Expenses', 'Balance'],
    datasets: [{
      data: [0, 0, 0],
      backgroundColor: [
        '#10b981', // green
        '#ef4444', // red
        '#3b82f6', // blue
      ],
      borderWidth: 0,
      borderRadius: 4
    }]
  };
  export let type = 'bar';
  export let title = 'Current Month Overview';

  let canvas;
  let chart;

  onMount(() => {
    chart = new Chart(canvas, {
      type: type,
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
          title: {
            display: true,
            text: title,
            color: '#cbd5e1',
            font: {
              family: "'Outfit', sans-serif",
              size: 16,
              weight: 500
            }
          },
          tooltip: {
            backgroundColor: '#1e1e1e',
            titleColor: '#f8fafc',
            bodyColor: '#cbd5e1',
            borderColor: '#333333',
            borderWidth: 1,
            padding: 10,
            displayColors: false,
            callbacks: {
              label: function(context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                if (context.parsed.y !== null) {
                  label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'EUR' }).format(context.parsed.y);
                }
                return label;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: '#333333',
              drawBorder: false,
            },
            ticks: {
              color: '#94a3b8',
              font: {
                family: "'Outfit', sans-serif"
              }
            }
          },
          x: {
            grid: {
              display: false,
              drawBorder: false,
            },
            ticks: {
              color: '#94a3b8',
              font: {
                family: "'Outfit', sans-serif"
              }
            }
          }
        },
        animation: {
          duration: 1000,
          easing: 'easeOutQuart'
        }
      }
    });
  });

  $: if (chart && data) {
    chart.data = data;
    chart.update();
  }

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<div class="relative w-full h-full min-h-[250px]">
  <canvas bind:this={canvas}></canvas>
</div>
