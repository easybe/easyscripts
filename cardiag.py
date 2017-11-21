import obd

connection = obd.OBD()

#status = connection.query(obd.commands.STATUS).value

print("Freeze DTCs")
code, msg = connection.query(obd.commands.FREEZE_DTC).value
print("{}\t{}".format(code, msg))

print("DTCs")
dtcs = connection.query(obd.commands.GET_DTC).value
for code, msg in dtcs:
    print("{}\t{}".format(code, msg))

obd.commands.FREEZE_DTC
