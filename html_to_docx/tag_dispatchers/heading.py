from . import ParagraphTailMixin, TagDispatcher


class HeadingDispatcher(ParagraphTailMixin, TagDispatcher):
    @classmethod
    def append_head(cls, element, container):
        paragraph = cls.get_new_paragraph(container)
        return cls._append_heading(element.text, element.tag, paragraph)

    @classmethod
    def _append_heading(cls, text, tag, container):
        """
        <hx> Creates a heading paragraph inside the document container
        """
        level = int(tag[1:])
        style = 'Title' if level == 0 else 'Heading %d' % level

        container.text = text
        container.style = style
        return container
