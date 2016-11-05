$(function () {
    $.get('/city-dashboard/data/frontend.json', function (data) {
      var template = '';
      $.each(data[0]['districts'], function(index, district) {
        console.log(district['name'])
        template += "<h1>" + district['name'] + "</h1>";
        $.each(district['indicators'], function(index, indicator) {
          template += buildTemplateIndicator(indicator);
        });
      });

      $('#dashboard').html(template);

      $('.easypiechart-teal').easyPieChart({
        scaleColor: false,
        barColor: '#1ebfae'
      });

      $('.easypiechart-red').easyPieChart({
        scaleColor: false,
        barColor: '#f9243f'
      });
    });
});

function buildTemplateIndicator(indicator){
  // One more color: orange
  var color = indicator['value'] <= indicator['average'] ? 'teal' : 'red';
  var unit = indicator['unit'] !== undefined ? indicator['unit'] : ''

  return `<div class="col-xs-6 col-md-3">
            <div class="panel panel-default">
              <div class="panel-body easypiechart-panel">
                <h4>${indicator['name']}</h4>
                <div class="easypiechart easypiechart-${color}" data-percent="${indicator['value']}" ><span class="percent">${indicator['value']} ${unit}</span>
                </div>
              </div>
            </div>
          </div>`;
}
