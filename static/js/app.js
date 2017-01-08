(function($) {
  'use strict';

  var $dropdown = $("#doc-dropdown-js"),
      $data = $dropdown.data('amui.dropdown'),
      $date = $("#selectM");
  var m = $date.data('sem');
  $("#selectM").datepicker({
      format: 'yyyy-mm',
      'viewMode':'months',
      'minViewMode':'months',
      'autoClose':true
  }).on('changeDate.datepicker.amui', function(event) {
        $(this).text((event.date.getMonth()+1)+'月')
        m = event.date.format('yyyy-MM');
        ac();
        $(this).datepicker('close');
      });
  $(".am-dropdown-content>li:not(.am-dropdown-header,.am-divider,.am-active)",$dropdown).click(function(){
    $(".am-dropdown-content>li.am-active",$dropdown).removeClass('am-active')
    $(this).addClass('am-active');
    ac();
  })

  function ac(k){
    var u = $(".am-dropdown-content>li.am-active",$dropdown).data('data')||$(".am-dropdown-content>li.am-active",$dropdown).text();
    window.location.href="?month="+m+'&trade='+u;
  }
})(jQuery);
/**
 * 时间格式化
 * @param format
 * @returns
 */
Date.prototype.format = function(format){
    var o = {
            "M+" : this.getMonth()+1, //month
            "d+" : this.getDate(), //day
            "h+" : this.getHours(), //hour
            "m+" : this.getMinutes(), //minute
            "s+" : this.getSeconds(), //second
            "q+" : Math.floor((this.getMonth()+3)/3), //quarter
            "S" : this.getMilliseconds() //millisecond
        }
        if(/(y+)/.test(format)) {
            format = format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
        }
        for(var k in o) {
            if(new RegExp("("+ k +")").test(format)) {
                format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}