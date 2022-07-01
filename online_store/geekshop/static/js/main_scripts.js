window.onload = function(event) {
    var link = window.location.pathname + 'ajax/';
    var link_array = link.split('/');
    if (link_array[2] == 'category') {
        $.ajax({
            url: link,
            success: function (data) {
                $('.products_list').html(data);
            },
        });
        event.preventDefault();
    }
}
