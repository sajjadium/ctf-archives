defmodule Utility do

  def access(filename) do
    unsafe = "pastes/" <> filename <> ".txt"
    path = filter(unsafe <> <<0>>, "", String.length(unsafe))
    case File.read path do
      {:ok, content} -> content
      {:error, reason} -> "File not found.\n"
    end
  end

  def filter(<< head, tail :: binary >>, acc, n) do
    if n == 0 do 
      acc
    else
      n = n - 1
      if head < 33 or head > 126 do
        filter(tail, acc, n)
      else
        filter(tail, acc <> <<head>>, n)
      end
    end
  end
end