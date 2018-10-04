#!/usr/bin/env bash

NAME=caspar_message_proto
TMP=`mktemp -d --suffix _$NAME`
RCHAIN=$TMP/rchain
SCALAPB=$TMP/scalapb
PROTO=./proto
PY=./generated
GIT="git clone --depth 1 -b master"

# download scalaPB and rchain repos, sources of proto files
$GIT https://github.com/rchain/rchain.git $RCHAIN
$GIT https://github.com/scalapb/ScalaPB.git $SCALAPB

# remove all proto, always start from scrach
rm -rf $PROTO $PY
mkdir $PROTO $PY

# copy proto files
cp $RCHAIN/models/src/main/protobuf/CasperMessage.proto $PROTO/CasperMessage.proto
cp $RCHAIN/models/src/main/protobuf/RhoTypes.proto $PROTO/RhoTypes.proto
cp $RCHAIN/node/src/main/protobuf/repl.proto $PROTO/repl.proto
cp -R $SCALAPB/protobuf/scalapb $PROTO/scalapb


python -m grpc_tools.protoc   `# call code generator`\
       --proto_path=$PROTO    `# path to dir with protofiles`\
       --python_out=$PY       `# dir for files with types and low level code`\
       --grpc_python_out=$PY  `# dir for client code`\
       CasperMessage.proto    `# list of files to be compiled`\
       RhoTypes.proto         \
       repl.proto             \
       scalapb/scalapb.proto

touch $PY/scalapb/__init__.py # make scalapb python package
touch $PY/__init__.py         # make generated python package

rm -rf $TMP
