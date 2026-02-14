#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# added libraries
from collections import defaultdict
import json
import unittest

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int

 
# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = None
recipe = defaultdict(str)
ingredient = defaultdict(str)

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that is legible as per spec
def parse_handwriting(recipeName: str) -> Union[str , None]:
	# TODO: implement me
	finalString = ""
	first = True

	for character in recipeName:
		if character.isalpha():
			if first:
				finalString += character.upper()
			else:
				finalString += character.lower()
			first = False

		elif character == '-' or character == '_' or character == ' ':
			if not first:
				finalString += " "
			first = True

	return finalString if len(finalString) > 0 else None


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():

	entry = request.get_json()

	type = entry["type"]
	name = entry["name"]
	if recipe[name] or ingredient[name]:
		return 'entry already exists', 400

	if type == 'recipe':
		requirements = entry["requiredItems"]
		for items in requirements:
			if len(items) > 2:
				return 'too many elements within requiredItems', 400
		
		recipe[name] = requirements

	elif type == 'ingredient':
		time = entry['cookTime'] 
		if time < 0:
			return 'invalid cooking time', 400

		if time == 0:
			time = -1
		ingredient[name] = time

	else:
		return 'invalid type', 400


	return f'added {name} onto the database', 200



# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	name = request.args.get('name')
	totalTime = 0
	items = defaultdict(int)
	recipes = []

	if not recipe[name]:
		return 'not a proper reciepe', 400

	for item in recipe[name]:
		if recipe[item['name']]:
			recipes.append([item['name'], item['quantity']])
		else:
			items[item['name']] += item['quantity']
	
	
	while recipes:
		new, amount = recipes.pop(0)

		for item in recipe[new]:
			if recipe[item['name']]:
				recipes.append([item['name'], amount * item['quantity']])
			else:
				items[item['name']] += (item['quantity'] * amount)
	array = []

	output = []
	for keys in items.keys():
		if not ingredient[keys]:
			return f'{keys} does not exist', 400
		if ingredient[keys] == -1:
			ingredient[keys] = 0
		totalTime += items[keys] * ingredient[keys]
		output.append([items[keys] , ingredient[keys]])
		array.append({"name": f"{keys}", "quantity": f'{items[keys]}'})


	output = {
		"name": f"{name}",
		"cookTime": f"{totalTime}",
		"ingredients": f"{array}"
	}

	return output, 200


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
