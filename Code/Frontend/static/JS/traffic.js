window.onload = async function() {
	var trafficTable = document.getElementById("content");
    var trafficData = await getTrafficData();
    fillTrafficTable(trafficData)
    //trafficTable.appendChild(fillTrafficTable(trafficData));
};

async function getTrafficData() {
    var trafficData = await fetch(`api/Traffic`);
	var trafficJson = await trafficData.json();
	return trafficJson;
}

function fillTrafficTable(trafficData) {    
    /*var tableDiv =  document.getElementById("content");
    tableDivInnerHTML = 
`<h3>${trafficData.displayName}</h3>
<table>
    <thead>
        <tr>
`;
    trafficData.traffic.value.headers.forEach(header => {
        tableDivInnerHTML += 
`           <th>${header.value}</th>
`
    });
    tableDivInnerHTML += 
`       </tr>
    </thead>
    <tbody>
`;
    trafficData.traffic.value.rows.forEach(row => {
        var tablerow = 
`       <tr>
`;
        row.data.forEach(cell => {
            tablerow += 
`            <td>${cell.value}</td>
`;
        });
        tablerow += 
`       </tr>
`;
        tableDivInnerHTML += tablerow;
    });
    tableDivInnerHTML += 
`   </tbody>
</table>
`;
    tableDiv.innerHTML = tableDivInnerHTML;
    return tableDiv;*/
    var tableDiv =  document.getElementById("content");
    var header = `<h3>${trafficData.displayName}</h3>`
    var tableHead = `<table><thread><tr>`
    var tableEnd = "</tbody></table>"
    var tableRows=""
    Object.keys(trafficData.data[0].data[0]).forEach(key=> {
        tableHead+=`<th>${key}</th>`
    })
    tableHead+="</tr></thead><tbody>"

    trafficData.data[0].data.forEach(row=>{
    tableRows+="<tr>"
    Object.keys(row).forEach(rowkey=>{
        tableRows += `<td>${row[rowkey]}</td>`
    })
    tableRows+="</tr>"
})

tableDiv.innerHTML = header+tableHead+tableRows+tableEnd
}
