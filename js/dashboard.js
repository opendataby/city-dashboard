function render(data) {
  var template = '';

  var districts = _.keys(data)

  districts.forEach(function (districtId) {
    const district = data[districtId]

    template += "<div class='row'>";
    template += `<h1 id=${districtId}>${district['name']}</h1>`;

    $.each(district['indicators'], function(index, indicator) {
      template += buildTemplateIndicator(indicator);
    });

    template += "</div>";
  })

  $('#dashboard').html(template);

  $('.easypiechart-teal').easyPieChart({
    scaleColor: false,
    barColor: '#1ebfae'
  });

  $('.easypiechart-red').easyPieChart({
    scaleColor: false,
    barColor: '#f9243f'
  });
}

$(function () {
    $.get('/city-dashboard/frontend.json', function (frontendData) {
      let fetchData = Promise.all(
          frontendData
          .map((indicator) => `data/indicators/${indicator.data}`)
          .map(dataUrl=>($.get(dataUrl)))
      )

      fetchData.then(function (indicatorData) {
        var indicatorHash = indicatorData.reduce(function (hash, indicator) {
          hash[indicator.id] = indicator
          return hash
        }, {})

        var districtsData = indicatorData.reduce(function (districtsHash, indicator) {
          const indicatorId = indicator.id

          indicator.districts.forEach(function (district) {
            let districtData = districtsHash[district.id]

            if (districtData === undefined) {
              districtsHash[district.id] = {
                name: district.name,
                indicators: []
              }
              districtData =  districtsHash[district.id]
            }

            let indicatorData = _.cloneDeep(indicator)
            delete indicatorData.districts
            indicatorData.value = district.value
            indicatorData.isOk = district.isOk

            districtData.indicators.push(indicatorData)
          })

          return districtsHash
        }, {})
        console.log(indicatorHash, districtsData)

        render(districtsData)
      })
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
