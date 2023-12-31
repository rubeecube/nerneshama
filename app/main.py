from app import app

debug = False

if debug:
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000, url_scheme='https')
