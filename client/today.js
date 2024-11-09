const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

const data = {
    labels: labels,
    datasets: [{
        label: 'CO2 Emissions per Month',
        data: [65, 59, 80, 81, 56, 55, 40],
        backgroundColor: [
            'rgba(147, 0, 0, 0.2)',   
            'rgba(255, 165, 0, 0.2)',  
            'rgba(255, 205, 86, 0.2)', 
            'rgba(75, 192, 192, 0.2)', 
            'rgba(54, 162, 235, 0.2)', 
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)' 
        ],
        borderColor: [
            'rgb(147, 0, 0)',   
            'rgb(255, 165, 0)',  
            'rgb(255, 205, 86)', 
            'rgb(75, 192, 192)', 
            'rgb(54, 162, 235)', 
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)' 
        ],
        borderWidth: 1
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
    