// SideNav Initialization
$(".button-collapse").sideNav();

var container = document.querySelector('.custom-scrollbar');
Ps.initialize(container, {
    wheelSpeed: 2,
    wheelPropagation: true,
    minScrollbarLength: 20
});

$(document).ready(function () {
    // Material Select Initialization
    $('.mdb-select').material_select();
    // Data Picker Initialization
    $('.datepicker').pickadate({
        format: 'yyyy-mm-dd'
    });
    // Time Picker Initialization
    $('.timepicker').pickatime({
        // 12 or 24 hour
        twelvehour: false
    });
    // Tooltips Initialization
    $('[data-toggle="tooltip"]').tooltip();
    $('.modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var modal = $(this);
        modal.find('.modal-header .heading').text(button.data('title'));
        modal.find('.modal-body .col-9 p').text(button.data('message'));
        modal.find('.confirm').one('click', function () {
            $.ajax({
                method: button.data('method'),
                url: button.data('url')
            }).done(function () {
                modal.modal('hide');
                location.reload();
            }).fail(function (jqXHR) {
                modal.modal('hide');
                toastr.error(jqXHR.responseJSON['detail']);
            });
        });
    });
    $('.sticky').sticky({
        topSpacing: 90,
        zIndex: 2,
    });
    $('.list-group.checked-list-box .list-group-item').each(function () {

        // Settings
        var $widget = $(this),
            $checkbox = $('<input type="checkbox" class="hidden" />'),
            color = ($widget.data('color') ? $widget.data('color') : "primary"),
            style = ($widget.data('style') == "button" ? "btn-" : "list-group-item-"),
            settings = {
                on: {
                    icon: 'glyphicon glyphicon-check'
                },
                off: {
                    icon: 'glyphicon glyphicon-unchecked'
                }
            };

        $widget.css('cursor', 'pointer');
        $widget.append($checkbox);

        // Event Handlers
        $widget.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });


        // Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $widget.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $widget.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$widget.data('state')].icon);

            // Update the button's color
            if (isChecked) {
                $widget.addClass(style + color + ' active');
            } else {
                $widget.removeClass(style + color + ' active');
            }
        }

        // Initialization
        function init() {
            if ($widget.data('checked') == true) {
                $checkbox.prop('checked', !$checkbox.is(':checked'));
            }

            updateDisplay();

            // Inject the icon if applicable
            if ($widget.find('.state-icon').length == 0) {
                $widget.prepend('<span class="state-icon ' + settings[$widget.data('state')].icon + '"></span>');
            }
        }
        init();
    });

    $('.get-checked-data').on('click', function (event) {
        event.preventDefault();
        var checkedItems = [],
            button = $(this),
            modal = $(this).closest('.modal');
        var fields = $('form', modal).serializeArray().reduce(function (map, obj) {
            if (obj.value)
                map[obj.name] = obj.value;
            return map;
        }, {});
        $(".checked-list-box .list-group-item.active").each(function (idx, item) {
            checkedItems.push(Object.assign({}, fields, {
                id: $('input:checkbox:first', item).val()
            }));
        });
        $.ajax({
            method: button.data('method'),
            url: button.attr('href'),
            data: JSON.stringify(checkedItems),
            contentType: 'application/json'
        }).done(function (data) {
            modal.modal('hide');
            location.reload();
        }).fail(function (jqXHR) {
            modal.modal('hide');
            toastr.error(jqXHR.responseJSON['detail']);
        });
    });
});

// Acquiring the token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

// Setting the token on the AJAX request
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// Notifications
var notificationsSocket = new WebSocket('wss://' + window.location.host + '/ws/notifications/');

notificationsSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    toastr.info(message);
};

notificationsSocket.onclose = function (e) {
    console.error('Notifications socket closed unexpectedly');
};
