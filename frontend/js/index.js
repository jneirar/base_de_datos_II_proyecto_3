document.getElementById('form').onsubmit = function(e){
    e.preventDefault();
    const filename = e.target.files[0];
    console.log(filename);
    fetch('/afterUpload/' + filename.name,{
        method : 'GET',
        headers: {
            'Content-Type' : 'application/json'
        }
    })
    .then(response =>{
        response.json().then(data => ({
            data: data
        }) )
        

    })
    .then(text =>{
        console.log("GET: ");
        console.log(text.message);
        document.write("<img src = " + text.message + ">")
    })
}
