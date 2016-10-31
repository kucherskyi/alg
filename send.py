import argparse
import evolute
import uuid
import datetime
import re

from qpid.messaging import Connection

REQUEST = None


def instrument(args):
    request = evolute.InstrumentRequest()
    request.id = {evolute.InstrumentIdType.ISIN: str(args.isin)}
    request.sourceId = str(args.provider)
    global REQUEST
    REQUEST = request


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
instr_parser = subparsers.add_parser('instruments')
instr_parser.add_argument('-p', '--provider', type=str, default='reuters')
instr_parser.add_argument('-i', '--isin', type=str, default='AU3CB0214823')
instr_parser.add_argument('-f', '--file_path', type=str)
instr_parser.set_defaults(func=instrument)

args = parser.parse_args()
args.func(args)

__epoch = datetime.date.fromtimestamp(0)


def parse(value, format_re='(?P<Y>\d{4})(?P<M>\d{2})(?P<D>\d{2})'):
    p = re.compile(format_re)
    m = p.search(value)

    dt = datetime.date(int(m.group('Y')),
                       int(m.group('M')),
                       int(m.group('D')))

    return int((dt - __epoch).total_seconds() * 1000)


def send_response(broker, queue, message):
    # entities to send response data
    connection = Connection(broker)
    connection.open()
    session = connection.session()
    try:
        sender = session.sender(queue)
        sender.send(message)
    finally:
        sender.close()
        session.close()


def send():
    bonded = evolute.bonded_evolute_Data_()
    evolute.Unmarshal(evolute.Marshal(REQUEST), bonded)

    inid = str(uuid.uuid4())[:8]

    message = evolute.Request()
    reqh = evolute.RequestHeader()
    reqh.creationDate = parse("20160830")
    reqh.executionPointer = 0
    reqh.requestUuid = str(uuid.uuid4())

    message.requestHeader = reqh

    subr = evolute.SubRequest()
    subr.engineType = evolute.EngineType().DataLoadEngine
    subr.methodSignature = "Get Account"
    subr.inputIds = [inid]

    message.subRequests = [subr]

    message.dataStorage = {inid: bonded}
    request = evolute.Serialize(message)

    send_response("localhost:5672", "Input-Queue", request)


if __name__ == '__main__':
    send()
