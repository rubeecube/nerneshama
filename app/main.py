from app import app

debug = True

if debug:
    app.run(debug=True, port=5000)
else:
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000, url_scheme='https')
