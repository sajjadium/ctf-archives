use std::net::{Ipv4Addr, SocketAddr};
use std::str::FromStr;
use std::sync::Arc;
use anyhow::{anyhow, Error};
use bytes::{BufMut, Bytes, BytesMut};
use bytes::Buf;
use h3::error::ErrorLevel;
use h3::quic::BidiStream;
use h3::server::RequestStream;
use http::{HeaderName, HeaderValue, Method, Request, Response, StatusCode};
use http_body_util::Full;
use httparse::Status;
use hyper::body::Incoming;
use hyper_util::rt::{TokioExecutor, TokioIo};
use rustls::{Certificate, PrivateKey, ServerConfig};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};
use tokio_rustls::TlsAcceptor;
use url::Url;

#[tokio::main]
async fn main() {
    let certificates = std::fs::read("cert.crt").expect("Failed to read cert.crt");
    let certificates: Vec<_> = rustls_pemfile::certs(&mut certificates.as_slice())
        .map(|cert| {
            let cert = cert.expect("Failed to parse cert.crt");
            Certificate(cert.to_vec())
        })
        .collect();
    let key = std::fs::read("cert.key").expect("Failed to read cert.key");
    let key = rustls_pemfile::private_key(&mut key.as_slice())
        .expect("Failed to parse cert.key")
        .expect("cert.key contains no private keys");
    let key = PrivateKey(key.secret_der().to_vec());

    let h2_task = {
        let certificates = certificates.clone();
        let key = key.clone();
        tokio::spawn(async move {
            run_h2_server(certificates, key).await
        })
    };

    let h3_task = tokio::spawn(async move {
        run_h3_server(certificates, key).await
    });

    let _ = tokio::join!(h2_task, h3_task);
}

async fn run_h2_server(certificates: Vec<Certificate>, key: PrivateKey) {
    let mut tls_config = ServerConfig::builder()
        .with_safe_default_cipher_suites()
        .with_safe_default_kx_groups()
        .with_protocol_versions(&[&rustls::version::TLS13])
        .unwrap()
        .with_no_client_auth()
        .with_single_cert(certificates, key)
        .expect("Failed to create TLS configuration");
    tls_config.alpn_protocols = vec!["h2".as_bytes().to_vec()];
    let tls_acceptor = TlsAcceptor::from(Arc::new(tls_config));

    let address = SocketAddr::from((Ipv4Addr::from(0), 443));
    let listener = TcpListener::bind(address)
        .await
        .expect("Failed to bind to 0.0.0.0:443");

    println!("HTTP/2: Listening on 0.0.0.0:443");

    loop {
        if let Ok((stream, _)) = listener.accept().await {
            let tls_acceptor = tls_acceptor.clone();
            tokio::spawn(async move {
                let _ = handle_h2_connection(stream, &tls_acceptor).await;
            });
        }
    }
}

async fn handle_h2_connection(stream: TcpStream, tls_acceptor: &TlsAcceptor) -> Result<(), Error> {
    let tls_stream = tls_acceptor.accept(stream).await?;

    let _ = hyper::server::conn::http2::Builder::new(TokioExecutor::new())
        .serve_connection(TokioIo::new(tls_stream), hyper::service::service_fn(handle_h2_request))
        .await;

    Ok(())
}

async fn handle_h2_request(_: Request<Incoming>) -> Result<Response<Full<Bytes>>, Error> {
    let response = Response::builder()
        .header(http::header::ALT_SVC, "h3=\":443\"")
        .status(StatusCode::OK)
        .body(Full::new(Bytes::from("Please use HTTP/3. \
        I put so much effort into upgrading ALL the server infrastructure use HTTP/3. I hope it didn't add any bugs!\n\
        You can probably do this by refreshing the page.\n\
        \n\
        Here are some reasons you should use HTTP/3:\n\
        HTTP/3 brings several improvements over its predecessors, particularly in terms of performance and security. Here are some key reasons why you should consider using HTTP/3:\n\
        Improved Performance: HTTP/3 is built on top of the QUIC protocol, which uses UDP instead of TCP. This reduces latency and speeds up connections, especially for websites that require multiple requests.\n\
        Multiplexing: HTTP/3 supports multiplexing at the protocol level, allowing multiple streams of data to be sent concurrently over a single connection. This can lead to faster loading times for websites with many resources.\n\
        Reduced Head-of-Line Blocking: In HTTP/2, if one resource encounters an issue during transmission, it can block other resources from being delivered, leading to performance bottlenecks. HTTP/3's use of QUIC helps mitigate this problem by isolating streams, reducing the impact of such blocking.\n\
        Connection Migration: HTTP/3 allows for seamless connection migration between IP addresses or networks. This can be beneficial in scenarios where devices switch networks frequently, such as mobile devices moving between Wi-Fi and cellular networks.\n\
        Improved Security: HTTP/3 mandates the use of TLS encryption, providing a secure connection by default. This helps protect data from interception and tampering, enhancing overall security for web communications.\n\
        Better Handling of Packet Loss: QUIC, the underlying protocol of HTTP/3, includes mechanisms for handling packet loss more efficiently than TCP. This can lead to improved performance in networks with high packet loss rates, such as wireless networks or congested connections.\n\
        Future-Proofing: As technologies evolve, HTTP/3 is designed to be more adaptable and scalable than previous versions. It can accommodate new requirements and optimizations as they emerge, ensuring that your web infrastructure remains relevant and efficient.\n\
        While HTTP/3 offers numerous benefits, it's essential to consider factors such as server and client support, network configurations, and compatibility with existing systems before transitioning to this protocol.")))
        .unwrap();

    Ok(response)
}

async fn run_h3_server(certificates: Vec<Certificate>, key: PrivateKey) {
    let mut tls_config = ServerConfig::builder()
        .with_safe_default_cipher_suites()
        .with_safe_default_kx_groups()
        .with_protocol_versions(&[&rustls::version::TLS13])
        .unwrap()
        .with_no_client_auth()
        .with_single_cert(certificates, key)
        .expect("Failed to create TLS configuration");
    tls_config.alpn_protocols = vec!["h3".as_bytes().to_vec()];

    let server_config = quinn::ServerConfig::with_crypto(Arc::new(tls_config));
    let endpoint = quinn::Endpoint::server(server_config, SocketAddr::from((Ipv4Addr::from(0), 443)))
        .expect("Failed to create quinn endpoint");

    println!("HTTP/3: Listening on 0.0.0.0:443");

    while let Some(connecting) = endpoint.accept().await {
        tokio::spawn(async move {
            if let Ok(connection) = connecting.await {
                if let Ok(connection) = h3::server::Connection::new(h3_quinn::Connection::new(connection)).await {
                    handle_h3_connection(connection).await
                }
            }
        });
    }

    endpoint.wait_idle().await;
}

async fn handle_h3_connection(mut connection: h3::server::Connection<h3_quinn::Connection, Bytes>) {
    loop {
        match connection.accept().await {
            Ok(Some((request, stream))) => {
                tokio::spawn(async {
                    let _ = handle_h3_request(request, stream).await;
                });
            }
            Ok(None) => {
                break;
            }
            Err(err) => {
                match err.get_error_level() {
                    ErrorLevel::ConnectionError => break,
                    ErrorLevel::StreamError => continue,
                }
            }
        }
    }
}

async fn handle_h3_request<T>(request: Request<()>, mut stream: RequestStream<T, Bytes>) -> Result<(), Error>
    where T: BidiStream<Bytes> {
    let mut body = BytesMut::new();
    while let Some(data) = stream.recv_data().await? {
        body.extend_from_slice(data.chunk());
    }

    if request.uri().path() == "/admin/register" {
        stream.send_response(Response::builder().status(StatusCode::UNAUTHORIZED).body(()).unwrap()).await?;
        stream.send_data(Bytes::from("Unauthorized")).await?;
        stream.finish().await?;
        return Ok(());
    }

    let body = if request.method() == Method::GET { Bytes::new() } else { Bytes::from(body) };

    let mut proxy_stream = TcpStream::connect("app:80").await?;
    proxy_stream.write_all(request_to_h1_bytes(request, body).as_ref()).await?;
    let (proxied_response, proxied_body) = read_h1_response(proxy_stream).await?;

    stream.send_response(proxied_response).await?;
    stream.send_data(proxied_body).await?;
    stream.finish().await?;

    Ok(())
}

fn request_to_h1_bytes<T: Buf>(request: Request<()>, body: T) -> Bytes {
    let path = request.uri().path_and_query()
        .map(|path| path.as_str())
        .unwrap_or("/");
    let mut proxied_request_headers = request.headers().clone();
    proxied_request_headers.remove(http::header::CONTENT_LENGTH);
    proxied_request_headers.insert(http::header::HOST, HeaderValue::from_static("app:80"));
    if request.method() == Method::POST {
        proxied_request_headers.insert(http::header::CONTENT_LENGTH, HeaderValue::from(body.remaining()));
    }
    let mut proxied_request_text = BytesMut::new();
    proxied_request_text.put_slice(format!("{} {} HTTP/1.1\r\n", request.method(), path).as_bytes());
    for (header_name, header_value) in &proxied_request_headers {
        proxied_request_text.put_slice(format!("{}: ", header_name).as_bytes());
        proxied_request_text.put_slice(header_value.as_bytes());
        proxied_request_text.put_slice(b"\r\n");
    }
    proxied_request_text.put_slice(b"\r\n");
    proxied_request_text.put(body);

    return Bytes::from(proxied_request_text);
}

fn parse_response_builder(buf: &[u8]) -> Result<Option<(http::response::Builder, usize)>, Error> {
    let mut parsed_headers = [httparse::EMPTY_HEADER; 64];
    let mut parsed_response = httparse::Response::new(&mut parsed_headers);
    if let Status::Complete(bytes_read) = parsed_response.parse(&buf)? {
        let mut proxied_response_builder = Response::builder()
            .status(parsed_response.code.ok_or(anyhow!("status is missing"))?);
        let proxied_response_headers = proxied_response_builder.headers_mut().unwrap();
        for header in parsed_response.headers {
            proxied_response_headers.insert(HeaderName::from_str(header.name)?, HeaderValue::from_bytes(header.value)?);
        }

        return Ok(Some((proxied_response_builder, bytes_read)));
    }

    Ok(None)
}

async fn read_h1_response(mut proxy_stream: TcpStream) -> Result<(Response<()>, Bytes), Error> {
    let mut parsed_response_buf = BytesMut::new();
    let mut read_buf = [0; 1024];
    let mut proxied_response_builder;
    let request_bytes_read;
    loop {
        let bytes_read = proxy_stream.read(&mut read_buf).await?;
        parsed_response_buf.extend_from_slice(&read_buf[0..bytes_read]);

        if let Some((new_builder, new_bytes_read)) = parse_response_builder(&parsed_response_buf)? {
            proxied_response_builder = new_builder;
            request_bytes_read = new_bytes_read;
            break;
        }
    }

    let proxied_response_headers = proxied_response_builder.headers_mut().ok_or(anyhow!("error parsing response"))?;
    let content_length = proxied_response_headers.get(http::header::CONTENT_LENGTH)
        .and_then(|value| value.to_str().ok().and_then(|value| value.parse::<u32>().ok()));
    let proxied_body = if let Some(content_length) = content_length {
        let mut buf = vec![0; content_length as usize];
        let body_bytes_already_read = parsed_response_buf.remaining() - request_bytes_read;
        buf[0..body_bytes_already_read].copy_from_slice(&parsed_response_buf[request_bytes_read..]);
        proxy_stream.read_exact(&mut buf[body_bytes_already_read..]).await?;
        Bytes::from(buf)
    } else {
        Bytes::new()
    };
    proxied_response_headers.remove(http::header::CONTENT_LENGTH);
    if let Some(location) = proxied_response_headers.get_mut(http::header::LOCATION) {
        if let Ok(location_str) = location.to_str() {
            if let Ok(mut location_url) = Url::parse(location_str) {
                location_url.set_scheme("https").map_err(|_| anyhow!("error setting scheme"))?;
                location_url.set_host(Some("http-fanatics.challs.umdctf.io"))?;
                location_url.set_port(Some(443)).map_err(|_| anyhow!("error setting port"))?;
                *location = HeaderValue::from_str(location_url.as_str())?;
            }
        }
    }
    let proxied_response = proxied_response_builder.body(())?;

    Ok((proxied_response, proxied_body))
}
