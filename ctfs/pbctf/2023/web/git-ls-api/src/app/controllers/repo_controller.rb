class RepoController < ApplicationController
  before_action :check_repo

  def index
    render json: {
      sha: repo_sha,
      files: repo_files
    }
  rescue StandardError => e
    puts e
    render json: { error: 'There was an error' }, status: 500
  end

  private

  def permitted_params
    @permitted_params ||= begin
      repo, api_endpoint = params.permit(%i[repo api_endpoint])
      {}.merge(repo || {}, api_endpoint || {}).symbolize_keys
    end
  end

  def repo
    @repo ||= permitted_params[:repo]
  end

  def api_endpoint
    @api_endpoint ||= permitted_params[:api_endpoint] || 'https://api.github.com'
  end

  def check_repo
    render json: 'Missing repo', status: 404 unless repo.present?
  end

  def client
    @client ||= Octokit::Client.new(api_endpoint: api_endpoint)
  end

  def files_cache_key
    @files_cache_key ||= "files/host/#{api_endpoint}/repo/#{repo}"
  end

  def sha_cache_key
    @sha_cache_key ||= "sha/host/#{api_endpoint}/repo/#{repo}"
  end

  def repo_files
    Rails.cache.fetch(files_cache_key, expires_in: 5.minutes, raw: true) do
      client.tree(repo, 'HEAD').tree.map { |entry| entry.path }.join(', ')
    end
  end

  def repo_sha
    Rails.cache.fetch(sha_cache_key, expires_in: 5.minutes, raw: true) do
      client.tree(repo, 'HEAD').sha
    end
  end
end
