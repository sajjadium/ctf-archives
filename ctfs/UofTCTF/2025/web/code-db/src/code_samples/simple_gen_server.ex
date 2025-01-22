defmodule SimpleGenServer do
  use GenServer

  # Client API
  def start_link(initial_value) do
    GenServer.start_link(__MODULE__, initial_value, name: __MODULE__)
  end

  def increment do
    GenServer.call(__MODULE__, :increment)
  end

  def get_value do
    GenServer.call(__MODULE__, :get)
  end

  # Server Callbacks
  def init(initial_value) do
    {:ok, initial_value}
  end

  def handle_call(:increment, _from, state) do
    {:reply, :ok, state + 1}
  end

  def handle_call(:get, _from, state) do
    {:reply, state, state}
  end
end

# Usage
{:ok, _pid} = SimpleGenServer.start_link(0)
SimpleGenServer.increment()
IO.puts("Current value: \#{SimpleGenServer.get_value()}")
