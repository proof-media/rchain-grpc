# hack needed becouse protc use absolute imports
import sys, os

ROOT = os.path.dirname(__file__)
GENERATED = os.path.join(ROOT, 'generated')
sys.path.append(GENERATED)

import CasperMessage_pb2_grpc
import CasperMessage_pb2

import RhoTypes_pb2_grpc
import RhoTypes_pb2
