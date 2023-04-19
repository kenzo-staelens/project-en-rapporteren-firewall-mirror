function xhrreq(content, apitoken, onready) {
  var url = "/api";
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      console.log(xhr.status);
      console.log(xhr.responseText);
      var j = JSON.parse(xhr.responseText);
      //console.log(j)
      onready(j)
    }
  };
  content["apitoken"]=encodeURIComponent(apitoken)
  content = JSON.stringify(content)
  //var data = '{"apitoken":"'+encodeURIComponent(apitoken)+'","setting":"value"}';
  xhr.send(content);
}
