func = (lambda g, c, d: (lambda _: (_.__setitem__('$', ''.join([(_['chr'] if ('chr'
in _) else chr)((_['_'] if ('_' in _) else _)) for _['_'] in (_['s'] if ('s'
in _) else s)[::(-1)]])), _)[-1])( (lambda _: (lambda f, _: f(f, _))((lambda
__,_: ((lambda _: __(__, _))((lambda _: (_.__setitem__('i', ((_['i'] if ('i'
in _) else i) + 1)),_)[(-1)])((lambda _: (_.__setitem__('s',((_['s'] if ('s'
in _) else s) + [((_['l'] if ('l' in _) else l)[(_['i'] if ('i' in _) else i
)] ^ (_['c'] if ('c' in _) else c))])), _)[-1])(_))) if (((_['g'] if ('g' in
_) else g) % 4) and ((_['i'] if ('i' in _) else i)< (_['len'] if ('len' in _
) else len)((_['l'] if ('l' in _) else l)))) else _)), _) ) ( (lambda _: (_.
__setitem__('!', []), _.__setitem__('s', _['!']), _)[(-1)] ) ((lambda _: (_.
__setitem__('!', ((_['d'] if ('d' in _) else d) ^ (_['d'] if ('d' in _) else
d))), _.__setitem__('i', _['!']), _)[(-1)])((lambda _: (_.__setitem__('!', [
(_['j'] if ('j' in _) else j) for  _[ 'i'] in (_['zip'] if ('zip' in _) else
zip)((_['l0'] if ('l0' in _) else l0), (_['l1'] if ('l1' in _) else l1)) for
_['j'] in (_['i'] if ('i' in _) else i)]), _.__setitem__('l', _['!']), _)[-1
])((lambda _: (_.__setitem__('!', [1373, 1281, 1288, 1373, 1290, 1294, 1375,
1371,1289, 1281, 1280, 1293, 1289, 1280, 1373, 1294, 1289, 1280, 1372, 1288,
1375,1375, 1289, 1373, 1290, 1281, 1294, 1302, 1372, 1355, 1366, 1372, 1302,
1360, 1368, 1354, 1364, 1370, 1371, 1365, 1362, 1368, 1352, 1374, 1365, 1302
]), _.__setitem__('l1',_['!']), _)[-1])((lambda _: (_.__setitem__('!',[1375,
1368, 1294, 1293, 1373, 1295, 1290, 1373, 1290, 1293, 1280, 1368, 1368,1294,
1293, 1368, 1372, 1292, 1290, 1291, 1371, 1375, 1280, 1372, 1281, 1293,1373,
1371, 1354, 1370, 1356, 1354, 1355, 1370, 1357, 1357, 1302, 1366, 1303,1368,
1354, 1355, 1356, 1303, 1366, 1371]), _.__setitem__('l0', _['!']), _)[(-1)])
            ({ 'g': g, 'c': c, 'd': d, '$': None})))))))['$'])

for i in range(1000, 0x1000):
        try:
            ret = func(1, i, 0)
            if 'quarks' in ret:
                print '%r' % ret
        except:
            pass