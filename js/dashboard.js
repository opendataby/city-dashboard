$(function () {
    console.log('start!')
    $.get('/city-dashboard/data/test.json', function (data) {
        console.log(data)

        var template = `
<div class="panel panel-default chart-panel">
    <div class="panel-body easypiechart-panel">
        <i class="fa fa-area-chart chart-panel__icon" aria-hidden="true"></i>
        <h4>Забруджванне</h4>
        <div class="easypiechart chart-panel__easypiechart">
            <div id="easypiechart-blue" data-percent="${data.pollution}" ><span class="percent chart-panel__value">${data.pollution}</span></div>
            <div class="chart-panel__dimension">Адзінкі вымярэння</div>
            <i class="fa fa-check-circle chart-panel__achievement chart-panel__achievement_done" aria-hidden="true"></i>
        </div>
    </div>
</div>`

        $('#chart_pollution').html(template)

        $('#easypiechart-blue').easyPieChart({
            scaleColor: false,
            barColor: '#30a5ff'
        })
    })
})
