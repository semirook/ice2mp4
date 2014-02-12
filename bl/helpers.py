# coding=utf-8
import Ice
import MediaFile
from collections import namedtuple
from bl.convertor import MediaFileTransferI


IceMedia = namedtuple('IceMedia', ['name_id', 'conn'])


IceMediaMediaPrx = IceMedia(
    name_id='SimpleConverter',
    conn='tcp -p 10000'
)


IceAdapters = {
    'SimpleConverterAdapter': {
        'reg': [(MediaFileTransferI, 'SimpleConverter')],
        'conn': 'tcp -p 10000'
    }
}


class IceConnection(object):

    def __init__(self, conn_prx, meth_prx):
        self._conn_prx = conn_prx
        self._meth_prx = meth_prx
        self._ic = None

    def __enter__(self):
        self._ic = Ice.initialize()
        base = self._ic.stringToProxy(
            '%s:%s' % (
                self._conn_prx.name_id,
                self._conn_prx.conn,
            )
        )
        ice_entity_prx = getattr(self._meth_prx, 'checkedCast')(base)
        if not ice_entity_prx:
            raise RuntimeError("Invalid proxy")

        return ice_entity_prx

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        if self._ic:
            try:
                self._ic.destroy()
            except:
                pass


def ice_send_file(filename, file_inst):
    chunkSize = 1024 * 128
    offset = 0
    results = []
    numRequests = 5
    is_completed = False

    with IceConnection(IceMediaMediaPrx, MediaFile.FileTransferPrx) as icer:
        if icer.isFileExists(filename):
            icer.removeFile(filename)

        while True:
            bytes = file_inst.stream.read(chunkSize)
            if not bytes:
                file_inst.close()
                break

            send_async = icer.begin_send(filename, offset, bytes)
            offset += len(bytes)

            send_async.waitForSent()
            results.append(send_async)

            while len(results) > numRequests:
                send_async = results[0]
                del results[0]
                send_async.waitForCompleted()

        while len(results) > 0:
            send_async = results[0]
            del results[0]
            send_async.waitForCompleted()

        is_completed = send_async.isCompleted()

    return is_completed


def ice_convert_to_mp4(filename):
    output_file_name = ''
    with IceConnection(IceMediaMediaPrx, MediaFile.FileTransferPrx) as icer:
        output_file_name = icer.convertToMp4(filename)

    return output_file_name
