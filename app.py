from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

base_price = 100
min_price = 80

@app.route('/')
def home():
    return "Welcome to the Negotiation Bot API."


def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"


@app.route('/negotiate', methods=['POST'])
def negotiate():
    customer_offer = request.json.get('customer_offer')
    customer_message = request.json.get('customer_message', "")  

    sentiment = analyze_sentiment(customer_message)


    if customer_offer >= base_price:
        bot_response = f"Accepted! We'll sell the product for {customer_offer}."
    elif customer_offer >= min_price:
        if sentiment == "positive":
            bot_response = f"That's a great offer! Since you're so polite, I'll give you a special counteroffer of {min_price - 10}. Would you accept?"
        elif sentiment == "negative":
            bot_response = f"That's too low, but I can counteroffer with {min_price}. Please consider this offer."
        else:  
            bot_response = f"That's too low, but I'll counteroffer with {min_price}. Would you accept?"
    else:
        bot_response = "Your offer is too low. Please increase your offer."

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
