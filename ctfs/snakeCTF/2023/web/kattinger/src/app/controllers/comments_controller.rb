class CommentsController < ApplicationController
  include SessionHelper

  def comment_exists?
    return if Comment.exists?(params[:id])

    raise ActionController::BadRequest, "Comment doesn't exist"
  end

  def current_user_comment?
    c = Comment.find(params[:id])
    return unless current_user.id != c.user_id && !is_admin?

    raise ActionController::RoutingError, 'Unauthorized'
  end

  def create
    @comment = Comment.new(comment_params)
    @comment = Comment.create(comment_params)
    @comment.save
    redirect_to cat_path(params[:cat_id])
    nil
  end

  def destroy
    comment_exists?
    current_user_comment?

    @comment = Comment.find(params[:id])
    @comment.destroy
    redirect_to user_path
    nil
  end

  private

  def comment_params
    params.permit(:cat_id, :user_id, :body, :rate)
  end
end
