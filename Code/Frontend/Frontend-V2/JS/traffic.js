window.onload = async function() {
	var trafficTable = document.getElementById("content");
    var trafficData = await getTrafficData();
    trafficTable.appendChild(fillTrafficTable(trafficData));
};

async function getTrafficData() {
    var trafficData = await fetch(`../Testdata/traffic.json`);
	var trafficJson = await trafficData.json();
	return trafficJson;
}

function fillTrafficTable(trafficData) {    
    var tableDiv =  document.getElementById("content");
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
    return tableDiv;
}
