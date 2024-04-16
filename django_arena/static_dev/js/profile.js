let data_rating = [
    {year: 2010, count: 10},
    {year: 2011, count: 20},
    {year: 2012, count: 15},
    {year: 2013, count: 25},
    {year: 2014, count: 22},
    {year: 2015, count: 30},
    {year: 2016, count: 28},
];

new Chart(
    document.getElementById('statistic-profile-rating-chart'),
    {
        type: 'bar',
        data: {
            labels: data_rating.map(row => row.year),
            datasets: [
                {
                    label: 'Acquisitions by year',
                    data: data_rating.map(row => row.count)
                }
            ]
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