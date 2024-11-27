const libssl = Process.getModuleByName('libssl.so');

var SSL_write = libssl.getExportByName('SSL_write');

Interceptor.attach(SSL_write, {
    onEnter: function (args) {
        const buf = args[1];
        const num = args[2];

        var byteArray = [];
        for (var i = 0; i < num; i++) {
            byteArray.push(buf.add(i).readU8());
        }
        Thread.backtrace(this.context, Backtracer.FUZZY).map(addr => {
            console.log('[!]', DebugSymbol.fromAddress(addr));
        });
        // send({ buf: byteArray });
    }
});