$(document).ready(function() {

    elements = {
        'name':             $('#name'),
        'price':            $('#price'),
        'bar_code':         $('#bar_code'),
        'comission':        $('#comission'),
        'pay_with_card':    $('#pay_with_card'),
        'cedula_cliente':   $('#cedula_cliente'),
        'cedula_vendedor':  $('#cedula_vendedor')
    }

    buttons = {
        'search_product':   $('#search_product'),
        'enviar':           $('#enviar')
    }

    forms = {
        'register':     $('#register'),
        'get_product':  $('#get_product')
    }

    initialize(elements)

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
                }

            })
        }

        e.preventDefault()
    })

    forms['register'].on('submit', function(e) {

        buttons['enviar'].attr('disabled', true)

        var name            =   trimText(elements['name']),
            price           =   to_int(elements['price']),
            is_card         =   elements['pay_with_card'].prop('checked'),
            bar_code        =   trimText(elements['bar_code'])
            comission       =   to_int(elements['comission']),
            owner_document  =   trimText(elements['cedula_vendedor']),
            client_document =   trimText(elements['cedula_cliente'])
        
        if(!bar_code){

            alert('Es necesario buscar un producto')
            elements['bar_code'].focus()
            buttons['enviar'].attr('disabled', false)

        } else if(comission !== 0 && !comission)  {

            alert('El porcentaje de comision tiene que ser un número')
            elements['comission'].focus()
            elements['comission'].val()
            buttons['enviar'].attr('disabled', false)

        }else if(comission > 100) {
            alert('El porcentaje del vendedor tiene que ser menor a 100.')
            elements['comission'].val('')
            elements['comission'].focus()            
            buttons['enviar'].attr('disabled', false)
        } else {
            $.post('/venta/producto/', {
                el_name: name,
                is_card: is_card,
                value: price,
                owner_document: owner_document,
                client_document: client_document,
                product_code: bar_code,
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
    if(value < 0) return NaN
    return value
}

function trimText($element) {
    return $.trim($element.val())
}

function initialize(elements) {

    elements['name'].val('')
    elements['price'].val('')
    elements['bar_code'].val('')
    elements['comission'].val('')
    elements['cedula_cliente'].val('')

    elements['pay_with_card'].prop('checked', false)

}