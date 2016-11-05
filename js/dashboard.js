$(function () {
    $.get('/city-dashboard/data/frontend.json', function (data) {
      var template = '';
      $.each(data[0]['params'], function(index, params) {
        template += indicator(params);
      });

      $('#indicators').html(template);

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

function indicator(params){
  // One more color: orange
  var color = params['value'] <= params['average'] ? 'teal' : 'red';
  var unit = params['unit'] !== undefined ? params['unit'] : ''

  return `<div class="col-xs-6 col-md-3">
            <div class="panel panel-default">
              <div class="panel-body easypiechart-panel">
                <h4>${params['parameter']}</h4>
                <div class="easypiechart easypiechart-${color}" data-percent="${params['value']}" ><span class="percent">${params['value']} ${unit}</span>
                </div>
              </div>
            </div>
          </div>`;
}
