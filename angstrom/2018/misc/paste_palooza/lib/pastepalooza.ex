defmodule PastePalooza do
  require Logger

  def accept(port) do
    {:ok, socket} = :gen_tcp.listen(port, [:binary, packet: :line, active: false, reuseaddr: true])
    Logger.info "Accepting connections on port #{port}"
    loop_acceptor(socket)
  end

  defp loop_acceptor(socket) do
    {:ok, client} = :gen_tcp.accept(socket)
    serve(client)
    loop_acceptor(socket)
  end

  defp serve(socket) do
    write_line(socket, "Welcome to Paste Palooza!\n")
    write_line(socket, "Currently, only the file access feature is available.\n")
    write_line(socket, "Access a file by entering its name: ")
    {:ok, filename} = read_line(socket)
    response = Utility.access(filename)
    write_line(socket, response)
    :gen_tcp.close(socket)
  end

  defp read_line(socket) do
    :gen_tcp.recv(socket, 0)
  end

  defp write_line(socket, text) do
    :gen_tcp.send(socket, text)
  end
end
