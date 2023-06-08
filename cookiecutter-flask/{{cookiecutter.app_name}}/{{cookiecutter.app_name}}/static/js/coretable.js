$(document).ready(function() {
    $('#example').DataTable( {
        "ajax": 'data',
        columns: [
            { data: 'hashtag',
                "render":  function ( data, type, full, meta ) {
                    output = '<a href="/{{cookiecutter.core_table_title|lower}}s/detail/' + full.id + '">' + data + '</a>';
                    return output;
                }     
            },
            { data: 'start',
                "render":  function ( data, type, full, meta ) {
                    return moment.utc(data).local().format("YYYY MMM DD, h:mm a");
                }        
            },
            { data: 'end',
                "render":  function ( data, type, full, meta ) {
                    return moment.utc(data).local().format("YYYY MMM DD, h:mm a");
                }        
             }
        ]
    } );
} );
