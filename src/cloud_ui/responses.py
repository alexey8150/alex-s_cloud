from fastui import components as c

ERROR_RESPONSE = [
    c.Page(
        components=[
            c.Heading(text='При выполнении запроса произошла ошибка, пожалуйста попробуйте позже.',
                      level=4),
        ]
    ),
]
