from app import create_app

app = create_app()

if __name__ == '__main__':
    # Update paths if necessary
    context = ('certs/cert.pem', 'certs/key.pem')
    app.run(host = '0.0.0.0', port = 443, ssl_context = context)