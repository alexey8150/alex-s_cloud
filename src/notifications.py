confirm_code_template = """
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Template</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
            line-height: 1.6;
            font-size: 20px;
        }
        .order-number {
            color: #000;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
</head>
</html>
    <div class="container">
        <h1>Здраствуйте!</h1>
        
        <p>Ваш код подтверждения: <span class="order-number">{{confirm_code}}</span></p>
        
        <p>Вы получили это письмо, так как пытались зарегистрироваться в облачном хранилище Alex\'s cloud.</p>
        
        <p>Если вы этого не делали, просто проигнорируйте это письмо.</p>
    </div>
</body>
</html>
"""

password_mail_template = """
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Восстановление пароля</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
        }

        p {
            margin-bottom: 20px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Ваш пароль для входа в систему</h1>
        <p>Здравствуйте,</p>
        <p>Вы зарегистрировались на сайте Alex's cloud. Ваш пароль для входа в систему: <strong>{{password}}</strong></p>
        <p>С уважением,<br>Alex's CLOUD</p>
    </div>
</body>
</html>
"""
