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
        'enviar':           $('#enviar')
    }

    forms = {
        'register':     $('#register'),
        'get_product':  $('#get_product')
    }

    initialize(elements)
    elements['tipo_ingreso'].val('Producto')

    elements['tipo_ingreso'].change(function() {
        $tipo = elements['tipo_ingreso']
        initialize(elements)

        if($tipo.val() === 'Producto')
            saleProduct(elements, buttons)

        else
            saleService(elements, buttons)

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

        buttons['enviar'].attr('disabled', true)

        var name            =   trimText(elements['name']),
            price           =   to_int(elements['price']),
            amount          =   to_int(elements['amount']),
            is_card         =   elements['pay_with_card'].prop('checked'),
            bar_code        =   trimText(elements['bar_code'])
            comission       =   to_int(elements['comission']),
            description     =   trimText(elements['descripcion']),
            tipo_ingreso    =   elements['tipo_ingreso'].val(),
            owner_document  =   trimText(elements['cedula_vendedor']),
            client_document =   trimText(elements['cedula_cliente'])


        if(amount < 1) {
            alert('La cantidad minima es 1')
            buttons['enviar'].attr('disabled', false)

        } else if(tipo_ingreso == 'Producto' && !bar_code){

            alert('Es necesario buscar un producto')
            elements['bar_code'].focus()
            buttons['enviar'].attr('disabled', false)


        }else if(tipo_ingreso === 'Servicio' && !price){

            alert('Es necesario llenar el campo Precio')
            elements['price'].focus()
            buttons['enviar'].attr('disabled', false)

        }else if(tipo_ingreso === 'Servicio' && !name) {

            alert('Es necesario llenar el campo Nombre')
            elements['name'].focus()
            buttons['enviar'].attr('disabled', false)
        
        } else if(!comission) {

            alert('Es necesario llenar el campo Procentaje Vendedor')
            elements['comission'].focus()
            buttons['enviar'].attr('disabled', false)

        } else {
            $.post('/venta/', {
                el_name: name,
                is_card: is_card,
                value: amount * price,
                description: description,
                owner_document: owner_document,
                client_document: client_document,
                percent: comission,
            }, function(data) {

                if(data.ok) {
                    alert('El ingreso se registro correctamente.')
                    initialize(elements)
                    
                } else {
                    alert(data.msg)
                }

                buttons['enviar'].attr('disabled', false)

            })
            
        }
        e.preventDefault()
    }) 


})

function to_int($element) {
    var value = $element.val()
    value = value == '' ? 0 : parseInt(value)
    return value
}

function trimText($element) {
    return $.trim($element.val())
}

function saleProduct(elements, buttons) {
    elements['price'].attr('readonly', true)
    elements['name'].attr('readonly', true)
    elements['name'].attr('placeholder', 'Nombre del producto')
    elements['bar_code'].attr('disabled', false)
    elements['amount_holder'].val('')
    buttons['search_product'].attr('disabled', false)
}

function saleService(elements, buttons) {
    elements['price'].attr('readonly', false)
    elements['name'].attr('readonly', false)
    elements['name'].attr('placeholder', 'Nombre del servicio')
    elements['bar_code'].attr('disabled', true)
    elements['amount_holder'].val('100')
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