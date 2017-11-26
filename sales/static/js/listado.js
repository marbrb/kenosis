'use strict'

$(document).ready(function() {

    var elements = {
        'row'           : $('#row_base'),
        'table'         : $('#table'),
        'credit'        : $('#credit'),
        'cash'          : $('#cash'),
        'table_expense' : $('#table_expense')
    }

    var buttons = {
        'print' : $('#print')
    }

    buttons['print'].click(function(e) {
        window.print()
    })

    $.get('/registros', function(data) {
        var registros = data.data

        elements['credit'].text(data.card_cash)

        var ingresos = {}
        var gastos = {}

        for(var i in registros) {
            var name = registros[i]['owner_name']

            if(registros[i].register_type === 'ingreso') {
                
                if(!ingresos[name])
                    ingresos[name] = 0

                ingresos[name] += registros[i].value

            } else {

                if(!gastos[name])
                    gastos[name] = 0

                gastos[name] += registros[i].value

            }
        }

        var idx = 1
        for(var i in ingresos){
            addRow(elements['row'], elements['table'], idx++, {
                key: i, 
                val: ingresos[i]
            })            
        }

        idx = 1
        for(var i in gastos) {
            addRow(elements['row'], elements['table_expense'], idx++, {
                key: i,
                val: gastos[i]
            })
        }

        var g = gastos['kenosis']
        if (g === undefined) {
            g = 0 
        }
        elements['cash'].text(data.today_cash - g)


    })
})

function addRow(base, table, idx, register) {

    var new_row = base.clone()
    var children = new_row.children()

    new_row.attr('hidden', false) 

    // children[0].textContent = idx
    children[0].textContent = register.key
    children[1].textContent = register.val

    table.append(new_row)

}
