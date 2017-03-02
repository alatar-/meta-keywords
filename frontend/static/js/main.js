(function($) {
    "use strict";
    $(document).ready(function() {
        $("#form").bind('submit', function (e) {
            e.preventDefault();

            var url = $('#input-url').val();
            if (!isURL(url)) {
                $('#input-url-group').addClass('has-error');
                return false;
            }

            $('#input-url-group').removeClass('has-error');
            $("#input-url-group div").addClass("hidden");
            $('#form-submit span').addClass('hidden'); // Hide "Process" on submit buttom
            $('#form-submit i').removeClass('hidden'); // Show spinner on submit buttom

            $.ajax({
                type: "GET",
                url: "/count_keywords?url=" + encodeURIComponent(url)
            }).done(function(response) {
                var keywords = response.result || {};
                $('#results-count').text(Object.keys(keywords).length);
                $('#results-group').empty();
                $.each(keywords, function(keyword, count) {
                    var html = '<li class="list-group-item">' + keyword + '<span class="badge">' + count + '</span></li>';
                    $('#results-group').append(html);
                });
                $('#form-submit i').addClass('hidden');
                $('#form-submit span').removeClass('hidden');
                $('#results-panel').removeClass('hidden');
            }).fail(function(error) {
                var errMessage = error.responseJSON.message || "Unknown error occured.";
                $("#input-url-group span").text(errMessage);
                $("#input-url-group div").removeClass("hidden");
                $('#form-submit i').addClass('hidden');
                $('#form-submit span').removeClass('hidden');
            });

            return false;
        });
    });

    function isURL(str) {
        // Source: http://stackoverflow.com/a/14582229
        var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
          '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.?)+[a-z]{2,}|'+ // domain name
          '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
          '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
          '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
          '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
        
        return pattern.test(str);
    }
})($);