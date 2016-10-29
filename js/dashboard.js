$(function () {
    console.log('start!')
    $.get('/city-dashboard/data/test.json', function (data) {
        console.log(data)

        var template = `<div class="panel panel-default">
					<div class="panel-body easypiechart-panel">
						<h4>Забруджванне</h4>
						<div class="easypiechart" id="easypiechart-blue" data-percent="${data.pollution}" ><span class="percent">${data.pollution}%</span>
						</div>
					</div>
				</div>`

        $('#chart_pollution').html(template)



    })
})
