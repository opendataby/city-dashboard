$(function () {
    console.log('start!')
    $.get('/city-dashboard/data/test.json', function (data) {
        console.log(data)
    })
})
