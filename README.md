# very-secure-web-server
![Description](files/the%20scene.png)

**Why Would You Use This?**

I rewatched _The Social Network_ recently, and guess what? I wanted to tackle the same challenge Zuckerberg threw down: "10 minutes to get a root access to a python web server; expose its ssl encryption and interecept all traffic over its secure ports." But- I don't have a Python server. So, I rolled up my sleeves and built my very own!

Use it for fun.

_Disclaimer: Please don't use this for wrong purposes.  Not to mention, Don't go to wild, wild internet for this._

**Let the hacking begin!**

## **Setup**
### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-pen-testing-server.git
   cd python-pen-testing-server
   ```
2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

4. Generate a SSL signed certificate:
    ```bash
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
    ```

## **Usage**
1. Run the server:
    ```bash
    python server.py
    ```
2. Access the server in your browser:
    - Navigate to: [https://localhost:443](https://localhost:443)
    - You might see a "Not secure" warning. This happens because the SSL certificate is self-signed. Simply bypass the warning to proceed.

## **Contact** 
Feel free to reach out for any questions/suggestions.