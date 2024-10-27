from flask import Flask, render_template, request, jsonify
import cohere
import os

app = Flask(__name__)

# Set your Cohere API key here (use environment variables for security)
COHERE_API_KEY = os.getenv('COHERE_API_KEY', '72u8aM6VJfoo9RMJFDkZDOQ9NEfBuUslkpmPYvoI')
co = cohere.Client(COHERE_API_KEY)

# Function to generate a response using Cohere API with user bio and mood context
def get_cohere_response(user_input, user_bio, mood):
    try:
        # Construct a prompt with all user inputs (bio, mood, message)
        prompt = (
            "Keep your responses less than 30 words."
            f"You are a supportive mental health assistant.\n"
            f"The user provided this information about themselves: {user_bio}.\n"
            f"They are feeling {mood}.\n"
            f"User's message: {user_input}\n"
            "Assistant:"
        )

        response = co.generate(
            model='command-xlarge',
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I encountered an issue. Please try again later."

# Route for the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle chatbot messages
@app.route("/get_response", methods=["POST"])
def get_chat_response():
    data = request.json
    user_message = data.get("message")
    user_bio = data.get("user_details", "No bio provided.")  # Default if bio is missing
    mood = data.get("mood", "neutral")  # Default to 'neutral' if no mood is provided

    # Generate the chatbot response
    bot_response = get_cohere_response(user_message, user_bio, mood)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
