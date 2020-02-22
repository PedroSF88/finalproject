var csv = "train.csv";
csv += "text weight\n";
csv += "Lorem 15\n";
csv += "Ipsum 9";

var lines = csv.split("\n");
var titles = lines[0].split(" ");
var data = new Array(lines.length - 1);

for (var i = 1; i < lines.length; i++) {
  data[i - 1] = {};
  lines[i] = lines[i].split(" ");
  for (var j = 0; j < titles.length; j++) {
    data[i - 1][titles[j]] = lines[i][j];
  }
}

function processData(csv) { 
  let allTextLines = csv.split(/\r\n|\n);

  for (let i = 0; i < allTextLines.length; i++){
    let row = allTextLines[i].split(';');

    let col = [];

    for (let j = 0; j < row.length; j++){
      col.push(row[j]);

    }
  }
}



console.log(data);