new Chart(
    document.getElementById('statistic-profile-rating-chart'),
    {
        type: 'bar',
        data: {
            labels: user_rank_distribution.map(row => row.rank),
            datasets: [
                {
                    label: 'Распределение по рангам',
                    data: user_rank_distribution.map(row => row.count)
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
        }
    }
);

new Chart(
    document.getElementById('statistic-profile-tasks-chart'),
    {
        type: 'doughnut',
        data: data_tasks,
    }
);