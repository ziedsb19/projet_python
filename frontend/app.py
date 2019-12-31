import dash


external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']
app = dash.Dash(name="test", external_stylesheets=external_stylesheets, assets_folder='assets')
app.config.suppress_callback_exceptions = True

