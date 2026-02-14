const url3 = "http://127.0.0.1:8080/summary?name=Skibidi%20Spaghetti";
const url2 = "http://127.0.0.1:8080/entry"
// very basic testing (same as the last one on python)
async function fetchSummary0() {
    try {
      const requestBody = {
        "type": "recipe",
        "name": "Skibidi Spaghetti",
        "requiredItems": [{
            "name": "Meatball",
            "quantity": 3
            },{
            "name": "Pasta",
            "quantity": 1
            },{
            "name": "Tomato",
            "quantity": 2
    }]};
    const requestBody2 = {
        "type": "ingredient",
        "name": "Meatball",
        "cookTime": 2
    };
    const requestBody3 = {
        "type": "ingredient",
        "name": "Tomato",
        "cookTime": 2
    };
    const requestBody4 = {
        "type": "ingredient",
        "name": "Pasta",
        "cookTime": 2
    };

    const requestBody6 = {
      "type": "ingredient",
      "name": "meatball",
      "cookTime": 2
  };
      
  
      const response = await fetch(url2, {
        method: "POST", // or 'PUT' if updating
        headers: {
          "Content-Type": "application/json", // tells the server it's JSON
        },
        body: JSON.stringify(requestBody), // convert JS object to JSON string
      });
      const response2 = await fetch(url2, {
        method: "POST", // or 'PUT' if updating
        headers: {
          "Content-Type": "application/json", // tells the server it's JSON
        },
        body: JSON.stringify(requestBody2), // convert JS object to JSON string
      });
      const response3 = await fetch(url2, {
        method: "POST", // or 'PUT' if updating
        headers: {
          "Content-Type": "application/json", // tells the server it's JSON
        },
        body: JSON.stringify(requestBody3), // convert JS object to JSON string
      });
      const response4 = await fetch(url2, {
        method: "POST", // or 'PUT' if updating
        headers: {
          "Content-Type": "application/json", // tells the server it's JSON
        },
        body: JSON.stringify(requestBody4), // convert JS object to JSON string
      });

      const response5 = await fetch(url3); // fetch is built-in in Node 18+
      console.log("Status code:", response5.status);
    // const data = await response5.json(); // parse JSON response5
    console.log("Response5 body:", response5);

    const response6 = await fetch(url2, {
      method: "POST", // or 'PUT' if updating
      headers: {
        "Content-Type": "application/json", // tells the server it's JSON
      },
      body: JSON.stringify(requestBody6), // convert JS object to JSON string
    });
  
      
    } catch (err) {
      console.error("Error:", err);
    }
  }


fetchSummary0();
