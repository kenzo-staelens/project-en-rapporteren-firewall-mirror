window.onload = function() {
	fillModulesList();
};

async function fillModulesList() {
    const moduleNames = await getNames("installedModules");
	moduleNames.forEach((element) => {
		var moduleList = document.getElementById('moduleList');
		var moduleToAdd = document.createElement('li');
        moduleToAdd.setAttribute("id", element.name);
		moduleToAdd.setAttribute('onclick', 'switchSelectedModule(this)');
        moduleToAdd.innerText = element.displayName ? element.displayName : element.name;
		moduleList.appendChild(moduleToAdd);
	});
	console.log('filled modules: ' + moduleNames.toString());
}

async function getNames(resource) {
    var names = [];
    try {
        const response = await fetch(`../Testdata/${resource}.json`)
        if(!response.ok) throw "nameList not found"
        const json = await response.json()
        json.data.forEach(item => {
            names.push( 
                {"name": item.name, "displayName": item.displayName ? item.displayName : item.name }
            );
        });
        return names;
    } catch (error) {
        console.error("error retrieving names: " + error);
        return null;
    }
}
//switches the module to the one that the user clicks
function switchSelectedModule(clickedElement) {
	const moduleList = document.getElementById('moduleList');
	const activeElement = moduleList.getElementsByClassName('active')[0];
    if(activeElement) {
        activeElement.classList.remove('active');
    }
	clickedElement.classList.add('active');
    fillModuleSettings(getSelectedModuleName());
	console.log('switched active module to: ' + clickedElement.id);
}

//Determines the module that the user selected
function getSelectedModuleName() {
	const moduleList = document.getElementById('moduleList');
	const selectedModuleName = moduleList.getElementsByClassName('active')[0].id;
	if (selectedModuleName === null) console.error('selectedModule is null');
	return selectedModuleName;
}

//Requests the module data from the server
async function getModuleFromServer(moduleName) {
	//Get request for specific module
    try {
        const response = await fetch(`../Testdata/${moduleName}ModuleSettings.json`)
        if(response.status !== 200) {
            console.error("error retrieving data: " + error);
            response = `{ "name" : "error ${response.status} \nThere was a problem retrieving the data"}`;
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("error retrieving data: " + error);
        return null;
    }
}

async function fillModuleSettings(moduleName) {
    var selectedModule = await getModuleFromServer(moduleName);
    var settingsForm = document.getElementById("moduleSettings");
    settingsForm.innerHTML = "";

    var header = document.createElement("header");
    header.innerHTML = 
    `<h2>${selectedModule.displayName}</h2>
`;
    settingsForm.appendChild(header);

    var moduleSettings = selectedModule.data;
    if(moduleSettings == null) return;
    moduleSettings.forEach(setting => {
        createSettingDiv(setting, settingsForm);
    });

    var footer = document.createElement("footer")
    footer.innerHTML =
    `<button class="bigButton" type="button" onclick=createPostData()>Save</button>
`;
    settingsForm.appendChild(footer);
}

function createSettingDiv(setting, parent) {
    var settingDiv;
    settingDiv = createEmptySetting(setting);
    switch (setting.type) {
        case "bool":
            settingDiv.appendChild(createBoolSettingDiv(setting));
            break;
        case "table":
            settingDiv.appendChild(createTableSettingDiv(setting));
            break;
        case "dropdown":
            settingDiv.appendChild(createDropdownSettingDiv(setting));
            break;
        case "text":
            settingDiv.appendChild(createTextSettingDiv(setting));
            break;
        default:
            console.log("unrecognized type: " + setting.type);
            break;
    }
    parent.appendChild(settingDiv);
}

//creates the containing div and title+description of a setting
function createEmptySetting(setting) {
    var settingDiv = document.createElement("div");
    settingDiv.setAttribute("class", setting.name + "Setting");
    
    var label = document.createElement("h3");
    label.innerText = setting.displayName ? setting.displayName : setting.name;
    settingDiv.appendChild(label);

    if(setting.desc) {
        var desc = document.createElement("p");
        desc.innerText = setting.desc;
        settingDiv.appendChild(desc);
    }

    return settingDiv;
}

function createBoolSettingDiv(setting) {
    var boolSetting = document.createElement("div");
    boolSetting.setAttribute("class", "toggleButton")
    boolSetting.innerHTML = 
`<input type="checkbox" class="checkbox" name="${setting.name}" checked=${setting.data}/>
    <div class="knobs">
        <span></span>
    </div>
    <div class="layer"></div>`;
    return boolSetting;
}

function createTableSettingDiv(setting) {
    var tableDiv = document.createElement("div");
    const columns = Object.keys(setting.data[0])
    tableDivInnerHTML = 
`<table id="${setting.name}">
    <button type="button" class="button_plus" onclick="addRowButton(this)"></button>
    <button type="button" class="button_plus minus" onclick="removeRowButton(this)"></button>
    <thead>
        <tr>
`;
    columns.forEach(header => {
    tableDivInnerHTML += 
`           <th>${header}</th>
`
});
    tableDivInnerHTML += 
`       </tr>
    </thead>
    <tbody>
`;
    var rowIndex = 0;
    setting.data.forEach(row => {
        var tablerow = 
`       <tr>
`;
        columns.forEach(column => {
            tablerow += 
`            <td><input type="text" name="${setting.name}_${rowIndex}_${column}" value="${row[column]}" /></td>
`;
        });
        tablerow += 
`       </tr>
`;
        tableDivInnerHTML += tablerow;
        rowIndex++;
    });
    tableDivInnerHTML += 
`   </tbody>
</table>
`;
    tableDiv.innerHTML = tableDivInnerHTML;
    return tableDiv;
}

function createDropdownSettingDiv(setting) {
    const dropdown = document.createElement("select");
    dropdown.setAttribute("name", setting.name)
    setting.data.forEach(value => {
        const option = document.createElement("option");
        option.setAttribute("value", value);
        option.innerText = value;
        dropdown.appendChild(option)
    })
    return dropdown;
}

function createTextSettingDiv(setting) {
    const text = document.createElement("input");
    text.setAttribute("name", setting.name);
    if(setting.data) {
        text.setAttribute("value", setting.data);
    }
    return text;
}

function addRowButton(caller) {
	const table = caller.parentNode.getElementsByTagName("table")[0];
    const headers = table.getElementsByTagName("th");
	const newInputRow = document.createElement('tr');
    newInputRow.setAttribute('class', 'newInputRow');
    var newInputRowInnerHTML = "";
    var rowIndex = table.getElementsByTagName("tbody")[0].children.length;
    for (let i = 0; i < headers.length; i++) {
        newInputRowInnerHTML += 
`<td>
<input type="text" name="${table.id}_${rowIndex}_${headers[i].innerText}" placeholder="${headers[i].innerText}" />
</td>
`;
    }
	newInputRow.innerHTML = newInputRowInnerHTML;
	table.prepend(newInputRow);
	console.log(`added row`);
}

function removeRowButton(caller) {
	const table = caller.parentNode.getElementsByTagName("table")[0];
	const rows = table.getElementsByClassName('newInputRow');
	if (rows.length === 0) {
        return;
    }
    rows.item(rows.length - 1).remove();
}

async function createPostData() {
    var rawFormData = new FormData(document.getElementById("moduleSettings"));
    console.log(rawFormData);
    const existingSettings = await getModuleFromServer(getSelectedModuleName())
    console.log(existingSettings);
    //var existingKeys = getKeysFromSettings(existingSettings);
    //console.log(existingKeys)
    var formData = {};
    rawFormData.forEach(entry => {
        //convert to good JSON
        
    })

}

/*function getKeysFromSettings(settings) {
    settings.data.forEach(x => {
        var keys = [];
        if(x.type === "table") {
            const tableName = x.displayName ? x.displayName : x.name
            for(var i = 0; i < x.data.Length ; i++){
                keys.push(`${tableName}_${}`);
            }
        }
    })
}*/

async function doPostRequest(moduleName, postData) {
    const response = await fetch(`api/settings/${moduleName}`, {
        method: "POST", 
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
        },
        redirect: "manual", // manual, *follow, error
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    });
    return response.ok; // parses JSON response into native JavaScript objects
}