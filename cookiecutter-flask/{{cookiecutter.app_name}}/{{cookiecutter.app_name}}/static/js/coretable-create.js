$(function () {
    $('#starttimepicker').datetimepicker();
    $('#endtimepicker').datetimepicker();

    $('#event-create').on('submit', function(e){
        e.preventDefault();
        var localtime = moment($('#starttime').val(), "MM/DD/YYYY h:mm a");
        $('#starttime').val(localtime.utc().toISOString());
        localtime = moment($('#endtime').val(), "MM/DD/YYYY h:mm a");
        $('#endtime').val(moment(localtime).utc().toISOString());
        this.submit();
        
    });
});