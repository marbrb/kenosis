$(function () {
  $('.js-reverse-sale').on('click', function () {
    var url = $(this).data('url');
    $.confirm({
      title: 'Eliminar ultima venta',
      content: '¿deseas eliminar la ultima venta de servicio/producto?',
      type: 'orange',
      buttons: {
        eliminar: function () {
          $.get(url, function (response) {
              $.alert({
                title: response.title,
                content: response.msg,
                type: response.type
              });
          });
        },
        cancelar: function () {}
      }
    });
  });

  $('.js-reverse-expense').on('click', function () {
    var url = $(this).data('url');
    $.confirm({
      title: 'Eliminar ultimo gasto',
      content: '¿deseas eliminar el ultimo gasto?',
      type: 'orange',
      buttons: {
        eliminar: function () {
          $.get(url, function (response) {
              $.alert({
                title: response.title,
                content: response.msg,
                type: response.type
              });
          });
        },
        cancelar: function () {}
      }
    });
  });
});
