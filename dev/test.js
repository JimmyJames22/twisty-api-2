
function getUser(){
    console.log("running getUser")
    let xhttp = new XMLHttpRequest();
    

    xhttp.open("GET", "https://twistyroads.tk/user?email=jameselliottmillington@gmail.com&password=sillystrin", true);
    xhttp.setRequestHeader("Content-type", "application/json")
    xhttp.send();

    xhttp.onreadystatechange = () => {
        if(xhttp.readyState == 4){
            console.log(xhttp.responseText)
            document.getElementById("heya").innerHTML = xhttp.responseText;
        }
    };
}

function postUser(){
    console.log("running postUser")
    let xhttp = new XMLHttpRequest();

    // addresses = encodeURIComponent(JSON.stringify([["Home", "5 Eager Road", null, "Milton", "MA", "02186"], ["James", "71 Columbine Road", null, "Milton", "MA", "02186"]]));
    addresses = encodeURIComponent(JSON.stringify([["Home", "71 Columbine Road", null, "Milton", "MA", "02186"], ["School", "170 Centre Street", null, "Milton", "MA", "02186"]]));
    
    console.log(`https://twistyroads.tk/user?firstname=Deirdre&lastname=Walsh&email=dmwalsh04@gmail.com&password=sillystring&phone=6179808103&addresses=${addresses}`)
    // xhttp.open("POST", `https://twistyroads.tk/user?firstname=Deirdre&lastname=Walsh&email=dmwalsh04@gmail.com&password=sillystring&phone=6179808103&addresses=${addresses}`, true);
    xhttp.open("POST", `https://twistyroads.tk/user?firstname=James&lastname=Millington&email=jameselliottmillington@gmail.com&password=sillystring&phone=6178988712&addresses=${addresses}`, true);
    xhttp.setRequestHeader("Content-type", "application/json")
    xhttp.send();

    xhttp.onreadystatechange = () => {
        if(xhttp.readyState == 4){
            console.log(xhttp.responseText)
            document.getElementById("heya").innerHTML = xhttp.responseText;
        }
    };
}
  
function putUser(){
    console.log("running changeUser")
    let xhttp = new XMLHttpRequest();

    addresses = encodeURIComponent(JSON.stringify([["Deirdre", "5 Eager Road", null, "Milton", "MA", "02186", "ADD"], ["Home", "DELETE"], ["James", "DELETE"]]));
    
    xhttp.open("PUT", `https://twistyroads.tk/user?client_id=86&firstname=Deirdr&lastname=Wals&email=dmwals04@gmail.com&password=a&phone=6178988712&addresses=${addresses}`, true);
    xhttp.setRequestHeader("Content-type", "application/json")
    xhttp.send();

    xhttp.onreadystatechange = () => {
        if(xhttp.readyState == 4){
            console.log(xhttp.responseText)
            document.getElementById("heya").innerHTML = xhttp.responseText;
        }
    };
}

function deleteUser(){
    console.log("running deleteUser")
    let xhttp = new XMLHttpRequest();
    
    xhttp.open("DELETE", "https://twistyroads.tk/user?client_id=86", true);
    xhttp.setRequestHeader("Content-type", "application/json")
    xhttp.send();

    xhttp.onreadystatechange = () => {
        if(xhttp.readyState == 4){
            console.log(xhttp.responseText)
            document.getElementById("heya").innerHTML = xhttp.responseText;
        }
    };
}

function getRoute(){
    console.log("running getRoute")
    let xhttp = new XMLHttpRequest();
    
    xhttp.open("GET", "https://twistyroads.tk/route?client_id=87&origin=1431%20Brush%20Hill%20Road&destination=71%20Columbine%20Road", true);
    xhttp.setRequestHeader("Content-type", "application/json")
    xhttp.send();

    xhttp.onreadystatechange = () => {
        if(xhttp.readyState == 4){
            console.log(JSON.parse(xhttp.responseText))
        }
    };
}
