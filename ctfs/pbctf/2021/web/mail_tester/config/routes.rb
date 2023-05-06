Rails.application.routes.draw do
  root "login#index"
  post 'login', to: "login#create"

  get 'email', to: "email#index"
  post 'email', to: "email#create"
end
