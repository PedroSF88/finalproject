// d3.json("/teams/2016").then((teams) => {
//     Object.values(teams).forEach(team => {
//         Object.entries(team).forEach(([key, value]) => {
//             console.log(`${key}:${value}`)
//         });
//     });
// });

// d3.json("/people").then((teams) => {
//     Object.values(teams).forEach(team => {
//         Object.entries(team).forEach(([key, value]) => {
//             console.log(`${key}:${value}`)
//         });
//     });
// });

$(document).ready(function() {
    populateYears();
    buildCharts(2016);
    
    //listen for year change
    $('#years').change(function() {
     buildCharts($('#years').val())
    });
});

function populateYears() {
    d3.json('/years').then((data) => {
        var objs = Object.values(data);

        var years = [];
        for (var i = 0; i < objs.length; i++) {
            years.push(objs[i].yearID);
        }

        years.forEach(year => {
            $('#years').append(`<option>${year}</option>`);
        });
        $('#years').val(years[0]);
    });
}

// function buildCharts(year) {
//     d3.json(`/teams/${year}`).then((data) => {
//         var objs = Object.values(data);

//         var runs = [];
//         var wins = [];
//         var teams = [];
//         for (var i = 0; i < objs.length; i++) {
//             runs.push(objs[i].R);
//             wins.push(objs[i].W);
//             teams.push(objs[i].name);
//         }

//         // Build a Bubble Chart
//         var bubbleLayout = {
//             margin: { t: 0 },
//             hovermode: "closest",
//             xaxis: { title: "Team Wins" },
//             yaxis: { title: "Team Runs" }
//         };
//         var bubbleData = [{
//             x: wins,
//             y: runs,
//             text: teams,
//             mode: "markers",
//             marker: {
//                 size: 10,
//                 color: wins,
//                 colorscale: "Earth"
//             }
//         }];

//         Plotly.newPlot("bubble", bubbleData, bubbleLayout);
//     });
// }
function buildCharts(year) {
    d3.json(`/salaries/${year}`).then((data) => {
        var objs = Object.values(data);

        var salaries = [];
        var teams = [];
        for (var i = 0; i < objs.length; i++) {
            salaries.push(objs[i].avgsal);
            teams.push(objs[i].teamID);
        }
        console.log(salaries)
        console.log(teams)

        // Build a Bubble Chart
        var barLayout = {
            margin: { t: 0 },
            hovermode: "closest",
            width: 1100,
            height: 400,
            xaxis: { title: "Teams" },
            yaxis: { title: "Team Average Salary" }
        };
        var barData = [{
            x: teams,
            y: salaries,
            text: teams,
            type: "bar",
        }];

        Plotly.newPlot("bubble", barData, barLayout);
    });
}