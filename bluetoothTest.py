# #import ubluetooth
# from ble_advertising import advertising_payload as adpl

# if __name__=='__main__':
#     #ble = ubluetooth.BLE()
#     pl = adpl(name='TempSens', customData=56)  # 56 is some random "data" to test, put in whatever you like but there is a limit to the total advertisement length.
#     ble.active(True)
#     ble.gap_advertise(30000, adv_data=pl)