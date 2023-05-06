Rails.application.routes.draw do
  get "/viene", to: "viene#index"
  post "/viene", to: "viene#index"
  put "/viene", to: "viene#index"
end