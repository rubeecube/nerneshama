$( document ).ready(function() {
    function resize(max_font_size){
        $('.wrapper_flex .box_content .text > span.autofit').each(function(){
            font_size = 20;
            if( $(this).parent().width() < $(this).width() ) {
                font_size = (parseInt($(this).css('font-size')) * $(this).parent().width()/$(this).width())*0.8;
            }else{
                font_size = (Math.floor(parseFloat($(this).css('font-size'))*$(this).parent().width()/$(this).width()))*0.8;
            }
            font_size = Math.min(font_size, max_font_size);
            $(this).css('font-size', font_size + "px" );
        });
    }
    resize(40);
    //setInterval(function() {
        console.log(show_all);
        $.get('ajax_data?json_output', {}, function (ajax_data_text) {
            $.get('ajax_data?html_skeleton&ratio=1', {}, function (skeleton1) {
                $.get('ajax_data?html_skeleton&ratio=2', {}, function (skeleton2) {
                    ajax_data = JSON.parse(ajax_data_text);
                    i = 0;
                    v = 9;
                    setInterval(function() {
                        new_html = "";

                        new_html = skeleton1;

                        var $div = $("<div>").html(new_html);

                        $div.find(".nom_francais").first().html(new Option(ajax_data[v].nom_francais).innerHTML);
                        $div.find(".nom_hebreu").first().html(new Option(ajax_data[v].nom_hebreu).innerHTML);
                        $div.find(".date_niftar_g").first().html(new Option(ajax_data[v].date_niftar_g).innerHTML);
                        $div.find(".date_niftar").first().html(new Option(ajax_data[v].date_niftar).innerHTML);
                        $div.find(".date_hazcara_g").first().html(new Option(ajax_data[v].date_hazcara_g).innerHTML);

                        $('#box_' + i).html($div.html());

                        resize(40);

                        i = (i+1) % 9;
                        v = (v+1) % ajax_data.length;
                        while (!show_all && ajax_data[v].show){
                            v = (v+1) % ajax_data.length;
                        }

                    }, 5000); // Check refresh every 5 sec
                });
            });
        });
    //}, 1800000); // Check refresh every 30 min
});