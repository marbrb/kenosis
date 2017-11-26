$(document).ready(function() {

    elements = {
        'price':            $('#price'),
        'comission':        $('#comission'),
        'descripcion':      $('#descripcion'),
        'pay_with_card':    $('#pay_with_card'),
        'cedula_cliente':   $('#cedula_cliente'),
        'cedula_vendedor':  $('#cedula_vendedor')
    }

    buttons = {
        'enviar':           $('#enviar')
    }

    forms = {
        'register':     $('#register'),
    }

    initialize(elements)

    forms['register'].on('submit', function(e) {

        // buttons['enviar'].attr('disabled', true)

        var price           =   to_int(elements['price']),
            is_card         =   elements['pay_with_card'].prop('checked'),
            comission       =   to_int(elements['comission']),
            description     =   trimText(elements['descripcion']),
            owner_document  =   trimText(elements['cedula_vendedor']),
            client_document =   trimText(elements['cedula_cliente'])

        if(!description) {

            alert('Tienes que ingresar una descripción')
            elements['descripcion'].val('')
            buttons['enviar'].attr('disabled', false)
        
        } else if(!price) {

            alert('El precio tiene que ser mayor a cero.')
            elements['price'].val('')
            elements['price'].focus()
            buttons['enviar'].attr('disabled', false)

        } else if(comission !== 0 && !comission) {

            alert('El porcentaje del vendedor tiene que ser un número.')
            elements['comission'].val('')
            elements['comission'].focus()            
            buttons['enviar'].attr('disabled', false)

        } else if(comission > 100) {
            alert('El porcentaje del vendedor tiene que ser menor a 100.')
            elements['comission'].val('')
            elements['comission'].focus()            
            buttons['enviar'].attr('disabled', false)
        }else {

            $.post('venta/servicio', {
                is_card: is_card,
                owner_document: owner_document,
                client_document: client_document,
                services: JSON.stringify([{
                    el_name: description,
                    value:  price,  
                    percent: comission,
                }])
            }, function(data) {

                if(data.ok) {
                    alert('El ingreso se registro correctamente.')
                    elements['descripcion'].val('')
                    elements['price'].val('')
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
    if (value < 0) return NaN
    return value
}

function trimText($element) {
    return $.trim($element.val())
}

function initialize(elements) {

    elements['price'].val('')
    elements['comission'].val('')
    elements['descripcion'].val('')
    elements['cedula_cliente'].val('')

    elements['pay_with_card'].prop('checked', false)

}