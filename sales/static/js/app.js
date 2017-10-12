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
    elements['tipo_ingreso'].val('Producto')

    elements['tipo_ingreso'].change(function() {
        $tipo = elements['tipo_ingreso']

        if($tipo.val() === 'Producto')
            saleProduct(elements, buttons)

        else
            saleService(elements, buttons)

        initialize(elements)
    })

    buttons['add_product'].on('click', function() {

        var maximum_value = to_int(elements['amount_holder'])

        var value = to_int(elements['amount']) + 1
        value = (value > maximum_value) ? maximum_value : value
        elements['amount'].val(value)

    })

    buttons['remove_product'].on('click', function() {

        var value = to_int(elements['amount']) - 1
        elements['amount'].val(value < 0 ? 0 : value)

    })

    forms['get_product'].on('submit', function(e) {
        var codigo = $.trim(elements['bar_code'].val())
        
        if(codigo) {

            $.get('/producto/', {code: codigo}, function(data) {

                if(!data.ok){
                    alert(data.msg)
                    elements['bar_code'].val('')
                    elements['bar_code'].focus()

                } else {

                    elements['name'].val(data.name)
                    elements['price'].val(data.price)
                    elements['amount_holder'].val(data.amount)

                }

            })
        }

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
    elements['amount_holder'].val('')
    elements['cedula_cliente'].val('')
    elements['cedula_vendedor'].val('')

    elements['pay_with_card'].prop('checked', false)

}