google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ['Category', 'Amount'],
    ['Rent', 1400],
    ['Subscriptions', 50],
    ['Utilities', 500],
    ['Bills', 75]
  ]);

  var options = {
    title: 'Cost Breakdown',
    is3D: true
  };

  var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
  chart.draw(data, options);
}
