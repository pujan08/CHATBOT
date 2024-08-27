from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

def load_data():
    # Load the datasets
    df1 = pd.read_csv(r'datasets\microsoft.csv', index_col=0)
    df2 = pd.read_csv(r'datasets\apple.csv', index_col=0)
    df3 = pd.read_csv(r'datasets\tesla.csv', index_col=0)

    # Transpose and reset index
    df1 = df1.T.reset_index()
    df2 = df2.T.reset_index()
    df3 = df3.T.reset_index()

    # Add 'Company' column
    df1['Company'] = 'Microsoft'
    df2['Company'] = 'Apple'
    df3['Company'] = 'Tesla'

    # Concatenate all dataframes
    df = pd.concat([df1, df2, df3])
    df.columns = ['Year', 'Total Revenue', 'Net Income', 'Total Assets', 'Total Liabilities', 'Cash Flow', 'Company']

    # Calculate growth rates
    df['Revenue Growth (%)'] = df.groupby('Company')['Total Revenue'].pct_change() * 100
    df['Net Income Growth (%)'] = df.groupby('Company')['Net Income'].pct_change() * 100

    return df

data = load_data()

def get_answer_by_number(number):
    if number == '1':
        return "What is the total revenue for Microsoft, Apple, and Tesla?"
    elif number == '2':
        return "How has the net income changed for Microsoft, Apple, and Tesla?"
    elif number == '3':
        return "What is the revenue growth for Microsoft, Apple, and Tesla?"
    elif number == '4':
        return "What is the net income growth for Microsoft, Apple, and Tesla?"
    else:
        return "Invalid question number."

def simple_chatbot(query_number):
    # Handle queries based on the number
    if query_number == '1':
        result = []
        for company in ['Microsoft', 'Apple', 'Tesla']:
            revenue = data[data['Company'] == company]['Total Revenue'].iloc[-1]
            result.append(f"The total revenue for {company} is {revenue}.")
        return " | ".join(result)

    elif query_number == '2':
        result = []
        for company in ['Microsoft', 'Apple', 'Tesla']:
            income = data[data['Company'] == company]['Net Income'].iloc[-1]
            result.append(f"The net income for {company} is {income}.")
        return " | ".join(result)

    elif query_number == '3':
        result = []
        for company in ['Microsoft', 'Apple', 'Tesla']:
            growth = data[data['Company'] == company]['Revenue Growth (%)'].dropna().iloc[-1]
            result.append(f"The revenue growth for {company} is {growth:.2f}%.")
        return " | ".join(result)

    elif query_number == '4':
        result = []
        for company in ['Microsoft', 'Apple', 'Tesla']:
            growth = data[data['Company'] == company]['Net Income Growth (%)'].dropna().iloc[-1]
            result.append(f"The net income growth for {company} is {growth:.2f}%.")
        return " | ".join(result)

    else:
        return "Sorry, I can only provide information on predefined questions."

@app.route('/')
def home():
    return render_template_string("""
    <html>
    <head>
        <title>Financial Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                text-align: center;
            }
            .container {
                width: 80%;
                max-width: 600px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
            }
            form {
                margin-top: 20px;
            }
            select {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 4px;
                width: 100%;
                max-width: 300px;
            }
            input[type="submit"] {
                background-color: #007bff;
                color: #fff;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 4px;
                cursor: pointer;
                margin-top: 10px;
            }
            input[type="submit"]:hover {
                background-color: #0056b3;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Financial Chatbot!</h1>
            <p>Select a question number to get a response:</p>
            <form action="/chat" method="get">
                <select name="query_number" required>
                    <option value="">Select a question...</option>
                    <option value="1">1. What is the total revenue for Microsoft, Apple, and Tesla?</option>
                    <option value="2">2. How has the net income changed for Microsoft, Apple, and Tesla?</option>
                    <option value="3">3. What is the revenue growth for Microsoft, Apple, and Tesla?</option>
                    <option value="4">4. What is the net income growth for Microsoft, Apple, and Tesla?</option>
                </select>
                <input type="submit" value="Submit">
            </form>
        </div>
    </body>
    </html>
    """)

@app.route('/chat', methods=['GET'])
def chat():
    query_number = request.args.get('query_number', '')
    if not query_number:
        return "Please select a question number."
    question = get_answer_by_number(query_number)
    response = simple_chatbot(query_number)
    return render_template_string("""
    <html>
    <head>
        <title>Financial Chatbot Response</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                text-align: center;
            }
            .container {
                width: 80%;
                max-width: 600px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
            }
            p {
                font-size: 18px;
            }
            a {
                color: #007bff;
                text-decoration: none;
                font-size: 16px;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Financial Chatbot Response</h1>
            <p><strong>Question:</strong> {{ question }}</p>
            <p><strong>Response:</strong> {{ response }}</p>
            <a href="/">Back</a>
        </div>
    </body>
    </html>
    """, question=get_answer_by_number(query_number), response=simple_chatbot(query_number))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
