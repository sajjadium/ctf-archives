Rails.application.routes.draw do
  get '*repo', to: 'repo#index'

  root to: 'repo#index'
end
