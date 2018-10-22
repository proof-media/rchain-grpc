
import time
from pprint import pprint
from rchain_grpc import casper
# from rchain_grpc import repl

hostname = 'tests-rchain'
connection = casper.create_connection(host=hostname)
# connection = repl.create_connection(host=hostname)
print(connection)

#########
logs = []
rholang_code = """
new print(`rho:io:stdout`) in { print!("Hello World!") }
"""

# #########
# EVAL/REPL not working...
# logs.append(repl.eval(connection=connection, program=rholang_code))
# pprint(logs)

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
time.sleep(3)

#########
print("deploy", casper.deploy(connection, rholang_code))
print("propose", casper.propose(connection))
stream = casper.listen_on(connection, channel_name)
block = next(stream)

results = casper.rho_types.to_dict(block) \
    .get('blockResults', {})[0].get('postBlockData', [])
for result in results:
    print(result)
