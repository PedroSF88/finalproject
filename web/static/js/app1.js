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

function buildCharts(year) {
    d3.json(`/teams/${year}`).then((data) => {
        var objs = Object.values(data);

        var runs = [];
        var wins = [];
        var teams = [];
        for (var i = 0; i < objs.length; i++) {
            runs.push(objs[i].R);
            wins.push(objs[i].W);
            teams.push(objs[i].name);
        }

        // Build a Bubble Chart
        
        var bubbleLayout = {
            margin: { t: 0 },
            hovermode: "closest",
            title: "Runs Vs Wins",
            xaxis: { title: "Team Runs" },
            yaxis: { title: "Team wins" },
            autosize: false,
            width: 1100,
            height: 900,
            margin: {
                l: 50,
                r: 50,
                b: 100,
                t: 100,
                pad: 4
            },
        };
        
        var bubbleData = [{
            x: runs,
            y: wins,
            text: teams,
            mode: "markers",
            marker: {
                size: wins,
                color: wins,
                colorscale: -"Earth"
            }
        }];

        Plotly.newPlot("bubble", bubbleData, bubbleLayout);
    });

}