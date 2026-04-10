function loadAnalytics() {
  fetch("/api/admin/statistics")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let graph_data = data.data;
      if (graph_data === undefined) {
        throw Error("Graph data retrieval failed.");
      }

    fetch("/api/admin/statistics").then(response => {
        return response.json()

    }).then(data => {
        let graph_data = data.data;
        if (graph_data === undefined) {
            throw Error("Graph data retrieval failed.");
        }

            const ctx = document.getElementById('analytics_chart');

        const chartData = {
            labels: ["11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0"],
            datasets: [{
                backgroundColor: "rgba(210, 252, 255, 0.2)",
                borderColor: "rgba(210, 252, 255, 1)",
                data: graph_data, // Placeholder data - replace with actual data from backend
                borderWidth: 1,
                borderRadius: 5
            }]
        }

        Chart.defaults.style = "bold";
        Chart.defaults.color = "#EFE9FF";
        Chart.defaults.font.family = "DM Sans, sans-serif";
        Chart.defaults.plugins.tooltip.titleFont.size = 16;
        Chart.defaults.plugins.tooltip.backgroundColor = "#1d4376";

      const chartData = {
        labels: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
        datasets: [
          {
            backgroundColor: "rgba(210, 252, 255, 0.2)",
            borderColor: "rgba(210, 252, 255, 1)",
            data: graph_data,
            borderWidth: 1,
            borderRadius: 5,
          },
        ],
      };

      Chart.defaults.style = "bold";
      Chart.defaults.color = "#EFE9FF";
      Chart.defaults.font.family = "DM Sans, sans-serif";
      Chart.defaults.plugins.tooltip.titleFont.size = 16;
      Chart.defaults.plugins.tooltip.backgroundColor = "#1d4376";

      new Chart(ctx, {
        type: "bar",
        data: chartData,
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                color: "#EFE9FF",
                font: { family: "DM Sans, sans-serif", size: 14 },
                stepSize: 10, // Adjust step size as needed from backend data range
              },
            },
          },
          plugins: {
            legend: { display: false },
            title: {
              display: true,
              text: "Reviews in the Past 12 Months",
              color: "#EFE9FF",
              font: {
                family: "DM Sans, sans-serif",
                size: 25,
              },
            },
            tooltip: {
              titleFont: {
                family: "DM Sans, sans-serif",
                size: 14,
              },
            },
          },
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    });
}

import { review_card } from "./components/review_card.js";

export function add_reviews(albumid) {
  review_section = document.getElementById("review_section");

  fetch(`/api/admin/reviews`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let reviews = data.reviews;
      reviews.forEach((review) => {
        review_section.appendChild(review_card(review));
      });
    });
}

/*
function loadAnalytics0() {
    
    const ctx = document.getElementById('analytics_chart').getContext('2d');
    // Placeholder for chart data - replace with actual data from backend
    const chartData = {
        labels: ['Category 1', 'Category 2', 'Category 3'],
        datasets: [{
            label: 'Number of Reviews',
            data: [12, 19, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 205, 86, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 205, 86, 1)'
            ],
            borderWidth: 1
        }]
    };

    // Create the chart
    const myChart = new myChart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
*/

// Call the function to load analytics when the page loads
window.onload = loadAnalytics();
window.onload = add_reviews();
