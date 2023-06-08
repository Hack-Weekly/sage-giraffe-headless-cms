$(document).ready(function() {
    $.fn.dataTable.moment( 'YYYY MMM DD h:mm a' );
    var postTable = $('#example').DataTable( {
        "ajax": "/{{cookiecutter.core_table_title|lower}}s/all", $('#my-data').data("core_id")),
        columns: [
            { data: 'body',
                "render":  function ( data, type, full, meta ) {
                    payload = JSON.parse(data)

                    output = $('<div/>').text(payload.user.name).html();
                    output += '<br>';
                    output += $('<div/>').text(payload.user.screen_name).html();
                    output += '<br>';
                    output += $('<div/>').append($('<img class="loadingprofile"/>').attr("orig", payload.user.profile_image_url).attr("src", "/static/img/image_899311.gif")).html();

                    return output;
                }        
            },
            { data: 'body',
                "render":  function ( data, type, full, meta ) {
                    payload = JSON.parse(data)
                    output = '';
                    if (payload.entities.media)
                    {
                        //output += '<img src="' + payload.entities.media[0].media_url + ':small" />'
                        output += $('<div/>').append($('<img class="loadingpost"/>').attr("orig", payload.entities.media[0].media_url + ':small').attr("src", "/static/img/image_899310.gif")).html();
                        output += '<br/>'
                    }
                    output += $('<div/>').text(payload.text).html();
                    return output;
                }        
            },
            { data: 'created_at',
                "render":  function ( data, type, full, meta ) {
                    return moment.utc(data).local().format("YYYY MMM DD h:mm a");
                }        
            },
           { data: 'moderationresult',
                "render":  function ( data, type, full, meta ) {
                    payload = JSON.parse(full.body)
                    modReportStatus = modReport(full.moderationstatus, data, full.moderationrequiredmask)
                    if (modReportStatus == 'Censored') {

                    }
                    output = $('<div/>').text(modReportStatus).html();
                    if ($('#my-data').data("view_type").toLowerCase() == 'pending' || $('#my-data').data("view_type").toLowerCase() == 'approved') {
                        output += '<br/><br/>';
                        output += $('<div/>').append($('<button>Censor</button>').attr(
                                            {
                                                "id": payload.id_str, 
                                                "class":"btn btn-danger button-censor",
                                                "title": "Censor Post"
                                            }
                                    )).html();
                    } else if ($('#my-data').data("view_type").toLowerCase() == 'censored') {
                        output += '<br/><br/>';
                        output += $('<div/>').append($('<button>Approve</button>').attr(
                                            {
                                                "id": payload.id_str, 
                                                "class":"btn btn-primary button-approve",
                                                "title": "Censor Post"
                                            }
                                    )).html();
                    }
                    return output;
                }                  
            }

        ],
        "createdRow": function ( row, data, index ) {

    
        },
        "rowCallback": function ( row, data, index ) {

            modReportStatus = modReport(data.moderationstatus, data.moderationresult, data.moderationrequiredmask)

            if ( modReportStatus == 'Censored') {
                $(row).addClass('danger');
            }
            if ( modReportStatus == 'Approved') {
                $(row).addClass('success');
            }

            var imgprofile = $('img.loadingprofile', row);
     
            imgprofile.attr('src', imgprofile.attr('orig'));
            imgprofile.removeClass('loadingprofile');

            var imgpost = $('img.loadingpost', row);
     
            imgpost.attr('src', imgpost.attr('orig'));
            imgpost.removeClass('loadingpost');            
    
        },        
        "order": [[ 2, "desc" ]]
    });





    activaTab($('#my-data').data("view_type"), $('#my-data').data("core_id"));

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $('meta[name=csrf-token]').attr('content'))
            }
        }
    })
});

function openModal() {
        document.getElementById('modal').style.display = 'block';
        document.getElementById('fade').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('fade').style.display = 'none';
}

function modReport(status, result, mask)
{
    status = parseInt(status)
    mask = parseInt(mask)
    result = parseInt(result)
    if ((mask & status & result) != (mask & status)) {
        return "Censored";
    }
    if ((mask & status) != mask ) {
        return "Pending";
    }
    if ((mask & status & result) == mask ) {
        return "Approved";
    }

}




(function($) {

$.fn.dataTable.moment = function ( format, locale ) {
    var types = $.fn.dataTable.ext.type;

    // Add type detection
    types.detect.unshift( function ( d ) {
        // Null and empty values are acceptable
        if ( d === '' || d === null ) {
            return 'moment-'+format;
        }

        return moment( d.replace ? d.replace(/<.*?>/g, '') : d, format, locale, true ).isValid() ?
            'moment-'+format :
            null;
    } );

    // Add sorting method - use an integer for the sorting
    types.order[ 'moment-'+format+'-pre' ] = function ( d ) {
        return d === '' || d === null ?
            -Infinity :
            parseInt( moment( d.replace ? d.replace(/<.*?>/g, '') : d, format, locale, true ).format( 'x' ), 10 );
    };
};

}(jQuery));