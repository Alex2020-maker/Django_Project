function recalculate_total_values() {
    TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    var _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    var quantity_arr = [];
    var price_arr = [];

    for (var i=0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } 
        else {
            price_arr[i] = 0;
        }
    }

    order_total_quantity = 0;
    order_total_cost = 0;
 
    for (var i=0; i < TOTAL_FORMS; i++) {
        order_total_quantity += quantity_arr[i];
        order_total_cost += quantity_arr[i] * price_arr[i];
    }

    $('.order_total_quantity').html(order_total_quantity.toString());
    $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());

}
 
window.onload = function() {
    $('.order_form input[type="number"]').on('click', recalculate_total_values);
    $('.order_form select').on('change', function(event) {
        var product_id = this.value;
        $.ajax({
            url: "/products/product" + product_id + "/price",
            success: function (data) {
                $('.orderitems-' + product_id + '-price').text(data.result);
            },
        });

    })
    recalculate_total_values();
}

 