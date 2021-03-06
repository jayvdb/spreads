import time
from itertools import chain, repeat

import mock

with mock.patch('cffi.FFI'):
    import spreadsplug.hidtrigger as hidtrigger


@mock.patch('spreadsplug.hidtrigger.hidapi.enumerate')
@mock.patch('spreadsplug.hidtrigger.hidapi.Device')
def test_trigger_loop(devicecls, hid_enumerate):
    mock_dev = mock.Mock()
    mock_dev.read.side_effect = chain(
        list(chain(repeat(None, 10), ('foo',), repeat(None, 10), ('bar',)))*6,
        repeat(None))
    hid_enumerate.return_value = [mock.Mock(), mock.Mock()]
    devicecls.return_value = mock_dev
    mock_cb = mock.Mock()
    plugin = hidtrigger.HidTrigger(config=None)
    plugin.start_trigger_loop(mock_cb)
    time.sleep(1.3)
    plugin.stop_trigger_loop()
    assert not plugin._loop_thread.is_alive()
    assert mock_cb.call_count == 6
