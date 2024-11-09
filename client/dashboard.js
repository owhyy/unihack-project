
const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

const data = {
    labels: labels,
    datasets: [{
        label: 'CO2 Emissions per Month',
        data: [65, 59, 80, 81, 56, 55, 40],
        backgroundColor: [
            'rgba(147, 0, 0, 1)',   
            'rgba(147, 0, 0, 1)',  
            'rgba(147, 0, 0, 1)', 
            'rgba(147, 0, 0, 1)', 
            'rgba(147, 0, 0, 1)', 
            'rgba(147, 0, 0, 1)',
            'rgba(147, 0, 0, 1)' 
        ]
    }]
};

const config = {
    type: 'bar',
    data: data,
    options: {
        responsive: true, 
        maintainAspectRatio: false, 
        scales: {
            x: {
                grid: {
                    display: false 
                },
                ticks: {
                    color: '#fff' 
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    color: '#ddd' 
                },
                ticks: {
                    color: '#fff' 
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: '#fff' 
                }
            },
            tooltip: {
                backgroundColor: '#333', 
                titleColor: '#fff', 
                bodyColor: '#fff', 
                borderColor: '#930000', 
                borderWidth: 1 
            }
        }
    }
};


const ctx = document.getElementById('timeChart').getContext('2d');
new Chart(ctx, config);
    