(function($) {
    "use strict";
    $(document).ready(function() {

        $("#form").bind('submit', function (e) {
            e.preventDefault();

            var url = $('#form-url input').val();
            if (!isURL(url)) {
                $('#form-url').addClass('has-error');
                return false;
            }
            
            DOM.showProcessingSpinner();
            $.ajax({
                type: "GET",
                url: "/count_keywords?url=" + encodeURIComponent(url)
            }).done(function(response) {
                var keywords = response.result || {};
                var keywordsCount = Object.keys(keywords).length;
                
                DOM.showResultsPanel(keywordsCount);
                $.each(keywords, function(keyword, count) {
                    DOM.appendResult(keyword, count);
                });
            }).fail(function(error) {
                var errMessage = error.responseJSON.message || "Unknown error occured.";
                DOM.showAlert(errMessage);
            }).complete(function() {
                DOM.hideProcessingSpinner();
            });

            return false;
        });

        var DOM = {
            clearPage: function() {
                $('#form-url').removeClass('has-error');
                $("#form-alert-box").addClass("hidden");
                $('#results-panel').addClass('hidden');
            },

            showProcessingSpinner: function() {
                this.clearPage();
                $('#form-submit span').addClass('hidden'); // Hide "Process" on submit buttom
                $('#form-submit i').removeClass('hidden'); // Show spinner on submit buttom
            },

            hideProcessingSpinner: function() {
                $('#form-submit span').removeClass('hidden');
                $('#form-submit i').addClass('hidden');
            },

            showAlert: function(errMessage) {
                $("#form-alert-box span").text(errMessage);
                $("#form-alert-box").removeClass("hidden");
            },

            showResultsPanel: function(resultsCount) {
                $('#results-count').text(resultsCount);
                $('#results-group').empty();
                $('#results-panel').removeClass('hidden');
            },

            appendResult: function(keyword, count) {
                var li = createElement('li', 'list-group-item');
                li.appendChild(document.createTextNode(keyword));
                li.appendChild(createElement('span', 'badge', count));
                $('#results-group').append(li);
            }

        };

    });

    function createElement(type, className, value) {
        var elem = document.createElement(type);
        elem.className = className;
        if (value !== undefined) {
            elem.appendChild(document.createTextNode(value));
        }
        return elem;
    }

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