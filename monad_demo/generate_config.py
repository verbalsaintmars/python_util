from common_func import get_dict_obj


def validate_for_none(key, result, anchor=None, path="", sep="/"):
    if anchor is None:
        anchor = []
    if result[key]:
        if isinstance(result[key], dict):
            for k in result[key].keys():
                validate_for_none(
                    k, result[key], anchor, (sep).join((path, key)))
    else:
        anchor.append((sep).join((path, key)))
    return anchor


class key_monad(object):
    """
    Context is immutable.
    No side-effect.
    """
    CACHE = {}

    def __init__(self, key, config, separator=r"/"):
        """
        :key: config key string tuple or single key string
        :config: json config
        """
        self.__key = key
        self.__config = config
        self.__result = {}
        self.__key_separator = separator

        def assign(k):
            key = k.split(self.key_separator)[-1]
            self.__result[key] = self.CACHE.get(
                k, self.__get_dict_obj(k, self.key_separator))
            self.CACHE[k] = self.__result[key]

        if isinstance(self.key, list) or isinstance(self.key, tuple):
            for k in iter(self.key):
                assign(k)
        else:
            assign(self.key)

    def __get_dict_obj(self, key, separator):
        return get_dict_obj(self.__config, key, separator=separator)

    @property
    def key_separator(self):
        return self.__key_separator

    @property
    def result_key(self):
        return self.result.keys()

    @property
    def key(self):
        return self.__key

    @property
    def result(self):
        return self.__result

    def apply_validate(self, validator=validate_for_none):
        """
        :validator: callable object taking arg(key, value) to validate.
        :return: list of invalid keys.
        """
        keys_not_valid = []
        if isinstance(self.result_key, list) or \
           isinstance(self.result_key, tuple):
            for k in iter(self.result_key):
                keys_not_valid.extend(validator(k, self.result))
        else:
            keys_not_valid.extend(validator(self.result_key, self.result))
        return keys_not_valid

    def apply(self, functor):
        keylist = []

        if isinstance(self.key, list) or isinstance(self.key, tuple):
            keylist.extend(self.key)
        else:
            keylist.append(self.key)

        if isinstance(functor.key, list) or isinstance(functor.key, tuple):
            keylist.extend(functor.key)
        else:
            keylist.append(functor.key)

        return key_monad(tuple(set(keylist)), self.__config)


def generate_config(config, keys):
    def create_monoid(keys, monad=None, root=''):
        for k in keys:
            k = root + k
            if monad:
                monad = monad.apply(key_monad(k, config))
            else:
                monad = key_monad(k, config)
        return monad

    monad = create_monoid(keys)
    return monad
