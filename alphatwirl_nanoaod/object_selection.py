from alphatwirl.selection.modules import All as base_All
from alphatwirl.selection.modules import Any as base_Any
from alphatwirl.selection.modules import Not as base_Not

from alphatwirl.selection import build_selection

##__________________________________________________________________||
class All(base_All):
    """
    select objects that meet all conditions
    """
    def set_args(self, args_dict):
        super(All, self).set_args(args_dict)
        self.in_obj_name = args_dict["in_obj_name"]

    def selection(self, obj):
        for s in self.selections:
            if not s(obj): return False
        return True

    def event(self, event):
        return [o for o in getattr(event, self.in_obj_name) if self.selection(o)]

##__________________________________________________________________||
class Any(base_Any):
    """
    select objects that meet any of the conditions
    """
    def set_args(self, args_dict):
        super(All, self).set_args(args_dict)
        self.in_obj_name = args_dict["in_obj_name"]

    def selection(self, obj):
        for s in self.selections:
            if s(obj): return True
        return False

    def event(self, event):
        return [o for o in getattr(event, self.in_obj_name) if self.selections(o)]

##__________________________________________________________________||
class ObjectSelection(object):
    def __init__(self, **kargs):
        self.out_obj_name = kargs.pop("out_obj_name")
        kargs["AllClass"] = All
        kargs["AnyClass"] = Any
        self.factory_dispatcher = build_selection(**kargs)

    def begin(self, event):
        self.factory_dispatcher.begin(event)

        self.out_objs = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        setattr(event, self.out_obj_name, self.out_objs)

    def event(self, event):
        self._attach_to_event(event)
        self.out_objs[:] = self.factory_dispatcher.event(event)

    def end(self):
        self.factory_dispatcher.end()
