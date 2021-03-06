from base64 import b64decode
from io import BytesIO

from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches

from . import ParagraphTailMixin, TagDispatcher

MAX_WIDTH = Inches(7.5)
MAX_LENGTH = Inches(8)


class ImgDispatcher(ParagraphTailMixin, TagDispatcher):
    @classmethod
    def append_head(cls, element, container):
        container = cls.get_new_paragraph(container)
        return cls._append_img(element, container)

    @classmethod
    def _append_img(cls, element, container):
        """
        First real add on to this thing -kevin
        <img> lets see if this can work.....
        """
        scr = element.attrib['src']
        if 'base64,' not in scr:
            return container

        base64image = scr.split('base64,')[1]
        image_filelike = BytesIO(b64decode(base64image))

        run = container.add_run()
        run.add_break()
        inline_shape = run.add_picture(image_filelike)

        if inline_shape.width > MAX_WIDTH:
            scalar = MAX_WIDTH/inline_shape.width
            inline_shape.width = int(scalar * inline_shape.width)
            inline_shape.height = int(scalar * inline_shape.height)

        if inline_shape.height > MAX_LENGTH:
            scalar = MAX_LENGTH / inline_shape.height
            inline_shape.width = int(scalar * inline_shape.width)
            inline_shape.height = int(scalar * inline_shape.height)

        container.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

        return container
