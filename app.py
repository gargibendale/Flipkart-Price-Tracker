from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup 
import time 
import html5lib
import smtplib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/result', methods=['GET','POST'])
def result():
    message = request.args.get('result')
    return render_template("result.html", result=message)

@app.route('/track', methods=['POST'])
def track():
    if request.method == "POST":
        product_url = request.form.get('product-url')
        RECEIVER_EMAIL = request.form.get('email')
        target_price = int(request.form.get('target-price'))

        # fetch webpage 
        r = requests.get(product_url) 
        print('requests successful')
        # parse the html 
        soup = BeautifulSoup(r.content, 'html5lib') 
        with open('file.txt', 'w', encoding="utf-8") as f:
            f.write(str(r.text))

        # extract price using class '_16Jk6d' 
        price = soup.find('div', attrs={"class": "Nx9bqj CxhGGd"}).text 
        title = soup.find('span', attrs={"class": "VU-ZEz"}).text.strip()
        print(title)
        # remove Rs symbol from price 
        price_without_Rs = price[1:] 
        # remove commas from price 
        price_without_comma = price_without_Rs.replace(",", "") 
        # convert price from string to int 
        int_price = int(price_without_comma) 
        print(int_price)

        EMAIL_ADDRESS = 'gargibendale734@gmail.com'
        EMAIL_PASSWORD = 'kiho gpnv secz wdli'

        cur_price = int_price 
        print(f"Current price is {cur_price}") 
        start_time = time.time()
        while True:
            # compare the prices
            if cur_price <= target_price: 
                message = f"Its time to buy the product {title}, its current price is {cur_price}"
                message = message.encode('ascii', 'ignore').decode('ascii')
                with smtplib.SMTP('smtp.gmail.com', 587) as connection:
                    connection.ehlo()
                    connection.starttls()
                    result = connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    print(result)
                    msg = f'Subject: Flipkart Price Alert!!\n\n{message}\n{product_url}'
                    connection.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg)
                    print('email sent!')
                    break
            else:
                
                time.sleep(3600)
            
                #check price every 1 hour
        
        result_text=f"The current price of your product {title} is {cur_price}. Relax, and have a coffee break. We'll mail you, once the product price hits out the target price."
        return redirect(url_for('result', result=result_text))


if __name__ == '__main__':
    app.run(debug=True)