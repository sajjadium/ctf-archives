require "test_helper"

class LoginControllerTest < ActionDispatch::IntegrationTest
  test "should get create" do
    get login_create_url
    assert_response :success
  end
end
