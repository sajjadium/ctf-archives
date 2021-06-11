defmodule Server do
  use Application

  def start(_type, _args) do
    children = [
      {Task.Supervisor, name: PastePalooza.TaskSupervisor},
      Supervisor.child_spec({Task, fn -> PastePalooza.accept(3001) end}, restart: :permanent)
    ]

    opts = [strategy: :one_for_one, name: PastePalooza.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
