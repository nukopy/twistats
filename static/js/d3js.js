d3.select('#chart').style('background-color', 'blue');

// d3.selectAll('p').style('color', function () {
//     return 'hsl(' + Math.random() * 360 + ',100%, 50%)';
// });

// d3.selectAll("p").style("color", function (d, i) {
//     return i % 2 ? "#fff" : "#eee";
// });

d3.selectAll('p')
    .data([4, 8, 15, 16, 32, 42])
    .style('font-size', function (d) {
        return d + 'px';
    })

// // bar chart data
// var barData = {
//     labels: [{% for index, row in tweets_df.sort_values(by = "created_at", ascending = True).iterrows() %}
// "{{ row['created_at'] }}",
//     {% endfor %}],
// datasets: [
//     {
//         label: "Retweets",
//         backgroundColor: 'rgba(255, 99, 132, 0.2)',
//         borderColor: 'rgba(255,99,132,1)',
//         borderWidth: 10,
//         bezierCurve: false,
//         data: [{% for index, row in tweets_df.sort_values(by = "created_at", ascending = True).iterrows() %}
//                      {{ row["retweets"] }},
//     {% endfor %}]
//      }, {
//     label: "Favorites",
//         data : [{% for index, row in tweets_df.sort_values(by = "created_at", ascending = True).iterrows() %}
// { { row["fav"] } },
// {% endfor %}],
// type: 'line',
//     borderColor: 'rgb(63, 127, 191)',
// }
// ]
// }
// // draw bar chart
// var mychart = document.getElementById("chart");
// var chart = new Chart(mychart, {
//     type: 'bar',
//     data: barData,
//     options: {
//         scales: {
//             yAxes: [
//                 {
//                     ticks: {
//                         beginAtZero: true,
//                         min: 0,
//                         max: 1000
//                     }
//                 }
//             ]
//         }
//     }
// });

