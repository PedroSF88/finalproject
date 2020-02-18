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
    myFunction();
});
   

function myFunction() {
        var x = document.createElement("IMG");
        x.setAttribute("src", "/resources/assets/images/cracker.jpg");
        x.setAttribute("width", "304");
        x.setAttribute("height", "228");
        x.setAttribute("alt", "Craker Jacks");
        document.body.appendChild(x);
    }
