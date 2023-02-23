//import retObj from '../retrieveTest';
export function userInput(){
        const fs = require('fs');
        // example {id:1592304983049, title: 'Deadpool', year: 2015}
        let inputs = []
        let input = {
            region: document.getElementById('Region').value,
            startYear: document.getElementById('Start').value,
            endYear: document.getElementById('End').value
        }
        inputs.push(input);
        document.forms[0].reset();

        let jsonObject = JSON.stringify(inputs);
        localStorage.setItem('inputList', jsonObject);

        let ret = localStorage.getItem("inputList")
        alert(ret)
          
//          const jsonString = JSON.stringify(data);
//          const filePath = 'user.txt'; // specify the full path to the file

//        fs.writeFile(filePath, jsonString, (err) => {
//        if (err) {
//                console.log('Error writing file:', err);
//            } else {
//               console.log('File written successfully!');
//            }
//        });
        
    
        //retObj(ret)
        // Retrieve the JSON object from local storage
        //const ret_parse = JSON.parse(ret);

        // Convert the JSON object to a string
        //const jsonContent = JSON.stringify(ret_parse);

        // Create a new Blob object containing the JSON data
        //const blob = new Blob([jsonContent], {type: 'application/json'});

        // Create a new URL object and a new file
        //const url = URL.createObjectURL(blob);
        //const a = document.createElement('a');
        //a.href = url;
        //a.download = 'myJSONFile.json';

        // Programmatically click the <a> element to trigger the download
        //document.body.appendChild(a);
        //a.click();

        // Revoke the URL object to free up memory
        //URL.revokeObjectURL(url);

}

