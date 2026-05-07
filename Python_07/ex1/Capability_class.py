#!/usr/bin/env python3
from abc import ABC, abstractmethod


class HealCapability(ABC):

    @abstractmethod
    def heal(self, target=None) -> str:
        pass


class TransformCapability(ABC):

    def __init__(self, transformed: bool = False):
        self.transformed = transformed

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass
