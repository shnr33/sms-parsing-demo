$(document).ready(function(){

    $('body').on('click', '.sender-details', function () {
        $("#detailsModal #senderDetails").html("");
        var detailsTable = "<table class='detailsTable table table-bordered table-condensed'><tbody>";
        detailsTable += "<tr><td class='modal-section-head' colspan='2'>Sender Details</td></tr>";
        detailsTable += "<tr><td>Sender</td><td>" + rawData[$(this).attr("sender")].sender  + "</td></tr>";
        detailsTable += "<tr><td>Sender Service Type</td><td>" + rawData[$(this).attr("sender")].sender_type  + "</td></tr>";
        detailsTable += "</tbody></table>";

        detailsTable += "<table class='detailsTable table table-bordered table-condensed'><tbody>";
        $.each(rawData[$(this).attr("sender")].messages, function(key, message) {
            detailsTable += "<tr><td class='modal-section-head' colspan='2'>SMS - "+ message.sms_id+"</td></tr>";
            detailsTable += "<tr><td>Datetime</td>" + "<td>" + message.sms_datetime + "</td></tr>";
            detailsTable += "<tr><td>SMS Type</td>" + "<td>" + message.msg_type + "</td></tr>";
            detailsTable += "<tr><td>SMS</td>" + "<td>" + message.sms_text + "</td></tr>";
        })

        detailsTable += "</tbody></table>";
        $("#detailsModal #senderDetails").html(detailsTable);
        $("#detailsModal").modal();
    });

})

var rawData = {};

function showDashboardTable(sms_data) {

    var columns = [
            { "name": "id", "title": "Sl. No.", "breakpoints": "xs", "type": "number"},
            { "name": "sender", "title": "Sender ID/Number", "type": "text"},
            { "name": "sender_type", "title": "Sender Service Type", "type": "text"},
            { "name": "total_sms", "title": "Total number of SMS", "breakpoints": "xs", "type": "number", "sort_initial":"true"},
            { "name": "tx_sms", "title": "No. of Tx SMSs", "breakpoints": "xs sm", "type": "number"},
            { "name": "promotional_sms", "title": "No. of Promotional SMSs", "breakpoints": "xs sm md", "type": "number"}
        ]

    var rows = []
    $.each(sms_data, function(index, data) {
        rawData[data.sender] = {'sender': data.sender, 
                                'sender_type': data.sender_service_type, 
                                'messages': data.messages}
        rows.push({
            "id": data.id, 
            "sender": "<a href='#' class='sender-details' sender='"+ data.sender + "'>" + data.sender + "</a>", 
            "sender_type": data.sender_service_type, 
            "total_sms": data.total_sms, 
            "tx_sms": data.total_tx_sms, 
            "promotional_sms": data.total_promo_sms
        })
    })

    $('.table').footable({
        "columns": columns,
        "rows": rows
    });
}
