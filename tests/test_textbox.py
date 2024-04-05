from unittest import TestCase

from certificator.certificates import TextBox


class TestTextBox(TestCase):
    def test_start_must_be_top_left(self):
        with self.assertRaises(AssertionError, msg="Start cannot be bottom-right"):
            TextBox((0.6, 0.4), (0.1, 0.3), (0, 0)),

        with self.assertRaises(AssertionError, msg="Start cannot be bottom-left"):
            TextBox((0.1, 0.4), (0.6, 0.3), (0, 0))

        with self.assertRaises(AssertionError, msg="Start cannot be top-right"):
            TextBox((0.6, 0.3), (0.1, 0.4), (0, 0))

    def test_width_height(self):
        box = TextBox((0.1, 0.3), (0.6, 0.4), (1920, 1080))

        self.assertEqual(box.width, 960)
        self.assertEqual(box.height, 108)

    def test_font_size(self):
        box = TextBox((0.1, 0.3), (0.6, 0.4), (1920, 1080))

        self.assertEqual(box.font_size(960), 108)
        self.assertEqual(box.font_size(961), 107)

    def test_text_start(self):
        box = TextBox((0.1, 0.3), (0.6, 0.4), (1920, 1080))

        self.assertEqual(box.text_start(500, 108), (422, 313))
