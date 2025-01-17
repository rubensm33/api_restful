def register_email_template(user_name, validation_link):
    return f"""
    <html>
    <body>
        <h1>Parabéns! {user_name}</h1>
        <p>Para validar seu email, basta clicar no link abaixo:</p>
        <h2><a href="{validation_link}" target="_blank">Validar Email</a></h2>
    </body>
    </html>
    """
