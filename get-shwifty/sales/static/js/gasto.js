$(document).ready(function() {

    elements = {
        'price':            $('#price'),
        'descripcion':      $('#descripcion'),
        'cedula_vendedor':  $('#cedula_vendedor')
    }

    buttons = {
        'enviar': $('#enviar')
    }

    forms = {
        'register':     $('#register'),
    }

    initialize(elements)

    forms['register'].on('submit', function(e) {

        buttons['enviar'].attr('disabled', true)

        var price           =   to_int(elements['price']),
            description     =   trimText(elements['descripcion']),
            owner_document  =   trimText(elements['cedula_vendedor'])

        if(!price || price <= 0) {

            alert('Ingresa un precio válido')
            elements['price'].val('')
            elements['price'].focus()
            buttons['enviar'].attr('disabled', false)


        } else {
            $.post('/gasto/', {
                value : price,
                description:description,
                owner_document: owner_document
            }, function(data) {

                if(data.ok) {
                    alert('La salida se registro correctamente.')
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

function initialize(elements) {

    elements['price'].val('')
    elements['descripcion'].val('')
    elements['cedula_vendedor'].val('')

}