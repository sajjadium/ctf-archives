use std::io::{BufRead, BufReader};
use std::io::{Error, ErrorKind, Read, Result};
use std::net::TcpStream;
use std::time::Duration;

pub struct HTTPRequest {
    request_line: String,
    headers: Vec<String>,
    body: Option<String>,
}

impl HTTPRequest {
    pub fn to_string(self) -> String {
        let mut request = self.request_line;
        self.headers.iter().for_each(|x| {
            request += "\r\n";
            request.push_str(x);
        });

        request += "\r\n\r\n";

        match self.body {
            Some(body) => request.push_str(&body),
            None => {}
        }

        request
    }
}

pub fn get_request(stream: &mut TcpStream) -> Result<HTTPRequest> {
    stream.set_read_timeout(Some(Duration::from_secs(5)))?;

    let mut buf_reader = BufReader::new(stream);

    // Read request line
    let request_line = get_request_line(&mut buf_reader)?;

    // Read headers
    let headers = get_headers(&mut buf_reader)?;

    // Search for Content-Lenght header
    let content_length: Option<usize> = get_content_length(&headers);

    // If content-lenght read body
    let body: Option<String> = match content_length {
        Some(x) => {
            let body = get_body(&mut buf_reader, x)?;
            Some(body)
        }
        None => None,
    };

    return Ok(HTTPRequest {
        request_line: request_line,
        headers: headers,
        body: body,
    });
}

fn request_error(content: &'static str) -> Error {
    Error::new(ErrorKind::Other, content)
}

fn get_request_line(
    buf_reader: &mut std::io::BufReader<&mut std::net::TcpStream>,
) -> Result<String> {
    let mut l: String = String::new();
    buf_reader.read_line(&mut l)?;
    let l = l.trim().to_string();

    let splitted: Vec<&str> = l.split(" ").collect();

    if splitted.len() != 3 {
        return Err(request_error("Wrong request line"));
    }

    if splitted[0] != "GET" && splitted[0] != "POST" {
        return Err(request_error("Wrong request method"));
    }

    if !splitted[1].starts_with("/") {
        return Err(request_error("Wrong path"));
    }

    Ok(l)
}

fn get_headers(
    buf_reader: &mut std::io::BufReader<&mut std::net::TcpStream>,
) -> Result<Vec<String>> {
    let mut headers: Vec<String> = Vec::new();

    loop {
        let header = get_header(buf_reader)?;
        if header.len() == 0 {
            break;
        }
        headers.push(header);
    }

    Ok(headers)
}

fn get_header(buf_reader: &mut std::io::BufReader<&mut std::net::TcpStream>) -> Result<String> {
    let mut l: String = String::new();
    buf_reader.read_line(&mut l)?;
    let l = l.trim().to_string();

    // Check if end of head request
    if l.len() == 0 {
        return Ok(l);
    }

    let splitted: Vec<&str> = l.split(": ").collect();
    if splitted.len() < 2 {
        return Err(request_error("Invalid header format"));
    }

    Ok(l)
}

fn get_content_length(headers: &Vec<String>) -> Option<usize> {
    headers
        .iter()
        .filter(|x: &&std::string::String| x.to_lowercase().starts_with("content-length"))
        .map(|x: &std::string::String| {
            let splitted: Vec<&str> = x.split(": ").collect();
            splitted[1]
        })
        .map(|x| x.parse::<usize>())
        .filter(|x| x.is_ok())
        .map(|x| x.unwrap())
        .nth(0)
}

fn get_body(
    buf_reader: &mut std::io::BufReader<&mut std::net::TcpStream>,
    content_length: usize,
) -> Result<String> {
    let mut l: Vec<u8> = vec![0; content_length];

    buf_reader.read_exact(&mut l)?;

    match String::from_utf8(l) {
        Ok(x) => Ok(x),
        Err(_x) => Err(request_error("Invalid body")),
    }
}

pub fn get_response(stream: &mut TcpStream) -> Result<String> {
    let mut buf_reader = BufReader::new(stream);

    // Read response line
    let request_line = get_response_line(&mut buf_reader)?;
    let mut response = request_line;

    // Read headers
    let headers = get_headers(&mut buf_reader)?;
    headers.iter().for_each(|x| {
        response += "\r\n";
        response.push_str(x);
    });

    // Add end of head
    response += "\r\n\r\n";

    // Search for Content-Lenght header
    let content_length: Option<usize> = get_content_length(&headers);

    // If content-lenght read body
    match content_length {
        Some(x) => {
            let body: String = get_body(&mut buf_reader, x)?;
            response.push_str(&body);
        }
        None => {}
    }

    return Ok(response);
}

fn get_response_line(
    buf_reader: &mut std::io::BufReader<&mut std::net::TcpStream>,
) -> Result<String> {
    let mut l: String = String::new();
    buf_reader.read_line(&mut l)?;
    let l = l.trim().to_string();

    Ok(l)
}
