
function getUser(){
    console.log("running getUser")
    let xhttp = new XMLHttpRequest();
    

    xhttp.open("GET", "https://24.60.153.154:4443/user?client_id=56", true);
    xhttp.setRequestHeader("Content-type", "application/json")
    xhttp.send();

    xhttp.onreadystatechange = () => {
        console.log(xhttp.readyState)
        if(xhttp.readyState == 4){
            console.log(xhttp.responseText)
            document.getElementById("heya").innerHTML = xhttp.responseText;
        }
    };
}

function postUser(){
    console.log("running postUser")
    let xhttp = new XMLHttpRequest();

    addresses = encodeURIComponent(JSON.stringify([["Home", "5 Eager Road", null, "Milton", "MA", "02186"], ["James", "71 Columbine Road", null, "Milton", "MA", "02186"]]));
    
    console.log(`https://127.0.0.1:4443/user?firstname=Deirdre&lastname=Walsh&email=dmwalsh04@gmail.com&password=sillystring&phone=6179808103&addresses=${addresses}`)
    xhttp.open("POST", `https://127.0.0.1:4443/user?firstname=Deirdre&lastname=Walsh&email=dmwalsh04@gmail.com&password=sillystring&phone=6179808103&addresses=${addresses}`, true);
    xhttp.setRequestHeader("Content-type", "application/json")
    xhttp.send();

    xhttp.onreadystatechange = () => {
        console.log(xhttp.readyState)
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
    
    xhttp.open("PUT", `https://127.0.0.1:4443/user?client_id=86&firstname=Deirdr&lastname=Wals&email=dmwals04@gmail.com&password=a&phone=6178988712&addresses=${addresses}`, true);
    xhttp.setRequestHeader("Content-type", "application/json")
    xhttp.send();

    xhttp.onreadystatechange = () => {
        console.log(xhttp.readyState)
        if(xhttp.readyState == 4){
            console.log(xhttp.responseText)
            document.getElementById("heya").innerHTML = xhttp.responseText;
        }
    };
}

function deleteUser(){
    console.log("running deleteUser")
    let xhttp = new XMLHttpRequest();
    
    xhttp.open("DELETE", "https://127.0.0.1:4443/user?client_id=87", true);
    xhttp.setRequestHeader("Content-type", "application/json")
    xhttp.send();

    xhttp.onreadystatechange = () => {
        console.log(xhttp.readyState)
        if(xhttp.readyState == 4){
            console.log(xhttp.responseText)
            document.getElementById("heya").innerHTML = xhttp.responseText;
        }
    };
}
