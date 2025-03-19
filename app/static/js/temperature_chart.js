document.addEventListener('DOMContentLoaded', function() {
    if (typeof Chart === 'undefined') {
        console.error('Chart.js non chargé');
        return;
    }
    
    const canvas = document.getElementById('temperatureChart');
    const dataElement = document.getElementById('temperature-chart-data');
    
    if (!canvas || !dataElement) {
        console.error('Canvas ou données non trouvées');
        return;
    }
    
    let chartData;
    try {
        chartData = JSON.parse(dataElement.dataset.chartInfo);
    } catch (error) {
        console.error('Erreur de parsing des données:', error);
        return;
    }
    
    const annotations = {};
    if (chartData.minLimit !== null) {
        annotations.minLine = {
            type: 'line',
            yMin: chartData.minLimit,
            yMax: chartData.minLimit,
            borderColor: 'rgba(255, 0, 0, 0.5)',
            borderWidth: 2,
            label: {
                display: true,
                content: 'Min',
                color: 'red',
                position: 'start',
            }
        };
    }
    if (chartData.maxLimit !== null) {
        annotations.maxLine = {
            type: 'line',
            yMin: chartData.maxLimit,
            yMax: chartData.maxLimit,
            borderColor: 'rgba(255, 0, 0, 0.5)',
            borderWidth: 2,
            label: {
                display: true,
                content: 'Max',
                color: 'red',
                position: 'start',
            }
        };
    }
    
    canvas.parentElement.style.height = '400px'; // Fixe la hauteur du conteneur
    
    new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: chartData.dates && chartData.dates.length > 0 ? chartData.dates : [''],
            datasets: [{
                label: 'Température (°C)',
                data: chartData.values && chartData.values.length > 0 ? chartData.values : [null],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: false,
                pointRadius: 2,
                tension: 0
            }]
        },
        options: {
            responsive: true,
            animation: false,
            maintainAspectRatio: false,
            scales: {
                y: {
                    title: { display: true, text: 'Température (°C)' },
                    min: chartData.minLimit !== null ? chartData.minLimit - 5 : undefined,
                    max: chartData.maxLimit !== null ? chartData.maxLimit + 5 : undefined
                },
                x: { title: { display: true, text: 'Date et heure' } }
            },
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true, intersect: false, mode: 'index' },
                annotation: { annotations }
            }
        }
    });
});
