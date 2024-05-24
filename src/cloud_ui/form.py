import fastapi
import fastui.forms
import pydantic
from fastapi import params as fastapi_params


def patched_fastui_form(model: type[fastui.forms.FormModel]) -> fastapi_params.Depends:
    async def run_fastui_form(request: fastapi.Request):
        async with request.form() as form_data:
            model_data = fastui.forms.unflatten(form_data)

            try:
                yield model.model_validate(model_data)
            except pydantic.ValidationError as e:
                raise fastapi.HTTPException(
                    status_code=422,
                    detail={'form': e.errors(include_input=False, include_url=False, include_context=False)},
                )

    return fastapi.Depends(run_fastui_form)


fastui.forms.fastui_form = patched_fastui_form