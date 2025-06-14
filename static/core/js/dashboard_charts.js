console.log('test');

document.addEventListener('DOMContentLoaded', () => {
    const stockCtx = document.getElementById('stockChart')?.getContext('2d');
    if (stockCtx && window.nombresProductos && window.cantidadesStock) {
        const colores = [
            'rgba(59, 130, 246, 0.7)',   // Azul
            'rgba(16, 185, 129, 0.7)',   // Verde menta
            'rgba(251, 191, 36, 0.7)',   // Amarillo
            'rgba(239, 68, 68, 0.7)',    // Rojo
            'rgba(168, 85, 247, 0.7)',   // Púrpura
            'rgba(236, 72, 153, 0.7)',   // Rosado
            'rgba(34, 197, 94, 0.7)',    // Verde intenso
            'rgba(20, 184, 166, 0.7)',   // Turquesa
            'rgba(147, 51, 234, 0.7)',   // Morado oscuro
            'rgba(252, 211, 77, 0.7)'    // Amarillo claro
        ];


        const coloresRepetidos = window.nombresProductos.map((_, i) => colores[i % colores.length]);

        new Chart(stockCtx, {
            type: 'doughnut',
            data: {
                labels: window.nombresProductos,
                datasets: [{
                    label: 'Cantidad en Stock',
                    data: window.cantidadesStock,
                    backgroundColor: coloresRepetidos,
                    borderColor: 'rgba(255, 255, 255, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: { enabled: true }
                }
            }
        });
    }

    const ventasCtx = document.getElementById('ventasChart')?.getContext('2d');
    if (ventasCtx && window.diasVentas && window.totalesVentas) {
        new Chart(ventasCtx, {
            type: 'line',
            data: {
                labels: window.diasVentas,
                datasets: [{
                    label: 'Total Vendido ($)',
                    data: window.totalesVentas,
                    fill: true,
                    tension: 0.4,
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: { display: true },
                    tooltip: { enabled: true }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    const ctxMenos = document.getElementById('productosMenosVendidosChart')?.getContext('2d');
    if (ctxMenos && window.menosNombres && window.menosCantidades) {
        new Chart(ctxMenos, {
            type: 'bar',
            data: {
                labels: window.menosNombres,
                datasets: [{
                    label: 'Cantidad Vendida',
                    data: window.menosCantidades,
                    backgroundColor: 'rgba(239, 68, 68, 0.5)',
                    borderColor: 'rgba(239, 68, 68, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: false,
                indexAxis: 'y',
                plugins: {
                    legend: { display: true },
                    tooltip: { enabled: true }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
});
