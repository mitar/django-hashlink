function hashlink(hashlink_url) {
    (function ($) {
        $(window).hashchange(function (event, data) {
            if (data.hashlink) {
                // This is a hashlink-invoked change so state is already set
                return;
            }

            var oldHash = data.oldHash;
            var currentHash = data.currentHash;

            if (currentHash) {
                $.post(hashlink_url, {'previous': oldHash || '', 'hashlink': currentHash}, function (data, textStatus, jqXHR) {
                    $(window).trigger('hashlink.state', data);
                });
            }
        });

        $.fn.hashlink = function (state) {
            $.post(hashlink_url, {'previous': $(window).currenthash(), 'state': JSON.stringify(state)}, function (data, textStatus, jqXHR) {
                $(window).updatehash(data.hashlink, {'hashlink': true, 'state': state});
            });

            return this;
        };

    })(jQuery);
}