$(document).ready(function() {

	var $amount_field = $('#amount');

	$('#add_product').on('click', function() {

		var value = to_int($amount_field)
		$amount_field.val(value + 1)

		//TODO: No exceder la cantidad máxima de producto

	})

	$('#remove_product').on('click', function() {
		
		var value = to_int($amount_field) - 1
		$amount_field.val(value < 0 ? 0 : value)

	})
})

function to_int($element) {
	var value = $element.val()
	value = value == '' ? 0 : parseInt(value)
	return value
}


