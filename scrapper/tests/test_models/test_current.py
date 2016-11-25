"""Test current module for models package."""


def test_current_key(models):
    """It tests the models' method key."""
    model, values, key = models
    model.from_dict(values)
    assert model.key() == key
