$(document).ready(function() {

    elements = {
        'name':             $('#name'),
        'price':            $('#price'),
        'amount':           $('#amount'),
        'bar_code':         $('#bar_code'),
        'comission':        $('#comission'),
        'descripcion':      $('#descripcion'),
        'tipo_ingreso':     $('#tipo_ingreso'),
        'pay_with_card':    $('#pay_with_card'),
        'amount_holder':    $('#amount_holder'),
        'cedula_cliente':   $('#cedula_cliente'),
        'cedula_vendedor':  $('#cedula_vendedor')
    }

    buttons = {
        'add_product':      $('#add_product'),
        'search_product':   $('#search_product'),
        'remove_product':   $('#remove_product'),
    }

    forms = {
        'register':     $('#register'),
        'get_product':  $('#get_product')
    }

    initialize(elements)

    elements['tipo_ingreso'].change(function() {
        $tipo = elements['tipo_ingreso']

        if($tipo.val() === 'Producto')
            saleProduct(elements, buttons)

        else
        saleService(elements, buttons)

    })

    buttons['add_product'].on('click', function() {

        var value = to_int(elements['amount'])
        elements['amount'].val(value + 1)

        //TODO: No exceder la cantidad máxima de producto

    })

    buttons['remove_product'].on('click', function() {

        var value = to_int(elements['amount']) - 1
        elements['amount'].val(value < 0 ? 0 : value)

    })

    forms['get_product'].on('submit', function(e) {
        console.log('Sending product...')
        $.get('http://59dede2bb11b290012f17b52.mockapi.io/kenosis/product', 
            function(data) {
                $('#price').val(data[0].price)
                $('#name').val(data[0].name)
            }
        )
        e.preventDefault()
    })

    forms['register'].on('submit', function(e) {
        console.log('ja')
        e.preventDefault()
    }) 


})

function to_int($element) {
    var value = $element.val()
    value = value == '' ? 0 : parseInt(value)
    return value
}

function saleProduct(elements, buttons) {
    elements['price'].attr('readonly', true)
    elements['name'].attr('readonly', true)
    elements['bar_code'].attr('disabled', false)
    buttons['search_product'].attr('disabled', false)
}

function saleService(elements, buttons) {
    elements['price'].attr('readonly', false)
    elements['name'].attr('readonly', false)
    elements['bar_code'].attr('disabled', true)
    buttons['search_product'].attr('disabled', true)
}

function initialize(elements) {

    elements['name'].val('')
    elements['price'].val('')
    elements['amount'].val('')
    elements['bar_code'].val('')
    elements['comission'].val('')
    elements['descripcion'].val('')
    elements['tipo_ingreso'].val('Producto')
    elements['amount_holder'].val('')
    elements['cedula_cliente'].val('')
    elements['cedula_vendedor'].val('')

    elements['pay_with_card'].prop('checked', false)

}