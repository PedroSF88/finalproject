$(document).ready(function() {
    populatePlayer();
    buildCharts2("rodrial01");
    playerinfo("rodrial01");
    
    
    //listen for year change
      $('#player').change(function() {
          buildCharts2($('#player').val());
          playerinfo($('#player').val());
      });
  });

function populatePlayer() {
    d3.json('/playerID').then((data) => {
        var objs = Object.values(data);
        var player = [];
        for (var i = 0; i < objs.length; i++) {
            player.push(objs[i].playerID);
        }
        console.log(player)
        player.forEach(player => {
            $('#player').append(`<option>${player}</option>`);
        });
        $('#player').val(player[0]);
    });
}
function buildCharts2(player) {
   d3.json(`/playersalaries/${player}`).then((data) => {
    console.log(player)
      var objs = Object.values(data);
      console.log(objs)
      var years = [];
      var salary = [];
      console.log(years)
  
      for (var i = 0; i < objs.length; i++) {
          years.push(objs[i].yearID);
          salary.push(objs[i].salary);
         
      }
      // Build a Bubble Chart
      var bubbleLayout = {
        margin: { t: 0 },
        hovermode: "closest",
        xaxis: { title: "Year" },
        yaxis: { title: "Salary"},
        title: {title: "Player Salary Comparisons"},
        autosize: false,
        width: 1100,
        height: 900,
        margin: {
            l: 50,
            r: 50,
            b: 100,
            t: 100,
            pad: 4,
        },
        legend: {
          x: 0,
          y: 1,
        }
      };
      var bubbleData = [
        {
          x: years,
          y: salary,
          text: player,
          mode: "markers",
          marker: {
            size: 30,
            color: player,
            colorscale: "Earth"
          }
        }
      ];
  
      Plotly.plot("bubble", bubbleData, bubbleLayout);
    });
}
  function playerinfo(player){
    d3.json(`/playerinfo/${player}`).then((data) => {
      var objs = Object.values(data);
      var playerid = [];
      var GivenName =[];
      var FirstName= [];
      var Lastname= [];
      var CofBirth=[];
      var datedebut=[];
      var weightlbs=[];
      var heightft=[];
      var batting=[];
      var throwing=[];

      console.log(objs)

      for (var i = 0; i < objs.length; i++) {
          playerid.push(objs[i].playerID);
          GivenName.push(objs[i].nameGiven);
          FirstName.push(objs[i].nameFirst);
          Lastname.push(objs[i].nameLast);
          CofBirth.push(objs[i].birthCountry);
          datedebut.push(objs[i].debut);
          weightlbs.push(objs[i].weight);
          heightft.push(objs[i].height);
          batting.push(objs[i].bats);
          throwing.push(objs[i].throws);
      }
      
      
      var h = document.createElement("H1");
      var t = document.createTextNode(`Player ${GivenName} (AKA ${FirstName} ${Lastname}) was born in the ${CofBirth}. He debut his carrier in ${datedebut}. Stats: Weight: ${weightlbs}/ Height: ${heightft}/  ${batting} batter/  ${throwing} thrower.`);
      d3.select("#playerinfo")
      .selectAll("panel-body")
      h.appendChild(t);
      document.body.appendChild(h);
      
  });
  }