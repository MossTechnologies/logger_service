from src.services.exceptions import NotModelError


def generate_id_for_any_model(model) -> int:
    try:
        return model.objects.count()+1
    except AttributeError:
        raise NotModelError('The transferred instance is not a model.')
