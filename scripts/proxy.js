/**
 * Proxy server to avoid bans from youtube
 * when using Pafy and Youtube-dl
 */

const http = require('http');
const net = require('net');
const url = require('url');
const port = process.env.PORT || 8383;

const AUTH_USER = process.env.USER;
const AUTH_PASSWORD = process.env.PASSWORD;

if (!(AUTH_USER && AUTH_PASSWORD)) {
    throw new Error("You need to specify USER and PASSWORD env variables");
}

const requestHandler = (req, res) => {
    // discard all requests to proxy server except HTTP/1.1 CONNECT method
    res.writeHead(405, { 'Content-Type': 'text/plain' })
    res.end('Method not allowed')
}

const server = http.createServer(requestHandler)

const listener = server.listen(port, (err) => {
    if (err) {
        return console.error(err)
    }
    const info = listener.address()
    console.log(`Server is listening on address ${info.address} port ${info.port}`)
})

server.on('connect', (req, clientSocket, head) => {
    // listen only for HTTP/1.1 CONNECT method
    console.log("CONNECT:", clientSocket.remoteAddress, clientSocket.remotePort, req.method, req.url)

    if (!isAuthenticationValid(req)) {
        console.log("Invalid authentication")
        clientSocket.write([
            'HTTP/1.1 407 Proxy Valid Authentication Required',
            'Proxy-Authenticate: Basic realm="proxy"',
            'Proxy-Connection: close',
        ].join('\r\n'))
        clientSocket.end()
        clientSocket.destroy();
        return;
    }

    const { port, hostname } = url.parse(`//${req.url}`, false, true) // extract destination host and port from CONNECT request
    if (hostname && port) {
        const serverErrorHandler = (err) => {
            console.error(err.message);
            if (clientSocket) {
                clientSocket.end(`HTTP/1.1 500 ${err.message}\r\n`)
            }
        }
        const serverEndHandler = () => {
            if (clientSocket) {
                clientSocket.end(`HTTP/1.1 500 External Server End\r\n`)
            }
        }
        const serverSocket = net.connect(port, hostname) // connect to destination host and port
        const clientErrorHandler = (err) => {
            console.error(err.message)
            if (serverSocket) {
                serverSocket.end()
            }
        }
        const clientEndHandler = () => {
            if (serverSocket) {
                serverSocket.end()
            }
        }
        clientSocket.on('error', clientErrorHandler)
        clientSocket.on('end', clientEndHandler)
        serverSocket.on('error', serverErrorHandler)
        serverSocket.on('end', serverEndHandler)
        serverSocket.on('connect', () => {
            clientSocket.write([
                'HTTP/1.1 200 Connection Established',
                'Proxy-agent: Node-VPN',
            ].join('\r\n'))
            clientSocket.write('\r\n\r\n') // empty body
            // "blindly" (for performance) pipe client socket and destination socket between each other
            serverSocket.pipe(clientSocket, { end: false })
            clientSocket.pipe(serverSocket, { end: false })
        })
    } else {
        clientSocket.end('HTTP/1.1 400 Bad Request\r\n')
        clientSocket.destroy()
    }
})

function isAuthenticationValid(req) {
    const authHeader = req.headers['proxy-authorization'];
    if (authHeader) {
        const [keyword, authHash] = (authHeader || "").split(" ");
        if (keyword.toLowerCase() === "basic" && authHash) {
            const [username, password] = extractUserAndPassword(authHash);
            if (username === AUTH_USER && password === AUTH_PASSWORD) {
                return true;
            }
        }
    }
    return false;
}


function extractUserAndPassword(encodedUserAndPassword) {
    let splitHash = decodeBase64(encodedUserAndPassword).split(":");
    const username = splitHash.shift();
    // We join again in case the password includes ":"
    const password = splitHash.join(":");
    return [username, password];
}

function decodeBase64(input) {
    return Buffer.from(input, "base64").toString("utf8");
}