# NOTE: this hack is needed because protc uses absolute imports...
import os
import sys

ROOT = os.path.dirname(__file__)
GENERATED = os.path.join(ROOT, 'generated')
sys.path.append(GENERATED)

import CasperMessage_pb2  # isort:skip
import CasperMessage_pb2_grpc  # isort:skip
import RhoTypes_pb2  # isort:skip
import RhoTypes_pb2_grpc  # isort:skip

__version__ = '0.7.2'
