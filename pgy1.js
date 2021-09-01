function sign(_0x1bb593, _0xd5e273) {
    var _0x1e241f = function (_0x46b1a2) {
        function _0x5ccfe5(_0x448670) {
            if (_0x15b4fd[_0x448670]) return _0x15b4fd[_0x448670]['exports'];

            var _0x5d6130 = _0x15b4fd[_0x448670] = {
                'i': _0x448670,
                'l': false,
                'exports': {}
            };

            return _0x46b1a2[_0x448670]['call'](_0x5d6130['exports'], _0x5d6130, _0x5d6130['exports'], _0x5ccfe5), _0x5d6130['l'] = true, _0x5d6130['exports'];
        }

        var _0x15b4fd = {};
        return _0x5ccfe5['m'] = _0x46b1a2, _0x5ccfe5['c'] = _0x15b4fd, _0x5ccfe5['i'] = function (_0xa49a68) {
            return _0xa49a68;
        }, _0x5ccfe5['d'] = function (_0x27309c, _0xdf4968, _0x5b2393) {
            var _0x505d94 = {
                'configurable': false,
                'enumerable': true,
                'get': _0x5b2393
            };
            _0x5ccfe5['o'](_0x27309c, _0xdf4968) || Object['defineProperty'](_0x27309c, _0xdf4968, _0x505d94);
        }, _0x5ccfe5['n'] = function (_0x271e6a) {
            var _0x201a31 = _0x271e6a && _0x271e6a['__esModule'] ? function () {
                return _0x271e6a['default'];
            } : function () {
                return _0x271e6a;
            };

            return _0x5ccfe5['d'](_0x201a31, 'a', _0x201a31), _0x201a31;
        }, _0x5ccfe5['o'] = function (_0x174749, _0x396f07) {
            return Object['prototype']['hasOwnProperty']['call'](_0x174749, _0x396f07);
        }, _0x5ccfe5['p'] = '', _0x5ccfe5(_0x5ccfe5['s'] = 4);
    }([function (_0x3e78a9, _0x577a2a) {
        var _0xeb44e8 = {
            'utf8': {
                'stringToBytes': function (_0x20b505) {
                    return _0xeb44e8['bin']['stringToBytes'](unescape(encodeURIComponent(_0x20b505)));
                },
                'bytesToString': function (_0x58bb5f) {
                    return decodeURIComponent(escape(_0xeb44e8['bin']['bytesToString'](_0x58bb5f)));
                }
            },
            'bin': {
                'stringToBytes': function (_0x41cbb6) {
                    var _0x57e475 = [],
                        _0x1f2252 = 0;

                    for (; _0x1f2252 < _0x41cbb6['length']; _0x1f2252++) _0x57e475['push'](255 & _0x41cbb6['charCodeAt'](_0x1f2252));

                    return _0x57e475;
                },
                'bytesToString': function (_0xc7dc19) {
                    var _0x2cad68 = [],
                        _0x3ad8fa = 0;

                    for (; _0x3ad8fa < _0xc7dc19['length']; _0x3ad8fa++) _0x2cad68['push'](String['fromCharCode'](_0xc7dc19[_0x3ad8fa]));

                    return _0x2cad68['join']('');
                }
            }
        };
        _0x3e78a9['exports'] = _0xeb44e8;
    }, function (_0x1e13e9, _0x532b44, _0x1a1caf) {
        !function () {
            var _0xa50d05 = _0x1a1caf(2),
                _0x22f48f = _0x1a1caf(0)['utf8'],
                _0x108157 = _0x1a1caf(3),
                _0x34fccd = _0x1a1caf(0)['bin'],
                _0x10ce55 = function (_0x3dbf2d, _0x1f282c) {
                    var _0x5852ad = 0;
                    _0x3dbf2d['constructor'] == String ? _0x3dbf2d = _0x1f282c && 'binary' === _0x1f282c['encoding'] ? _0x34fccd['stringToBytes'](_0x3dbf2d) : _0x22f48f['stringToBytes'](_0x3dbf2d) : _0x108157(_0x3dbf2d) ? _0x3dbf2d = Array['prototype']['slice']['call'](_0x3dbf2d, 0) : Array['isArray'](_0x3dbf2d) || (_0x3dbf2d = _0x3dbf2d['toString']());

                    var _0x510f99 = _0xa50d05['bytesToWords'](_0x3dbf2d),
                        _0x3f5924 = 8 * _0x3dbf2d['length'],
                        _0x5a7da4 = 1732584193,
                        _0x1fdf74 = -271733879,
                        _0x2bd1cd = -1732584194,
                        _0x14a341 = 271733878,
                        _0x288bb8 = 0;

                    for (; _0x288bb8 < _0x510f99['length']; _0x288bb8++) _0x510f99[_0x288bb8] = 16711935 & (_0x510f99[_0x288bb8] << 8 | _0x510f99[_0x288bb8] >>> 24) | 4278255360 & (_0x510f99[_0x288bb8] << 24 | _0x510f99[_0x288bb8] >>> 8);

                    _0x510f99[_0x3f5924 >>> 5] |= 128 << _0x3f5924 % 32, _0x510f99[14 + (_0x3f5924 + 64 >>> 9 << 4)] = _0x3f5924;
                    var _0x20a3ac = _0x10ce55['_ff'],
                        _0x3705ba = _0x10ce55['_gg'],
                        _0x60ed3 = _0x10ce55['_hh'],
                        _0x4396ce = _0x10ce55['_ii'],
                        _0x288bb8 = 0;

                    for (; _0x288bb8 < _0x510f99['length']; _0x288bb8 += 16) {
                        var _0x1a8bf5 = _0x5a7da4,
                            _0x44711f = _0x1fdf74,
                            _0x359546 = _0x2bd1cd,
                            _0x5bb435 = _0x14a341;
                        _0x5a7da4 = _0x20a3ac(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 0], 7, -680876936), _0x14a341 = _0x20a3ac(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 1], 12, -389564586), _0x2bd1cd = _0x20a3ac(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 2], 17, 606105819), _0x1fdf74 = _0x20a3ac(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 3], 22, -1044525330), _0x5a7da4 = _0x20a3ac(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 4], 7, -176418897), _0x14a341 = _0x20a3ac(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 5], 12, 1200080426), _0x2bd1cd = _0x20a3ac(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 6], 17, -1473231341), _0x1fdf74 = _0x20a3ac(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 7], 22, -45705983), _0x5a7da4 = _0x20a3ac(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 8], 7, 1770035416), _0x14a341 = _0x20a3ac(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 9], 12, -1958414417), _0x2bd1cd = _0x20a3ac(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 10], 17, -42063), _0x1fdf74 = _0x20a3ac(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 11], 22, -1990404162), _0x5a7da4 = _0x20a3ac(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 12], 7, 1804603682), _0x14a341 = _0x20a3ac(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 13], 12, -40341101), _0x2bd1cd = _0x20a3ac(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 14], 17, -1502002290), _0x1fdf74 = _0x20a3ac(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 15], 22, 1236535329), _0x5a7da4 = _0x3705ba(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 1], 5, -165796510), _0x14a341 = _0x3705ba(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 6], 9, -1069501632), _0x2bd1cd = _0x3705ba(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 11], 14, 643717713), _0x1fdf74 = _0x3705ba(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 0], 20, -373897302), _0x5a7da4 = _0x3705ba(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 5], 5, -701558691), _0x14a341 = _0x3705ba(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 10], 9, 38016083), _0x2bd1cd = _0x3705ba(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 15], 14, -660478335), _0x1fdf74 = _0x3705ba(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 4], 20, -405537848), _0x5a7da4 = _0x3705ba(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 9], 5, 568446438), _0x14a341 = _0x3705ba(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 14], 9, -1019803690), _0x2bd1cd = _0x3705ba(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 3], 14, -187363961), _0x1fdf74 = _0x3705ba(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 8], 20, 1163531501), _0x5a7da4 = _0x3705ba(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 13], 5, -1444681467), _0x14a341 = _0x3705ba(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 2], 9, -51403784), _0x2bd1cd = _0x3705ba(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 7], 14, 1735328473), _0x1fdf74 = _0x3705ba(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 12], 20, -1926607734), _0x5a7da4 = _0x60ed3(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 5], 4, -378558), _0x14a341 = _0x60ed3(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 8], 11, -2022574463), _0x2bd1cd = _0x60ed3(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 11], 16, 1839030562), _0x1fdf74 = _0x60ed3(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 14], 23, -35309556), _0x5a7da4 = _0x60ed3(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 1], 4, -1530992060), _0x14a341 = _0x60ed3(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 4], 11, 1272893353), _0x2bd1cd = _0x60ed3(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 7], 16, -155497632), _0x1fdf74 = _0x60ed3(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 10], 23, -1094730640), _0x5a7da4 = _0x60ed3(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 13], 4, 681279174), _0x14a341 = _0x60ed3(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 0], 11, -358537222), _0x2bd1cd = _0x60ed3(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 3], 16, -722521979), _0x1fdf74 = _0x60ed3(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 6], 23, 76029189), _0x5a7da4 = _0x60ed3(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 9], 4, -640364487), _0x14a341 = _0x60ed3(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 12], 11, -421815835), _0x2bd1cd = _0x60ed3(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 15], 16, 530742520), _0x1fdf74 = _0x60ed3(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 2], 23, -995338651), _0x5a7da4 = _0x4396ce(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 0], 6, -198630844), _0x14a341 = _0x4396ce(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 7], 10, 1126891415), _0x2bd1cd = _0x4396ce(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 14], 15, -1416354905), _0x1fdf74 = _0x4396ce(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 5], 21, -57434055), _0x5a7da4 = _0x4396ce(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 12], 6, 1700485571), _0x14a341 = _0x4396ce(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 3], 10, -1894986606), _0x2bd1cd = _0x4396ce(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 10], 15, -1051523), _0x1fdf74 = _0x4396ce(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 1], 21, -2054922799), _0x5a7da4 = _0x4396ce(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 8], 6, 1873313359), _0x14a341 = _0x4396ce(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 15], 10, -30611744), _0x2bd1cd = _0x4396ce(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 6], 15, -1560198380), _0x1fdf74 = _0x4396ce(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 13], 21, 1309151649), _0x5a7da4 = _0x4396ce(_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341, _0x510f99[_0x288bb8 + 4], 6, -145523070), _0x14a341 = _0x4396ce(_0x14a341, _0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x510f99[_0x288bb8 + 11], 10, -1120210379), _0x2bd1cd = _0x4396ce(_0x2bd1cd, _0x14a341, _0x5a7da4, _0x1fdf74, _0x510f99[_0x288bb8 + 2], 15, 718787259), _0x1fdf74 = _0x4396ce(_0x1fdf74, _0x2bd1cd, _0x14a341, _0x5a7da4, _0x510f99[_0x288bb8 + 9], 21, -343485551), _0x5a7da4 = _0x5a7da4 + _0x1a8bf5 >>> 0, _0x1fdf74 = _0x1fdf74 + _0x44711f >>> 0, _0x2bd1cd = _0x2bd1cd + _0x359546 >>> 0, _0x14a341 = _0x14a341 + _0x5bb435 >>> 0;
                    }

                    return _0xa50d05['endian']([_0x5a7da4, _0x1fdf74, _0x2bd1cd, _0x14a341]);
                };

            _0x10ce55['_ff'] = function (_0x26061b, _0x35eab8, _0xb6103a, _0x4c414f, _0x1cdd42, _0x29648d, _0x2f1e5e) {
                var _0x4c3bcd = _0x26061b + (_0x35eab8 & _0xb6103a | ~_0x35eab8 & _0x4c414f) + (_0x1cdd42 >>> 0) + _0x2f1e5e;

                return (_0x4c3bcd << _0x29648d | _0x4c3bcd >>> 32 - _0x29648d) + _0x35eab8;
            }, _0x10ce55['_gg'] = function (_0x30d170, _0x11f682, _0x2156b9, _0x2ab564, _0x357859, _0x290e12, _0x3862e5) {
                var _0x188a1b = _0x30d170 + (_0x11f682 & _0x2ab564 | _0x2156b9 & ~_0x2ab564) + (_0x357859 >>> 0) + _0x3862e5;

                return (_0x188a1b << _0x290e12 | _0x188a1b >>> 32 - _0x290e12) + _0x11f682;
            }, _0x10ce55['_hh'] = function (_0x4658b4, _0x5a84c0, _0x17d959, _0x4b304a, _0x188b6c, _0x29c682, _0x53a39f) {
                var _0x3137c2 = _0x4658b4 + (_0x5a84c0 ^ _0x17d959 ^ _0x4b304a) + (_0x188b6c >>> 0) + _0x53a39f;

                return (_0x3137c2 << _0x29c682 | _0x3137c2 >>> 32 - _0x29c682) + _0x5a84c0;
            }, _0x10ce55['_ii'] = function (_0xe0b83c, _0x1d8706, _0x4625b3, _0x4b7d3f, _0x3fbae0, _0x3b638c, _0x5aaccf) {
                var _0x42b54c = _0xe0b83c + (_0x4625b3 ^ (_0x1d8706 | ~_0x4b7d3f)) + (_0x3fbae0 >>> 0) + _0x5aaccf;

                return (_0x42b54c << _0x3b638c | _0x42b54c >>> 32 - _0x3b638c) + _0x1d8706;
            }, _0x10ce55['_blocksize'] = 16, _0x10ce55['_digestsize'] = 16, _0x1e13e9['exports'] = function (_0x32e3ff, _0x16292e) {
                if (void 0 === _0x32e3ff || null === _0x32e3ff) throw new Error("Illegal argument " + _0x32e3ff);

                var _0x36f4c9 = _0xa50d05['wordsToBytes'](_0x10ce55(_0x32e3ff, _0x16292e));

                return _0x16292e && _0x16292e['asBytes'] ? _0x36f4c9 : _0x16292e && _0x16292e['asString'] ? _0x34fccd['bytesToString'](_0x36f4c9) : _0xa50d05['bytesToHex'](_0x36f4c9);
            };
        }();
    }, function (_0x4178e3, _0x30d8fe) {
        !function () {
            var _0x3d43c8 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
                _0x29d2d3 = {
                    'rotl': function (_0x54e1aa, _0x326cb1) {
                        return _0x54e1aa << _0x326cb1 | _0x54e1aa >>> 32 - _0x326cb1;
                    },
                    'rotr': function (_0x461e2b, _0x292f6c) {
                        return _0x461e2b << 32 - _0x292f6c | _0x461e2b >>> _0x292f6c;
                    },
                    'endian': function (_0x12f8f5) {
                        if (_0x12f8f5['constructor'] == Number) return 16711935 & _0x29d2d3['rotl'](_0x12f8f5, 8) | 4278255360 & _0x29d2d3['rotl'](_0x12f8f5, 24);
                        var _0x3b8a53 = 0;

                        for (; _0x3b8a53 < _0x12f8f5['length']; _0x3b8a53++) _0x12f8f5[_0x3b8a53] = _0x29d2d3['endian'](_0x12f8f5[_0x3b8a53]);

                        return _0x12f8f5;
                    },
                    'randomBytes': function (_0x2aa806) {
                        var _0x578920 = [];

                        for (; _0x2aa806 > 0; _0x2aa806--) _0x578920['push'](Math['floor'](256 * Math['random']()));

                        return _0x578920;
                    },
                    'bytesToWords': function (_0x1c3141) {
                        var _0x3df9c0 = [],
                            _0x22a5dd = 0,
                            _0x23cc7 = 0;

                        for (; _0x22a5dd < _0x1c3141['length']; _0x22a5dd++, _0x23cc7 += 8) _0x3df9c0[_0x23cc7 >>> 5] |= _0x1c3141[_0x22a5dd] << 24 - _0x23cc7 % 32;

                        return _0x3df9c0;
                    },
                    'wordsToBytes': function (_0x4160d7) {
                        var _0x490e3e = [],
                            _0xbae194 = 0;

                        for (; _0xbae194 < 32 * _0x4160d7['length']; _0xbae194 += 8) _0x490e3e['push'](_0x4160d7[_0xbae194 >>> 5] >>> 24 - _0xbae194 % 32 & 255);

                        return _0x490e3e;
                    },
                    'bytesToHex': function (_0x399656) {
                        var _0x1c5c4a = [],
                            _0xbd6b1f = 0;

                        for (; _0xbd6b1f < _0x399656['length']; _0xbd6b1f++) _0x1c5c4a['push']((_0x399656[_0xbd6b1f] >>> 4)['toString'](16)), _0x1c5c4a['push']((15 & _0x399656[_0xbd6b1f])['toString'](16));

                        return _0x1c5c4a['join']('');
                    },
                    'hexToBytes': function (_0x2e7e98) {
                        var _0x323135 = [],
                            _0x128a5f = 0;

                        for (; _0x128a5f < _0x2e7e98['length']; _0x128a5f += 2) _0x323135['push'](parseInt(_0x2e7e98['substr'](_0x128a5f, 2), 16));

                        return _0x323135;
                    },
                    'bytesToBase64': function (_0x35285e) {
                        var _0x2095b0 = [],
                            _0x18a4b0 = 0;

                        for (; _0x18a4b0 < _0x35285e['length']; _0x18a4b0 += 3) {
                            var _0x12e718 = _0x35285e[_0x18a4b0] << 16 | _0x35285e[_0x18a4b0 + 1] << 8 | _0x35285e[_0x18a4b0 + 2],
                                _0x2a7fed = 0;

                            var _0x12e718 = _0x35285e[_0x18a4b0] << 16 | _0x35285e[_0x18a4b0 + 1] << 8 | _0x35285e[_0x18a4b0 + 2],
                                _0x2a7fed = 0;

                            for (; _0x2a7fed < 4; _0x2a7fed++) 8 * _0x18a4b0 + 6 * _0x2a7fed <= 8 * _0x35285e['length'] ? _0x2095b0['push'](_0x3d43c8['charAt'](_0x12e718 >>> 6 * (3 - _0x2a7fed) & 63)) : _0x2095b0['push']('=');
                        }

                        return _0x2095b0['join']('');
                    },
                    'base64ToBytes': function (_0x466d0a) {
                        _0x466d0a = _0x466d0a['replace'](/[^A-Z0-9+\/]/gi, '');
                        var _0x102df7 = [],
                            _0x5cfeb9 = 0,
                            _0xd78a4 = 0;

                        for (; _0x5cfeb9 < _0x466d0a['length']; _0xd78a4 = ++_0x5cfeb9 % 4) 0 != _0xd78a4 && _0x102df7['push']((_0x3d43c8['indexOf'](_0x466d0a['charAt'](_0x5cfeb9 - 1)) & Math['pow'](2, -2 * _0xd78a4 + 8) - 1) << 2 * _0xd78a4 | _0x3d43c8['indexOf'](_0x466d0a['charAt'](_0x5cfeb9)) >>> 6 - 2 * _0xd78a4);

                        return _0x102df7;
                    }
                };
            _0x4178e3['exports'] = _0x29d2d3;
        }();
    }, function (_0x5412a4, _0x58b7ae) {
        function _0x3b40b1(_0x278db3) {
            return !!_0x278db3['constructor'] && 'function' == typeof _0x278db3['constructor']['isBuffer'] && _0x278db3['constructor']['isBuffer'](_0x278db3);
        }

        function _0x393737(_0x573e43) {
            return 'function' == typeof _0x573e43['readFloatLE'] && 'function' == typeof _0x573e43['slice'] && _0x3b40b1(_0x573e43['slice'](0, 0));
        }

        _0x5412a4['exports'] = function (_0x8eeaa) {
            return null != _0x8eeaa && (_0x3b40b1(_0x8eeaa) || _0x393737(_0x8eeaa) || !!_0x8eeaa['_isBuffer']);
        };
    }, function (_0x3e8d12, _0x3aef88, _0x1e5d4b) {
        _0x3e8d12['exports'] = _0x1e5d4b(1);
    }]);

    var _0x5609bd = function (_0x390b3d) {
        _0x390b3d = _0x390b3d['replace'](/\r\n/g, "\n");
        var _0x4c18ef = '';
        var _0x33908c = 0;

        for (; _0x33908c < _0x390b3d['length']; _0x33908c++) {
            var _0x2c4993 = _0x390b3d['charCodeAt'](_0x33908c);

            if (_0x2c4993 < 128) {
                _0x4c18ef += String['fromCharCode'](_0x2c4993);
            } else if (_0x2c4993 > 127 && _0x2c4993 < 2048) {
                _0x4c18ef += String['fromCharCode'](_0x2c4993 >> 6 | 192);
                _0x4c18ef += String['fromCharCode'](_0x2c4993 & 63 | 128);
            } else {
                _0x4c18ef += String['fromCharCode'](_0x2c4993 >> 12 | 224);
                _0x4c18ef += String['fromCharCode'](_0x2c4993 >> 6 & 63 | 128);
                _0x4c18ef += String['fromCharCode'](_0x2c4993 & 63 | 128);
            }
        }

        return _0x4c18ef;
    };

    var _0x1b80ed = 'A4NjFqYu5wPHsO0XTdDgMa2r1ZQocVte9UJBvk6/7=yRnhISGKblCWi+LpfE8xzm3';

    var _0x4acb01 = function (_0x19b406) {
        var _0x1c5e31 = 0;
        var _0x1c19ee = '';

        var _0x2b72d5, _0x4382ed, _0x4ed5d7, _0x37312a, _0x304f63, _0x2f11aa, _0x5abc14;

        var _0x346dfb = 0;
        _0x19b406 = _0x5609bd(_0x19b406);

        while (_0x346dfb < _0x19b406['length']) {
            var _0x41f057 = 0;
            _0x2b72d5 = _0x19b406['charCodeAt'](_0x346dfb++);
            _0x4382ed = _0x19b406['charCodeAt'](_0x346dfb++);
            _0x4ed5d7 = _0x19b406['charCodeAt'](_0x346dfb++);
            _0x37312a = _0x2b72d5 >> 2;
            _0x304f63 = (_0x2b72d5 & 3) << 4 | _0x4382ed >> 4;
            _0x2f11aa = (_0x4382ed & 15) << 2 | _0x4ed5d7 >> 6;
            _0x5abc14 = _0x4ed5d7 & 63;

            if (isNaN(_0x4382ed)) {
                _0x2f11aa = _0x5abc14 = 64;
            } else if (isNaN(_0x4ed5d7)) {
                _0x5abc14 = 64;
            }

            _0x1c19ee = _0x1c19ee + _0x1b80ed['charAt'](_0x37312a) + _0x1b80ed['charAt'](_0x304f63) + _0x1b80ed['charAt'](_0x2f11aa) + _0x1b80ed['charAt'](_0x5abc14);
        }

        return _0x1c19ee;
    };

    var _0x4346c9 = function (_0xa37392) {
        var _0x2d962d = Math['floor'](_0xa37392['length'] * Math['random']());

        var _0x9bb07e = ('' + _0xa37392 + _0xa37392)['substr'](_0x2d962d, _0xa37392['length']);

        return _0x9bb07e['slice'](0, _0x2d962d) + '_' + _0x9bb07e['slice'](_0x2d962d, _0xa37392['length']);
    };

    var _0xce618 = 'test';

    var _0xf2bb34 = new Date()['getTime']();

    var _0x3ac6ec = typeof window === 'undefined' ? global : window;

    if (typeof _0x3ac6ec !== 'undefined') {
        if (_0x3ac6ec && _0x3ac6ec['navigator'] && _0x3ac6ec['navigator']['userAgent'] && _0x3ac6ec['alert']) {
            _0xce618 = 'test';
        }
    }

    var _0x10dd73 = Object['prototype']['toString']['call'](_0xd5e273) === "[object Object]" || Object['prototype']['toString']['call'](_0xd5e273) === "[object Array]";

    var _0x5f5922 = {
        'X-s': _0x4acb01(_0x1e241f([_0xf2bb34, _0xce618, _0x1bb593, _0x10dd73 ? JSON['stringify'](_0xd5e273) : '']['join'](''))),
        'X-t': _0xf2bb34
    };
    return _0x5f5922;
}

var BLOCKED_HOSTS = ['t.xiaohongshu.com', 'c.xiaohongshu.com', 'spltest.xiaohongshu.com', 't2.xiaohongshu.com', 't2-test.xiaohongshu.com', 'lng.xiaohongshu.com', 'apm-track.xiaohongshu.com', 'apm-track-test.xiaohongshu.com', 'fse.xiaohongshu.com', 'fse.devops.xiaohongshu.com', 'fesentry.xiaohongshu.com'];

// window['sign'] = sign;
// t = {
//     "timeout": 30000,
//     "method": "GET",
//     "url": "/api/solar/cooperator/blogger/v1",
//     "matchedPath": "/api/solar/cooperator/blogger/v1",
//     "headers": {
//         "x-b3-traceid": "a12aee5c0b9bd017",
//         "Authorization": "",
//     }
// }
// f = '"/api/solar/cooperator/blogger/v1?cpc=false&column=comprehensiverank&sort=asc&location=&type=%E5%87%BA%E8%A1%8C,%E7%BE%8E%E5%A6%86,%E6%97%B6%E5%B0%9A,%E5%AE%B6%E5%B1%85%E5%AE%B6%E8%A3%85,%E7%BE%8E%E9%A3%9F&pageNum=1&pageSize=20&userType=0"'
//
// console.log(sign(f, t.data))