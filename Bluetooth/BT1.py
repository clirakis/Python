"""
Modified  By   Reason
--------  --   ------
13-Nov-26 CBL  Original. looking at bluetooth interfaces.

"""
import hid

def All():
    for device in hid.enumerate():
        print(
            "Man: ",device["manufacturer_string"],
            "Prod: ", device["product_string"],
            hex(device["vendor_id"]),
            hex(device["product_id"]),
            device["usage_page"],
            device["usage"]
        )

def Some():
     for device in hid.enumerate():
        print(
            device["manufacturer_string"],
            device["product_string"],
            )

def Another():
    print("find path")
    for device in hid.enumerate():
        if device["usage_page"] == 0xFF00:
            print("Product: ", device["product_string"])
            print("Vendor: ", hex(device["vendor_id"]))
            print("Product ID: ", hex(device["product_id"]))
            print("Path: ", device["path"])
    
if __name__ == '__main__':
    All()
    #Another()
   
