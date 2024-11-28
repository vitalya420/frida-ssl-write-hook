const libssl = Process.getModuleByName('libssl.so');


const SSL_write = libssl.getExportByName('SSL_write');
const SSL_read = libssl.getExportByName('SSL_read');
const SSL_set_fd = libssl.getExportByName('SSL_set_fd');



Interceptor.attach(SSL_read, {
    onEnter(args){
        this.sslCtx = args[0];
        this.buf = args[1];
        this.num = args[2].toInt32();
    },
    onLeave(byte_read){
        byte_read = byte_read.toInt32();
        if (byte_read > 0){            
            const bytes = this.buf.readByteArray(byte_read);
            send({func: 'SSL_read', ssl: this.sslCtx}, bytes);
        }
    }
});

Interceptor.attach(SSL_write, {
    onEnter: function (args) {
        const buf = args[1];
        const num = args[2];

        var byteArray = [];
        for (var i = 0; i < num; i++) {
            byteArray.push(buf.add(i).readU8());
        }
        // Thread.backtrace(this.context, Backtracer.FUZZY).map(addr => {
        //     console.log('[!]', DebugSymbol.fromAddress(addr));
        // });
        // send({ SSL_write: byteArray });
    }
});
