import abc
import json
from typing import Any, Generic, List, Optional, overload, Set, TypeVar

from google.cloud import ndb

from backend.common.helpers.listify import delistify, listify
from backend.common.models.cached_model import CachedModel


TModel = TypeVar("TModel", bound=CachedModel)


class ManipulatorBase(abc.ABC, Generic[TModel]):
    @classmethod
    @abc.abstractmethod
    def updateMerge(
        cls, new_model: TModel, old_model: TModel, auto_union: bool
    ) -> TModel:
        """
        Child classes should implement this method with specific merging logic
        """
        ...

    """
    createOrUpdate is the main interface to a manipulator - given a singular/list of models from a caller
    it will either create it in the ndb or do read-modify-write on the existing version
    """

    @overload
    @classmethod
    def createOrUpdate(cls, new_models: TModel, auto_union: bool = True) -> TModel:
        ...

    @overload
    @classmethod
    def createOrUpdate(
        cls, new_models: List[TModel], auto_union: bool = True
    ) -> List[TModel]:
        ...

    @classmethod
    def createOrUpdate(cls, new_models, auto_union=True) -> Any:
        existing_or_new = listify(cls.findOrSpawn(new_models, auto_union))

        models_to_put = [model for model in existing_or_new if model._dirty]
        ndb.put_multi(models_to_put)
        cls._clearCache(existing_or_new)

        for model in existing_or_new:
            model._dirty = False

        return delistify(existing_or_new)

    """
    findOrSpawn will take either a singular model or a list of models and merge them
    with the (optionally present) existing versions
    """

    @overload
    @classmethod
    def findOrSpawn(cls, new_models: TModel, auto_union: bool = True) -> TModel:
        ...

    @overload
    @classmethod
    def findOrSpawn(
        cls, new_models: List[TModel], auto_union: bool = True
    ) -> List[TModel]:
        ...

    @classmethod
    def findOrSpawn(cls, new_models, auto_union=True) -> Any:
        new_models = listify(new_models)
        old_models = ndb.get_multi([model.key for model in new_models], use_cache=False)

        updated_models = [
            cls.updateMergeBase(new_model, old_model, auto_union)
            for (new_model, old_model) in zip(new_models, old_models)
        ]
        return delistify(updated_models)

    @classmethod
    def updateMergeBase(
        cls, new_model: TModel, old_model: Optional[TModel], auto_union
    ) -> TModel:
        """
        Given an "old" and a "new" model object, replace the fields in the
        "old" one that are present in the "new" one, but keep fields from
        the "old" one that are null or the empty list in the "new" one.
        """
        if old_model is None:
            new_model._dirty = True
            new_model._is_new = True
            cls._computeAndSaveAffectedReferences(new_model)
            return new_model

        cls._computeAndSaveAffectedReferences(old_model, new_model)
        return cls.updateMerge(new_model, old_model, auto_union)

    @classmethod
    def _computeAndSaveAffectedReferences(
        cls, old_model: TModel, new_model: Optional[TModel] = None
    ) -> None:
        """
        This method is called whenever a model may potentially be created or updated.
        Stores the affected references in the original instance of the model.
        """

        for attr in old_model._affected_references.keys():
            for a in [old_model, new_model] if new_model is not None else [old_model]:
                val = listify(getattr(a, attr))
                old_model._affected_references[attr] = old_model._affected_references[
                    attr
                ].union(val)

    """
    Helpers for subclasses
    """

    @staticmethod
    def _update_attrs(new_model: TModel, old_model: TModel, auto_union: bool) -> None:
        """
        Given an "old" and a "new" model, replace the fields in the
        "old" that are present in the "new", but keep fields from
        the "old" that are null in the "new".
        """
        updated_attrs: Set[str] = set()

        for attr in old_model._mutable_attrs:
            if (
                getattr(new_model, attr, None) is not None
                or attr in old_model._allow_none_attrs
            ):
                if getattr(new_model, attr) != getattr(old_model, attr):
                    setattr(old_model, attr, getattr(new_model, attr))
                    updated_attrs.add(attr)
                    old_model._dirty = True
            if getattr(new_model, attr, None) == "None":
                if getattr(old_model, attr, None) is not None:
                    setattr(old_model, attr, None)
                    updated_attrs.add(attr)
                    old_model._dirty = True

        for attr in old_model._json_attrs:
            if getattr(new_model, attr) is not None:
                if (getattr(old_model, attr) is None) or (
                    json.loads(getattr(new_model, attr))
                    != json.loads(getattr(old_model, attr))
                ):
                    setattr(old_model, attr, getattr(new_model, attr))
                    # changinging 'attr_json' doesn't clear lazy-loaded '_attr'
                    setattr(old_model, "_{}".format(attr.replace("_json", "")), None)
                    updated_attrs.add(attr)
                    old_model._dirty = True

        list_attrs = old_model._list_attrs
        if not auto_union:
            list_attrs = list_attrs.union(old_model._auto_union_attrs)
        for attr in list_attrs:
            if len(getattr(new_model, attr)) > 0 or not auto_union:
                if getattr(new_model, attr) != getattr(old_model, attr):
                    setattr(old_model, attr, getattr(new_model, attr))
                    updated_attrs.add(attr)
                    old_model._dirty = True

        for attr in old_model._auto_union_attrs if auto_union else {}:
            old_set = set(getattr(old_model, attr))
            new_set = set(getattr(new_model, attr))
            unioned = old_set.union(new_set)
            if unioned != old_set:
                setattr(old_model, attr, list(unioned))
                updated_attrs.add(attr)
                old_model._dirty = True

        old_model._updated_attrs = updated_attrs

    """
    cache clearing hook
    TODO
    """

    @classmethod
    def _clearCache(cls, models: List[TModel]) -> None:
        """
        Make deferred calls to clear caches
        Needs to save _affected_references and the dirty flag
        TODO implement this
        """
