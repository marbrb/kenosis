$(document).ready(function() {

	var $amount_field = $('#amount');
	console.log($('#remove_product'))

	$('#add_product').on('click', function() {

		var value = to_int($amount_field)
		$amount_field.val(value + 1)

		//TODO: No exceder la cantidad máxima de producto

	})

	$('#remove_product').on('click', function() {
		console.log('guasap')
		var value = to_int($amount_field) - 1
		$amount_field.val(value < 0 ? 0 : value)

	})

	$('#get_product').on('submit', function(e) {
		console.log('buenala')
		e.preventDefault()
	})

	$('#register').on('submit', function(e) {
		console.log('ja')
		e.preventDefault()
	}) 

})

function to_int($element) {
	var value = $element.val()
	value = value == '' ? 0 : parseInt(value)
	return value
}


