$(function() {
    $('#dbname').on('change', function() {
        $.ajax({
            url: 'handle.php',
            data: {
                dbname: $('#dbname option:selected').val()
            },
            method: 'post',
            success: function(result) {
            	$('#dbname').val('');
                var rst = JSON.parse(result);
                var a = new Array();
                var i = 0;
                //only one row
                rst = rst[0];
                for (var ftn in rst) {
                    a[i] = ftn.split('_OWNS_');
                    a[i].push(rst[ftn]);
                    i++;
                }
                var stbl = showRst(a);
                $('#result').empty().append(stbl);
            },
            error: function(xhr, status, errorThrown) {
                $('#errorResult').empty().
                append("xhr: " + xhr + "<br />").
                append("status: " + status + "<br />").
                append("error message: " + errorThrown);
            }
        });
    });
    function showRst(tblary) {
        var rst = document.getElementById('result');
        var tbl = document.createElement('table');
        var tblhead = document.createElement('thead');
        var tblbody = document.createElement('tbody');

        var thary = ['DB_NAME', 'TABLE_NAME', 'ROW_COUNT'];
        tblhead.appendChild(document.createElement('tr'));
        for (var i = 0; i < 3; i++) {
            var th = document.createElement('th');
            var thtxt = document.createTextNode(thary[i]);
            th.appendChild(thtxt);
            tblhead.appendChild(th);
        }
        for (var j = 0; j < tblary.length; j++) {
            var tr = document.createElement('tr');
            for (var k = 0; k < 3; k++) {
                var td = document.createElement('td');
                var tdtxt = document.createTextNode(tblary[j][k]);
                td.appendChild(tdtxt);
                tr.appendChild(td);
            };
            tblbody.appendChild(tr);
        }
        tbl.setAttribute('border', '1px');
        tbl.setAttribute('id', 'rsttbl');
        tbl.appendChild(tblhead);
        tbl.appendChild(tblbody);
        tbl.className = 'table table-striped';
        return tbl;
    }
});
