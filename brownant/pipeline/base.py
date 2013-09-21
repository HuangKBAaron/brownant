from werkzeug.utils import cached_property


class PipelineProperty(cached_property):
    """The base class of pipeline properties.

    There are three kinds of initial parameters.

    The first kind of initial parameters is required attribute. If a keyword
    argument's name was defined in :attr:`required_attrs`, it will be assigned
    as a instance attribute.

    The second kind is the member of :attr:`attr_names`, whose name always end
    with `_attr`, such as `raw_html_attr`.

    The last kind is option parameter, which will be placed at an instance
    owned attribute named :attr:`options`. The subclasses could set default
    option value in the :meth:`prepare`.

    :param kwargs: the parameters with the three kinds.
    """

    #: the names of required attributes.
    required_attrs = set()

    def __init__(self, **kwargs):
        super(PipelineProperty, self).__init__(self.provide_value)
        self.__name__ = None
        self.__module__ = None
        self.__doc__ = None

        #: the definition of attr_names
        self.attr_names = {}
        #: the definition of options
        self.options = {}

        assigned_attrs = set()
        for name, value in kwargs.items():
            assigned_attrs.add(name)

            # names of attrs
            if name.endswith("_attr"):
                self.attr_names[name] = value
            # required attrs
            elif name in self.required_attrs:
                setattr(self, name, value)
            # optional attrs
            else:
                self.options[name] = value
        lacked_attrs = self.required_attrs - assigned_attrs
        if lacked_attrs:
            raise TypeError("required attrs %r" % ", ".join(lacked_attrs))

        self.prepare()

    def prepare(self):
        """This method will be called after instance ininialized. The
        subclasses could override the implementation.

        In general purpose, the implementation of this method should give
        default value to options and the members of :attr:`attr_names`.

        Example:

        .. code-block:: python

           def prepare(self):
               self.attr_names.setdefault("raw_html_attr", "raw_html")
               self.options.setdefault("use_proxy", False)
        """

    def get_attr(self, obj, name):
        """Get attribute of the target object with the configured attribute
        name in the :attr:`attr_names` of this instance.

        :param obj: the target object.
        :param name: the internal name used in the :attr:`attr_names`.
                     .e.g. `"raw_html_attr"`
        """
        attr_name = self.attr_names[name]
        return getattr(obj, attr_name)
