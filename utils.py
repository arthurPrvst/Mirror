def hex2bin(d, nb=0):
    # Convert Hexadecimal number to binary
    d=int(d,16)
    if d==0:
        b="0"
    else:
        b=""
        while d!=0:
            b="01"[d&1]+b
            d=d>>1
    return b.zfill(nb)