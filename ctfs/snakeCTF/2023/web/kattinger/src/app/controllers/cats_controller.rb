class CatsController < ApplicationController
  include SessionHelper
  include CatsHelper

  def cat_exists?
    return if Cat.exists?(params[:id])

    raise ActionController::BadRequest, "Cat doesn't exist"
  end

  def index
    @kittens = Cat.all
  end

  def show
    cat_exists?

    @kitten = Cat.find(params[:id])
    @user   = current_user
  end

  def new
    @kitten = Cat.new
  end

  def create
    @kitten = Cat.new(cat_params)
    if @kitten.save
      redirect_to @kitten
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit
    cat_exists?

    @kitten = Cat.find(params[:id])
  end

  def update
    cat_exists?

    @kitten = Cat.find(params[:id])
    if @kitten.update(cat_params)
      redirect_to @kitten
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def preview
    cat_exists?
    @kitten = Cat.find(params[:id])
    @image_url = @kitten.location
    return unless is_admin?

    @processed_data = process_image(@image_url)
  end

  def destroy
    cat_exists?

    @kitten = Cat.find(params[:id])
    @kitten.destroy
    redirect_to action: 'index', status: :see_other
  end

  private

  def cat_params
    params.require(:cat).permit(:description, :location)
  end
end
