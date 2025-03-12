// Function to create LOS comparison chart
function createLOSChart(data) {
    const ctx = document.getElementById('losChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Length of Stay Comparison'
                }
            }
        }
    });
}

// Function to create complication rates chart
function createComplicationChart(data) {
    const ctx = document.getElementById('complicationChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Complication Rates by Surgeon'
                }
            }
        }
    });
}

// Function to create stage distribution chart
function createStageChart(data) {
    const ctx = document.getElementById('stageChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Stage Distribution'
                }
            }
        }
    });
} 