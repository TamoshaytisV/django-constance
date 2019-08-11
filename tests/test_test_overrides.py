from django.test import TestCase

from constance import config
from constance.test import override_config
from constance.test.pytest import override_config as pytest_override_config


class OverrideConfigFunctionDecoratorTestCase(TestCase):
    """Test that the override_config decorator works correctly.

    Test usage of override_config on test method and as context manager.
    """
    def test_default_value_is_true(self):
        """Assert that the default value of config.BOOL_VALUE is True."""
        self.assertTrue(config.BOOL_VALUE)

    @override_config(BOOL_VALUE=False)
    def test_override_config_on_method_changes_config_value(self):
        """Assert that the method decorator changes config.BOOL_VALUE."""
        self.assertFalse(config.BOOL_VALUE)

    def test_override_config_as_context_manager_changes_config_value(self):
        """Assert that the context manager changes config.BOOL_VALUE."""
        with override_config(BOOL_VALUE=False):
            self.assertFalse(config.BOOL_VALUE)

        self.assertTrue(config.BOOL_VALUE)


class PytestOverrideConfigFunctionDecoratorTestCase:
    """Test that the override_config decorator works correctly for Pytest classes.

    Test usage of override_config on test method and as context manager.
    """
    def test_default_value_is_true(self):
        """Assert that the default value of config.BOOL_VALUE is True."""
        assert config.BOOL_VALUE

    @pytest_override_config(BOOL_VALUE=False)
    def test_override_config_on_method_changes_config_value(self):
        """Assert that the method decorator changes config.BOOL_VALUE."""
        assert not config.BOOL_VALUE

    def test_override_config_as_context_manager_changes_config_value(self):
        """Assert that the context manager changes config.BOOL_VALUE."""
        with pytest_override_config(BOOL_VALUE=False):
            assert not config.BOOL_VALUE

        assert config.BOOL_VALUE


@pytest_override_config(ANY_PARAM="any_value")
class PytestOverrideConfigClassSetupTeardownTestCase:
    """Test that the override_config class decorator respects setup/teardown of test case."""
    urls = []

    def setup(self):
        self.urls.append("/some/url/")

    def teardown(self):
        self.urls.pop()

    def test_override_not_affects_setup_teardown(self):
        """Ensure setup() and teardown() methods are not affected by override."""
        self.setup()  # emulate pytest triggered setup
        assert self.urls
        self.teardown()  # emulate pytest triggered teardown
        assert not self.urls


@override_config(BOOL_VALUE=False)
class OverrideConfigClassDecoratorTestCase(TestCase):
    """Test that the override_config decorator works on classes."""
    def test_override_config_on_class_changes_config_value(self):
        """Asser that the class decorator changes config.BOOL_VALUE."""
        self.assertFalse(config.BOOL_VALUE)


@pytest_override_config(BOOL_VALUE=False)
class PytestOverrideConfigClassDecoratorTestCase:
    """Test that the override_config decorator works on classes."""
    def test_override_config_on_class_changes_config_value(self):
        """Asser that the class decorator changes config.BOOL_VALUE."""
        assert not config.BOOL_VALUE
