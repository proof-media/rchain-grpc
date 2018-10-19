
from pprint import pprint
from rchain_grpc import casper

connection = casper.create_connection(host='tests-rchain')
print(connection)

#########
logs = []
rholang_code = """
new print(`rho:io:stdout`) in { print!("Hello World!") }
"""

#########
logs.append(casper.deploy(connection, rholang_code))
logs.append(casper.propose(connection))
pprint(logs)

#########
blocks = casper.get_blocks(connection)
pprint(blocks)
block_hash = blocks.pop().get('blockHash')
block_data = casper.get_block(connection, block_hash)
print("Currently on block", block_data.get('blockNumber'))

#########
channel_name = 'test_name'
rholang_code = f"""
@"{channel_name}"!("Hello World!")
"""
print(casper.deploy(connection, rholang_code))
print(casper.propose(connection))
output = casper.get_value_from(connection, channel_name)
pprint(output)

#########
# TODO: test listen on
