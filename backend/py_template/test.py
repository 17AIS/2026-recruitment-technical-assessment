#!/usr/bin/env python3

import unittest
from devdonalds import app

class FlaskRouteTests(unittest.TestCase):
        
    def setUp(self):
            self.client = app.test_client()
            
            self.client.testing = True

    def test_task2_add_recipe(self):
        response = self.client.post(
            "/entry",
            json={
            "type": "recipe",
            "name": "Slop Salad",
            "requiredItems": [{
                "name": "Mayonaise",
                "quantity": 1
                },{
                "name": "Lettuce",
                "quantity": 3
                }]})
        self.assertEqual(response.status_code, 200)

    def test_task2_add_ingredient(self):
        response = self.client.post(
            "/entry",
            json={
                "type": "ingredient",
                "name": "Egg",
                "cookTime": 3
            })
        self.assertEqual(response.status_code, 200)

    def test_task2_invalidType(self):
        response = self.client.post(
            "/entry",
            json={
                "type": "a banana",
                "name": "Egg",
                "cookTime": 3
            })

        self.assertEqual(response.status_code, 400)

    def test_task2_duplicateIngredient(self):
        response = self.client.post(
            "/entry",
            json={
                "type": "ingredient",
                "name": "Potato",
                "cookTime": 15
            })

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/entry",
            json={
                "type": "ingredient",
                "name": "Potato",
                "cookTime": 15
            })

        self.assertEqual(response.status_code, 400)

    def test_task2_duplicateIngredientRecipe(self):
        response = self.client.post(
            "/entry",
            json={
                "type": "ingredient",
                "name": "new stuff",
                "cookTime": 6
            })
        self.assertEqual(response.status_code, 200)
        

        response = self.client.post(
            "/entry",
            json={
            "type": "recipe",
            "name": "new stuff",
            "requiredItems": [{
                "name": "Mayonaise",
                "quantity": 1
                },{
                "name": "Lettuce",
                "quantity": 3
                }]})
        self.assertEqual(response.status_code, 400)
   
    def test_task2_invalidIngredientParams(self):
        response = self.client.post(
            "/entry",
            json={
            "type": "recipe",
            "name": "Sussy Salad",
            "requiredItems": [{
                "name": "Mayonaise",
                "quantity": 1,
                "irrelevantField": 5,
                },{
                "name": "Lettuce",
                "quantity": 3
                }]})
        self.assertEqual(response.status_code, 400)

    # same as sample exam
    def test_task3_get_spaghetti(self):
        task3 = app.test_client()

        response = task3.get("/summary?name=Skibidi%20Spaghetti")
        self.assertEqual(response.status_code, 400)
        task3.post(
            "/entry",
            json={
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
            }]})
        
        response = task3.get("/summary?name=Skibidi%20Spaghetti")
        self.assertEqual(response.status_code, 400)

        
        task3.post(
            "/entry",
            json={
                "type": "recipe",
                "name": "Meatball",
                "requiredItems": [{
                    "name": "Beef",
                    "quantity": 2
                    },{
                    "name": "Egg",
                    "quantity": 1
            }]})
        
        response = task3.get("/summary?name=Skibidi%20Spaghetti")
        self.assertEqual(response.status_code, 400)

        task3.post(
            "/entry",
            json={
                "type": "recipe",
                "name": "Pasta",
                "requiredItems": [{
                    "name": "Flour",
                    "quantity": 3
                    },{
                    "name": "Egg",
                    "quantity": 1
            }]})
        
        response = task3.get("/summary?name=Skibidi%20Spaghetti")
        self.assertEqual(response.status_code, 400)
        
        task3.post(
            "/entry",
            json={
                "type": "ingredient",
                "name": "Beef",
                "cookTime": 5
            })
        
        response = task3.get("/summary?name=Skibidi%20Spaghetti")
        self.assertEqual(response.status_code, 400)
        
        task3.post(
            "/entry",
            json={
                "type": "ingredient",
                "name": "Egg",
                "cookTime": 3,
             })
        
        response = task3.get("/summary?name=Skibidi%20Spaghetti")
        self.assertEqual(response.status_code, 400)
        
        task3.post(
            "/entry",
            json={
                "type": "ingredient",
                "name": "Flour",
                "cookTime": 0
            })
        
        response = task3.get("/summary?name=Skibidi%20Spaghetti")
        self.assertEqual(response.status_code, 400)
        
        response  = task3.post(
            "/entry",
            json={
                "type": "ingredient",
                "name": "Tomato",
                "cookTime": 2,
            })

        response = task3.get("/summary?name=Skibidi%20Spaghetti")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.get_json()["cookTime"]), 46)

        response = task3.get("/summary?name=Sloppy%20Spaghetti")
        self.assertEqual(response.status_code, 400)
        
         
if __name__ == '__main__':
     unittest.main()

