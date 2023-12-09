Rails.application.routes.draw do
  root "session#home"
  resources :users , only: [:new, :create, :edit, :update, :show, :destroy, :reset, :reset_submit]
  
  resources :comments, only: [:create, :destroy]
  
  get "/login", to: "session#login"
  post "/login", to: "session#create"
  get "/register", to: "users#new"
  post "/register", to: "users#create"
  get "/logout", to: "session#destroy"
  post "/logout", to: "session#destroy"
  get "/reset", to: "users#reset"
  post "/reset", to: "users#reset"
  get "/reset_submit", to: "users#reset_submit"
  post "/reset_submit", to: "users#reset_submit"
  get "/preview", to: "cats#preview"

  resources :admin, only: [:index]

  resources :cats do
    resources :comments
  end
end