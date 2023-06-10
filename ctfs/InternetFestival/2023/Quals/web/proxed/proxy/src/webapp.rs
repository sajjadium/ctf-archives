use std::env;
use std::io::Write;
use std::net::TcpStream;
use std::sync::Arc;
use std::thread;
use std::time::Duration;

const ERROR_RESPONSE: &'static str = "HTTP/1.1 500 OK\r\nContent-Length: 5\r\n\r\nERROR";

pub fn start(
    incoming_queue: Arc<crate::queue::BlockingQueue<String>>,
    outgoing_queue: Arc<crate::queue::BlockingQueue<String>>,
) {
    // Echo
    loop {
        let req: String = incoming_queue.pop();
        let mut stream = create_connection();

        match stream.write_all(req.as_bytes()) {
            Err(_x) => {
                continue;
            }
            _ => {}
        };
        match stream.flush() {
            Err(_x) => {
                continue;
            }
            _ => {}
        }

        let resp = match crate::http::get_response(&mut stream) {
            Ok(x) => x,
            Err(_err) => {
                outgoing_queue.push(String::from(ERROR_RESPONSE));
                continue;
            }
        };
        outgoing_queue.push(resp);
    }
}

fn create_connection() -> TcpStream {
    loop {
        let backend_domain = env::var("BACKEND_DOMAIN").expect("No backend domain specified!");
        let stream = TcpStream::connect(format!("{}:5000", backend_domain));
        match stream {
            Err(_x) => {
                println!("Can't connect to backend!");
                thread::sleep(Duration::from_secs(1));
            }
            Ok(stream) => {
                return stream;
            }
        }
    }
}
