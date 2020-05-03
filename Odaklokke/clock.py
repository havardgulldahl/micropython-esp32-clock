"All time and date related functionality"

import machine, network  # pylint: disable=import-error


def ntp_sync():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        raise Exception("Network not availabel")
    rtc = machine.RTC()
    rtc.ntp_sync(server="no.pool.ntp.org", tz="CEST")
    return rtc.synced()
