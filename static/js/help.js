/**
 * Created by sina on 1/31/14.
 */

 $(document).ready(function () {
        $(".Sina_help").each(function () {
            $(this).hide();
        })

        icons = $(".help.icon")
        icons.each(function () {
                    x = this;
                    num = this.getAttribute('help-id');
                    id = "#msg_div" + num;
                    var help = $(id)
                    $(this).hover(function () {
                        help.show();
                        var h = help[0];
                        h.style.display = 'inline-table';
                    }, function () {
                        help.hide()
                    })
                }
        );
    });
