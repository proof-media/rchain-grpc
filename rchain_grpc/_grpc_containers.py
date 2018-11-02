# unify difference between python 3.7 and 3.6
import sys
from typing import Union

from google.protobuf.pyext._message import (RepeatedCompositeContainer,
                                            RepeatedScalarContainer)

container_classes = [RepeatedCompositeContainer, RepeatedScalarContainer]
IContainer = Union[RepeatedCompositeContainer, RepeatedScalarContainer]

if sys.version_info >= (3, 7):
    from google.protobuf.internal.containers import (
        RepeatedCompositeFieldContainer,
        RepeatedScalarFieldContainer,
    )

    container_classes.extend(
        (RepeatedCompositeFieldContainer, RepeatedScalarFieldContainer)
    )
    IContainer = Union[
        RepeatedCompositeContainer,
        RepeatedScalarContainer,
        RepeatedCompositeFieldContainer,
        RepeatedScalarFieldContainer,
    ]
