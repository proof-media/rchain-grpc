# unify difference between python 3.7 and 3.6
import sys

if sys.version_info >= (3, 7):
    from google.protobuf.internal.containers import (
        RepeatedCompositeFieldContainer as _Composite,
        RepeatedScalarFieldContainer as _Scalar,
    )
else:
    from google.protobuf.pyext._message import (
        RepeatedCompositeContainer as _Composite,
        RepeatedScalarContainer as _Scalar,
    )

RepeatedCompositeFieldContainer = _Composite
RepeatedScalarFieldContainer = _Scalar
