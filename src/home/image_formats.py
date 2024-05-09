from wagtail.images.formats import Format, register_image_format


class FloatLeft(Format):
    def image_to_html(self, image, alt_text, extra_attributes=None):
        default_html = super().image_to_html(image, alt_text, extra_attributes)
        return f'<div class="is-clearfix"></div>{default_html}'


class FloatRight(Format):
    def image_to_html(self, image, alt_text, extra_attributes=None):
        default_html = super().image_to_html(image, alt_text, extra_attributes)
        return f'<div class="is-clearfix"></div>{default_html}'


register_image_format(
    FloatLeft("float_left", "Float Left", "image is-pulled-left pr-3 pb-3", "width-400")
)
register_image_format(
    FloatRight(
        "float_right", "Float Right", "image is-pulled-right pl-3 pb-3", "width-400"
    )
)
