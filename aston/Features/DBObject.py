"""
DBObject is the base class for anything stored in a AstonDatabase.
"""


class DBObject(object):
    """
    Master class for peaks, features, and datafiles.
    """
    def __init__(self, info=None, data=None, parent=None, db=(None, None)):
        self.info = DBDict(self, info)
        self.rawdata = data

        self._parent = parent
        self._children = None

        self.db_type = 'none'
        self.db, self.db_id = db

    def _load_children(self):
        if self._children is None:
            if self.db is not None:
                self._children = self.db.get_children(self)
            else:
                self._children = []

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        if value is not None:
            #TODO: notify the DB if value is None?
            if value._children is None:
                value._load_children()
            value._children.append(self)
        if self.db is not None:
            self.db.save_object(self)

    def parent_of_type(self, cls=None):
        prt = self._parent
        while True:
            if prt is None:
                return prt
            if prt.db_type == cls:
                return prt
            prt = prt._parent
        else:
            return prt

    @property
    def children(self):
        if self._children is None:
            self._load_children()
        return self._children

    @children.setter
    def children(self, value):
        self._children = value
        for child in value:
            child._parent = self
            if self.db is not None:
                self.db.save_object(child)

    def children_of_type(self, cls=None):
        if self._children is None:
            self._load_children()
        child_list = []
        for child in self._children:
            if child.db_type == cls or cls is None:
                child_list.append(child)
            child_list += child.children_of_type(cls=cls)
        return child_list

    def delete(self):
        if self._parent is not None:
            self._parent._children.remove(self)
        if self.db is not None:
            self.db.delete_object(self)
        self._parent = None

        for child in self._children:
            child.delete()
        self._children = []

    def save_changes(self):
        """
        Save any changes in this object back to the database.
        """
        if self.db is None:
            return
        self.db.save_object(self)

    #override in subclasses
    def _load_info(self, fld):
        pass

    def _calc_info(self, fld):
        return ''


class DBDict(dict):
    def __init__(self, dbobj, *args, **kwargs):
        self._dbobj = dbobj
        #TODO: check that this next part works
        if args == [None]:
            args = [{'name': ''}]
        return super(DBDict, self).__init__(*args, **kwargs)

    def get(self, key, d=None):
        if key not in self.keys():
            self._dbobj._load_info(key)

        if key in self.keys():
            data = super(DBDict, self).get(key)
            if data != '':
                return data
        data = self._dbobj._calc_info(key)
        if data != '':
            return data
        else:
            return d

    def del_items(self, fld):
        #TODO: does invoking del so many times cause a
        #performance hit because of the save_changes in it?
        for key in self.keys():
            if key.startswith(fld):
                del self[key]

    def __getitem__(self, key):
        return self.get(key, '')

    def __setitem__(self, key, val):
        return super(DBDict, self).__setitem__(key, val)

    def __delitem__(self, key):
        self._dbobj.save_changes()
        return super(DBDict, self).__delitem__(key)
