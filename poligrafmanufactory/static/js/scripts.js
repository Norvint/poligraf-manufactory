
var month = new Array();
month[0] = "Январь";
month[1] = "Февраль";
month[2] = "Март";
month[3] = "Апрель";
month[4] = "Май";
month[5] = "Июнь";
month[6] = "Июль";
month[7] = "Август";
month[8] = "Сентябрь";
month[9] = "Октябрь";
month[10] = "Ноябрь";
month[11] = "Декабрь";

function updateTable() {
    var data = {page: {{ object_list.number }}}
    var tbodyRef = document.getElementById('shipmentsTable').getElementsByTagName('tbody')[0];
    var new_tbody = document.createElement('tbody');
    tbodyRef.parentNode.replaceChild(new_tbody, tbodyRef)

    // Append a text node to the cell
    //   var newText = document.createTextNode('new row');
    //   newCell.appendChild(newText);
   $.ajax({
       type: 'GET',
       data: data,
       url: '/warehouse/api/shipments/',
       success: function(res){
         for (const i in res.results) {
              var newRow = new_tbody.insertRow();
              var nameCell = newRow.insertCell();
              nameCell.innerHTML += res.results[i].name;
              var numberCell = newRow.insertCell();
              numberCell.innerHTML += res.results[i].number;
              var dateCell = newRow.insertCell();
              date = new Date(res.results[i].date);
              dateCell.innerHTML += date;
              var pannedDateCell = newRow.insertCell();
              var plannedDate = new Date(res.results[i].planned_date);
              var plannedDateString = `${plannedDate.getDate()}.${month[plannedDate.getMonth()]}`
              pannedDateCell.innerHTML += plannedDateString;
              var orderCell = newRow.insertCell();
              orderCell.innerHTML += "Заказ №" + res.results[i].order.number;
              var orderReadyCell = newRow.insertCell();
              if (res.results[i].order_is_ready) {
                 orderReadyCell.innerHTML += "Готов"
                 }
              else
              {   orderReadyCell.innerHTML += "Не готов" };

         };
       },
       error: function(error) {
           callbackErr(error,self)
       }
   })
}
setInterval(updateTable, 10000);