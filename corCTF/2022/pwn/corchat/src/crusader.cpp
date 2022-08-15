#include "crusader.h"
#include "inttypes.h"

Crusader::Crusader(int8_t client_fd, int uid)
{
    this->m_sock_fd = client_fd;
    this->m_uid = uid;
    this->uname = nullptr;
    this->uname_len = 10;
    this->is_admin = false;
}

Crusader::~Crusader()
{
    if (this->uname != nullptr)
        free(this->uname);
    if (this->m_sock_fd)
        close(this->m_sock_fd);
}

int Crusader::SendMsg(const char *msg, size_t msg_len, int8_t sender_id)
{
    if (sender_id == -1)
        return send(this->m_sock_fd, msg, msg_len, 0);
    std::cout << msg << std::endl;
    return send(this->m_sock_fd, msg, msg_len, 0);
}

bool Crusader::Recv(char *buf, size_t buf_size)
{
    int bytes_read;
    if ((bytes_read = read(this->m_sock_fd, buf, buf_size)) == 0 || bytes_read == -1)
    {
        std::cout << "[i] Crusader " << this->m_uid << " has disconnected." << std::endl;
        return false;
    }

    buf[bytes_read] = '\0';
    if (Parser::IsValid(buf, (size_t)bytes_read) == false)
    {
        std::cout << "[i] Crusader " << this->m_uid << " sent invalid data, disconnected." << std::endl;
        return false;
    }

    return true;
}

void Crusader::UpdateUname(const char **uname, size_t len)
{
    if (this->uname != nullptr)
    {
        free(this->uname);
        this->uname = nullptr;
    }
    this->uname = (char *)calloc(sizeof(char), 0x30);
    memcpy(this->uname, *uname, len);
    this->uname_len = len;
}

void Crusader::SetUname(const char *buf, size_t buf_size)
{
    this->UpdateUname(&buf, buf_size);
    std::string response = "Username has been set to " + this->GetUname() + "\n";
    this->SendMsg(response.data(), response.length(), -1);
}

std::string Crusader::RecvMessage()
{
    std::string msg = "";
    cor_msg_buf msg_buf;

    memset(msg_buf.buffer, '\x00', sizeof(msg_buf.buffer));

    if (read(this->m_sock_fd, &msg_buf.len, sizeof(msg_buf.len)) <= 0)
        return msg;

    if (msg_buf.len >= sizeof(msg_buf.buffer) || msg_buf.len == 0)
        return msg;

    if (read(this->m_sock_fd, &msg_buf.flags, sizeof(msg_buf.flags)) <= 0)
        return msg;

    msg_buf.len -= sizeof(msg_buf.flags);
    if (msg_buf.len <= 0)
        return msg;

    if (read(this->m_sock_fd, msg_buf.buffer, msg_buf.len) <= 0)
        return msg;

    msg_buf.buffer[msg_buf.len] = '\x00';
    msg += msg_buf.buffer;

    return msg;
}

std::string Crusader::RecvUname()
{
    std::string name = "";
    cor_uname_buf uname_buf;

    memset(uname_buf.buffer, '\x00', sizeof(uname_buf.buffer));

    if (read(this->m_sock_fd, &uname_buf.len, sizeof(uname_buf.len)) <= 0)
        return name;

    if (uname_buf.len >= sizeof(uname_buf.buffer) || uname_buf.len == 0)
        return name;

    if (read(this->m_sock_fd, uname_buf.buffer, uname_buf.len) <= 0)
        return name;

    uname_buf.buffer[uname_buf.len] = '\x00';
    name += uname_buf.buffer;

    return name;
}

std::string Crusader::GetUname()
{
    if (this->uname != nullptr)
    {
        return std::string(this->uname, this->uname_len);
    }

    return std::string("Crusader " + std::to_string(this->m_uid));
}
