async function fillModuleSettings() {
    var settingsForm = document.getElementById("moduleSettingsForm");
    settingsForm.innerHTML = "";
	var selectedModule = await getSelectedModule();
    var header = document.createElement("div");
    header.innerHTML = 
    `<h2>${selectedModule["displayName"]}</h2>
`;
    settingsForm.appendChild(header);

    var moduleSettings = selectedModule.settings;
    if(moduleSettings == null) return;
    moduleSettings.forEach(setting => {
        var settingDiv;
        switch (setting.type) {
            case "bool":
                settingDiv = createBoolSettingDiv(setting);
                break;
            case "table":
                settingDiv = createTableSettingDiv(setting);
                break;
            case "dropdown":
                settingDiv = createDropdownSettingdiv(setting);
                break;
            default:
                console.log("unrecognized type: " + setting.type);
                break;
        }
        settingsForm.appendChild(settingDiv);
    });

}

function createBoolSettingDiv(setting) {
    var boolDiv = document.createElement("div");
    boolDiv.setAttribute("class", "boolSetting")
    boolDiv.innerHTML = 
`<label for="enableModule">${setting.name}</label>
<div class="toggleButton">
    <input type="checkbox" class="checkbox" />
    <div class="knobs">
        <span></span>
    </div>
    <div class="layer"></div>
</div>`;
    return boolDiv;
}

function createTableSettingDiv(setting) {
    var tableDiv = document.createElement("div");
    tableDiv.setAttribute("class", "tableSetting");
    tableDivInnerHTML = 
`<h3>${setting.name}</h3>
<table>
    <thead>
        <tr>
`;
setting.value.headers.forEach(header => {
tableDivInnerHTML += 
`           <th>${header.value}</th>
`
});
tableDivInnerHTML += 
`       </tr>
    </thead>
    <tbody>
`;
setting.value.rows.forEach(row => {
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
<button type="button" class="button_plus" onclick="addRowButton(this)"></button>
<button type="button" class="button_plus minus" onclick="removeRowButton(this)"></button>
`;
    tableDiv.innerHTML = tableDivInnerHTML;
    return tableDiv;
}



function addRowButton(caller) {
	var table = caller.parentNode.children[1];
    var headers = table.getElementsByTagName("th");
	var newInputRow = document.createElement('tr');
    newInputRow.setAttribute('class', 'newInputRow');
    var newInputRowInnerHTML = "";
    for (let i = 0; i < headers.length; i++) {
        newInputRowInnerHTML += 
`<td>
    <input type="text" placeholder="${headers[i].innerText}">
</td>
`;
    }
	newInputRow.innerHTML = newInputRowInnerHTML;
	table.appendChild(newInputRow);
	console.log(`added row`);
}

function removeRowButton(caller) {
	var table = caller.parentNode.children[1];
	var rowes = table.getElementsByClassName('newInputRow');
	if (rowes.length === 0) {
        return;
    }
    rowes.item(rowes.length - 1).remove();
}

async function getSelectedModule() {
	var moduleName = getSelectedModuleName();
	//Get request for specific module
	var moduleData = await fetch(`../../Testdata/${moduleName}ModuleSettings.json`)
    .then(response => {
        if(response.status !== 200) {
            return JSON.parse(`{ "name" : "error ${response.status}", "displayName" : "There was a problem retrieving the module"}`);
        }
        return response.json().then(data => {return data;});
    }).catch(error => { console.error("error: " + error); return null; })
	console.log('object: ' + moduleData);
	return moduleData;
}