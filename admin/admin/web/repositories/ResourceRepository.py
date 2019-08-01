from masonite import env

class ResourceRepository:

    @staticmethod
    def create(params, new_model):

        for key, value in params.items():
            try:
                setattr(new_model, key, value)
            except Exception as e:
                print(e)

        new_model.save()

    @staticmethod
    def index(model, list_display, offset, items):
        """bussiness logic of index method.

        Args:
            model (class): model class
            list_display ([str]): dfinded in admin config
            offset (int): start position of fetch query
            items (int): how meny items to fetch

        Returns:
            new_result: serialized result
        """
        if list_display:
            results = model.select('id', *list_display) \
                .offset(offset) \
                .limit(items) \
                .get()

            new_results = [result._original for result in results._items]
        else:
            results = model.offset(offset).limit(items).get()
            new_results = [result._original for result in results._items]

        return new_results

    @staticmethod
    def show(model, detail_display, id):
        """bussiness logic of show method.

        Args:
            model (class): model class
            detail_display ([str]): definded in admin config
            id (int): from request param

        Returns:
            new_result: serialized result
        """
        if detail_display and env('DB_CONNECTION') == 'mysql':
            result = model \
                .select(*detail_display) \
                .find(id)

        elif detail_display:
            if 'id' not in detail_display:
                detail_display.insert(0, 'id')
            result = model \
                .select(*detail_display) \
                .find(id)

        else:
            result = model.find(id)

        if result:
            new_result = {i: v for i, v in result._original.items()}
            return new_result

    @staticmethod
    def update(record, params):
        return record.update(**params)

    @staticmethod
    def delete(model, id):
        record = model.find(id)
        if record:
            record.delete()
            return record
