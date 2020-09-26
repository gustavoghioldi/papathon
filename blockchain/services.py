from iota import Iota
from iota import ProposedTransaction
from iota import Address
from iota import Tag
from iota import TryteString
from datetime import datetime
api = Iota('https://nodes.devnet.iota.org:443', testnet = True)
address = 'ZLGVEQ9JUZZWCZXLWVNTHBDX9G9KZTJP9VEERIIFHY9SIQKYBVAHIMLHXPQVE9IXFDDXNHQINXJDRPFDXNYVAPLZAW'
       
class IotaService:
    @staticmethod
    def send(trak_id, lat, lon):
        dict_message = {
            "trak_id":trak_id,
            "lat":lat,
            "lon":lon
        }
        message = TryteString.from_unicode(str(dict_message))
        tx = ProposedTransaction(
            address = Address(address),
            message = message,
            tag = Tag(b'TRAK9999999'),
            value = 0
        )
        result = api.send_transfer(transfers = [tx])
        return result
    
    @staticmethod
    def retrive(order_tx):
        bundle = api.get_bundles(order_tx)
        message = bundle['bundles'][0].tail_transaction.signature_message_fragment
        ts = bundle['bundles'][0].tail_transaction.timestamp
        resp = eval(message.decode())
        time_stamp = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        resp['date'] = time_stamp
        return resp



