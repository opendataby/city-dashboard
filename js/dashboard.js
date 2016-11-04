$(function () {
    console.log('start!')
    $.get('/city-dashboard/data/test.json', function (data) {
        console.log(data)

        var template = `<div class="panel panel-default chart-panel">
					<div class="panel-body easypiechart-panel">
					    <i class="fa fa-area-chart chart-panel__icon" aria-hidden="true"></i>
						<h4>Забруджванне</h4>
						<div class="easypiechart chart-panel__easypiechart" id="easypiechart-blue" data-percent="${data.pollution}" ><span class="percent">${data.pollution}%</span>
						</div>
					</div>
				</div>`

        $('#chart_pollution').html(template)



    })
})
