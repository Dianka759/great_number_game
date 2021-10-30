from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe, hush hush!'


@app.route('/')
def start():
    import random                                               #import random
    if "number" not in session:                                 #Create a random number
        session["number"] = random.randint(1, 100)
    
    message_to_player = {                                       #creating a message to show to the player which will change upon every guess accordingly.
        "message": None                                         #before the game starts, message is empty.
    }
    previous_guess = {                                          #creating a message to show to the player which will change upon every guess accordingly.
        "message": "I will let you know your previous guess here! :)"
    }
    color = "mediumpurple"                                      #sets the initial color of the hint box to purple. 

    if "game" not in session:
        message_to_player["message"] = "Give it a try!"        #First message to the player before guessing
    
    elif session["game"] > session["number"]:                  #if guess is higher than the number, display message 
        message_to_player["message"] = "Too high! ↓"
        previous_guess["message"] = "Your guess was: " + str(session["game"]) #displays player's number of choice
        color = "red"                                                         #background color changes red.
    
    elif session["game"] < session["number"]:                  #if guess is lower than the number, display message
        message_to_player["message"] = "Too low! ↑"
        previous_guess["message"] = "Your guess was: " + str(session["game"])
        color = "red"
    
    elif session["game"] == session["number"]:                 #if the player guessed correctly, congratulate!
        message_to_player["message"] = "You got it! 👏. The mighty number was: " + str(session['number'])
        previous_guess["message"] = ""                         #removes the message from the page.
        color = "green"                                        #background color changes green for victory!

    if "guesses" not in session:                               #keeps track of the guesses
        session['guesses'] = 0

    return render_template("index.html", display=message_to_player, previous_guess=previous_guess, color = color)


# Informing the player how many guesses have been taken.
@app.route('/guess', methods=["POST"])                         #with every guess, the count goes up by 1.
def guess():
    session["game"] = int(request.form["game"])
    session["guesses"] += 1
    return redirect('/')


@app.route('/restart')  # Added option to restart the number of guesses/random number
def restart():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)