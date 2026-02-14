// import express, { Request, Response } from "express";
import express from "express"; // runtime import
import type { Request, Response } from "express"; // types only


// ==== Type Definitions, feel free to add or modify ==========================
interface cookbookEntry {
  name: string;
  type: string;
}

interface requiredItem {
  name: string;
  quantity: number;
}

interface recipe extends cookbookEntry {
  requiredItems: requiredItem[];
}

interface ingredient extends cookbookEntry {
  cookTime: number;
}

interface RecipeItem {
  name: string;
  quantity: number;
}

// =============================================================================
// ==== HTTP Endpoint Stubs ====================================================
// =============================================================================
const app = express();
app.use(express.json());
export default app;

// Store your recipes here!
const cookbook: any = null;
let ingredient: Map<String, number> = new Map();
let recipe: Map<String, String> = new Map();

// Task 1 helper (don't touch)
app.post("/parse", (req:Request, res:Response) => {
  const { input } = req.body;

  const parsed_string = parse_handwriting(input)
  if (parsed_string == null) {
    res.status(400).send("this string is cooked");
    return;
  } 
  res.json({ msg: parsed_string });
  return;
  
});

// [TASK 1] ====================================================================
// Takes in a recipeName and returns it in a form that 
const parse_handwriting = (recipeName: string): string | null => {
  // TODO: implement me
  let retString: string = ""
  let start: boolean = true

  for (const char of recipeName) {
    const Alpha = /^[a-zA-Z]$/.test(char)
    if (Alpha) {
      if (start) {
        retString += char.toUpperCase()
        start = false
      } else {
        retString += char.toLocaleLowerCase()
      }
    } else if (char === "-" || char === "_" || char === " ") {
      if (!start) { 
        retString += " "
      }
      start = true
    }

  }
  if (retString.length === 0 ) {
    return null
  }
  return retString
}

// [TASK 2] ====================================================================
// Endpoint that adds a CookbookEntry to your magical cookbook
app.post("/entry", (req:Request, res:Response) => {
  const entry = req.body
  let type = entry.type 
  let name = entry.name 
  console.log(name)
  
  if (ingredient.has(name) || recipe.has(name)) {
    res.status(400).send("entry already exists")
    return
  }

  if (type === "recipe") {
    let requirements = entry.requiredItems
    for (let items of requirements) {
      if (items.length > 2) {
        res.status(400).send("too many ingredient parameters")
        return
      }
    }

    recipe.set(name, requirements)

  } else if (type == "ingredient") {
     let time = entry.cookTime
     if (time < 0) {
      res.status(400).send("invalid cooktime")
      return
     }
     if (time === 0) {
      time = -1
     }
     ingredient.set(name, time)

  } else {
    res.status(400).send("invalid type")
    return
  }

  res.status(200).send("added onto the database!")
});

// [TASK 3] ====================================================================
// Endpoint that returns a summary of a recipe that corresponds to a query name
app.get("/summary", (req:Request, res:Request) => {
  let name: string = req.query.name
  let totalTime: number = 0;

  let items: Map<string, number> = new Map()
  let recipes = []

  if (!recipe.has(name)) {
    res.status(400).send(`hello: ${name}`)
    return
  }

  console.log(recipe.get(name))
  for (let item of recipe.get(name) as unknown as RecipeItem[]) {
    if (recipe.has(item.name)) {
      recipes.push([item.name, item.quantity])
    }
    else {
      items.set(item.name, item.quantity)
    }
  }
  
  while (recipes.length != 0) {
    let something = recipes[0];

    let ing = something[0];
    let amount = something[1];
    for (let item of recipe.get(ing)) {
      let json = JSON.parse(item)
      if (recipe.has(json.name)) {
        recipes.push([json.name, amount * json.quantity])
      }
      else {
        items.set(json.name, json.quantity * amount)
      }
    }
  }
  
  let array = []

  for (const keys of Array.from(items.keys())) {
    if (! ingredient.has(keys)) {
      res.status(400).send(`${keys} does not exist`)
      return
    }
    if (ingredient.get(keys) === -1) {
      ingredient.set(keys, 0) 
    }
    totalTime += items.get(keys) * ingredient.get(keys)
    array.push({"name": keys, "quantity": items.get(keys)})
  }

  let output = {
		"name": name,
		"cookTime": totalTime,
		"ingredients": array
	}

  res.status(200).send(output)

});

// =============================================================================
// ==== DO NOT TOUCH ===========================================================
// =============================================================================
const port = 8080;
app.listen(port, () => {
  console.log(`Running on: http://127.0.0.1:8080`);
});
