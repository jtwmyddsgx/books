(function ($) {
    'use strict';

    // $(function() {
    //   var $fullText = $('.admin-fullText');
    //   $('#admin-fullscreen').on('click', function() {
    //     $.AMUI.fullscreen.toggle();
    //   });
    //
    //   $(document).on($.AMUI.fullscreen.raw.fullscreenchange, function() {
    //     $fullText.text($.AMUI.fullscreen.isFullscreen ? '退出全屏' : '开启全屏');
    //   });
    // });
    $("#account-form").validator({
        onValid: function (validity) {
            $(validity.field).closest('.am-u-sm-9').find('.am-alert').hide();
        },
        onInValid: function (validity) {
            var $field = $(validity.field);
            var $group = $field.closest('.am-u-sm-9');
            var $alert = $group.find('.am-alert');
            // 使用自定义的提示信息 或 插件内置的提示信息
            var msg = $field.data('foolish-msg') || this.getValidationMessage(validity);

            if (!$alert.length) {
                $alert = $('<div class="am-alert am-alert-danger"></div>').hide().
                appendTo($group);
            }

            $alert.html(msg).show();
        }
    })
})(jQuery);
