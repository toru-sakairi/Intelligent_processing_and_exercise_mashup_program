from RecipeNutrition import app
from flask import Flask, render_template
#これをやるとcore空モジュールをインポートできる
#from core. ~~~

@app.route('/')
def index():
    return render_template('main.html')