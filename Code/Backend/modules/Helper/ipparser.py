#!/usr/bin/python
#parses ip or mask to integer
def parse_to_int(value):
    split = value.split(".")
    split = [int(i) for i in split]
    if(len(split)!=4):
        raise Exception("invalid dotted decimal value")
    retval = 0
    for i in range(4):
        if(split[i]>255 or split[i]<0):
            raise Exception("invalid dotted decimal value")
        retval+=split[i]<<((3-i)*8)
    return retval

#parse integer to ip or mask
def parse_to_quad(value):
    a=[]
    for _ in range(4):
        a.insert(0,str(value%256))
        value = value//256;
    return ".".join(a)

#masks ip
def mask_ip(ip, mask):
    return parse_to_int(ip)&invert_bits_32(mask)

def getDirection(dst, ipRange, mask):
    if mask_ip(dst,mask)==mask_ip(ipRange,mask):
       return "ingress"
    return "egress" 

def verifyQuads(*args):
    for arg in args:
        try:
            parse_to_int(arg)
        except:
            return False
    return True

#converts mask to and-able format
def invert_bits_32(value):
    mask = parse_to_int(value)
    constant = 0b11111111111111111111111111111111 #32 bits
    return constant - mask
