$(function () {
    $.get('/city-dashboard/data/frontend.json', function (data) {
      var template = '';
      $.each(data[0]['districts'], function(index, district) {
        template += "<div class='row'>";
        template += "<h1>" + district['name'] + "</h1>";
        $.each(district['indicators'], function(index, indicator) {
          template += buildTemplateIndicator(indicator);
        });
        template += "</div>";
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

  var icon = ''
  if(indicator['icon']){
    icon = '<i class="fa ' + indicator["icon"] + ' chart-panel__icon" aria-hidden="true"></i>'
  }

  var achievement = ''
  // var achievement = '<i class="fa fa-arrow-circle-right chart-panel__achievement chart-panel__achievement_on-the-way" aria-hidden="true"></i>'

  return `<div class="col-xs-3 col-md-3 col-mobile">
            <div class="panel panel-default chart-panel">
              <div class="panel-body easypiechart-panel">
                ${icon}
                <h4>${indicator['name']}</h4>
                <div class="easypiechart chart-panel__easypiechart">
                  <div class="easypiechart-${color}" data-percent="${indicator['value']}" ><span class="percent chart-panel__value">${indicator['value']}</span></div>
                  ${achievement}
                  <div class="chart-panel__dimension">${unit}</div>
                </div>
              </div>
            </div>
          </div>`
}
